"""Base classes for the plugin system."""

import inspect
import re
from abc import ABC
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Type


@dataclass
class VariableValidation:
    """Validation rules for plugin variables."""

    options: Optional[List[Any]] = None
    range: Optional[Tuple[Optional[Any], Optional[Any]]] = None
    pattern: Optional[str] = None
    error_message: Optional[str] = None

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """Validate a value against the rules.

        Args:
            value: The value to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if self.options is not None and value not in self.options:
            return False, self.error_message or f"Value must be one of: {self.options}"

        if self.range is not None:
            min_val, max_val = self.range
            if min_val is not None and value < min_val:
                return False, self.error_message or f"Value must be >= {min_val}"
            if max_val is not None and value > max_val:
                return False, self.error_message or f"Value must be <= {max_val}"

        if self.pattern is not None:
            if not isinstance(value, str):
                return (
                    False,
                    self.error_message or "Value must be a string for pattern validation",
                )
            if not re.match(self.pattern, value):
                return (
                    False,
                    self.error_message or f"Value must match pattern: {self.pattern}",
                )

        return True, None


class PluginVariable:
    """Configuration variable for a plugin."""

    def __init__(
        self,
        type: Type = str,
        description: str = "",
        default: Optional[Any] = None,
        sensitive: bool = False,
        validation: Optional[VariableValidation] = None,
        name: Optional[str] = None,
    ):
        """Initialize a plugin variable.

        Args:
            type: The expected type of the variable
            description: Description of the variable
            default: Default value if not specified
            sensitive: Whether this variable contains sensitive information
            validation: Validation rules for the variable
            name: Name of the variable (set automatically from class attribute name)
        """
        self.type = type
        self.description = description
        self.default = default
        self.sensitive = sensitive
        self.validation = validation
        self.name = name

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """Validate a value for this variable.

        Args:
            value: The value to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if value is required
        if value is None and self.default is None:
            return False, f"Variable {self.name} is required"

        # Use default if value is None
        if value is None:
            value = self.default

        # Type validation
        try:
            # Handle nested types like List[str], Dict[str, int], etc.
            if hasattr(self.type, "__origin__"):  # For generic types like List, Dict
                origin = self.type.__origin__
                args = self.type.__args__

                if origin == list:
                    if not isinstance(value, list):
                        return False, "Value must be a list"
                    # Validate each item in the list
                    for item in value:
                        if not isinstance(item, args[0]):
                            return False, f"List items must be of type {args[0]}"

                elif origin == dict:
                    if not isinstance(value, dict):
                        return False, "Value must be a dictionary"
                    # Validate dict key and value types
                    for k, v in value.items():
                        if not isinstance(k, args[0]):
                            return False, f"Dictionary keys must be of type {args[0]}"
                        if not isinstance(v, args[1]):
                            return False, f"Dictionary values must be of type {args[1]}"
            else:
                if not isinstance(value, self.type):
                    return False, f"Value must be of type {self.type}"
        except Exception as e:
            return False, f"Type validation error: {str(e)}"

        # Custom validation
        if self.validation:
            return self.validation.validate(value)

        return True, None

    # Add descriptor methods to make it work as a proper descriptor
    def __get__(self, obj, objtype=None):
        """Get the value of this variable from the plugin instance.

        Args:
            obj: The plugin instance
            objtype: The plugin class

        Returns:
            The value of this variable
        """
        if obj is None:
            return self
        return obj._values.get(self.name, self.default)

    def __set__(self, obj, value):
        """Set the value of this variable on the plugin instance.

        Args:
            obj: The plugin instance
            value: The value to set

        Raises:
            ValueError: If the value is invalid
        """
        is_valid, error = self.validate(value)
        if not is_valid:
            raise ValueError(f"Invalid value for {self.name}: {error}")
        obj._values[self.name] = value


class Plugin(ABC):
    """Base class for all plugins."""

    name: str
    description: str
    plugin_instructions: str
    namespace: str = "local"  # Default namespace for plugins

    def __init__(self, **variables):
        """Initialize plugin with variables.

        Args:
            **variables: Variable values keyed by variable name
        """
        # Get all class attributes that are PluginVariables
        self._variables = {}
        self._values = {}

        for name, attr in inspect.getmembers(self.__class__):
            if isinstance(attr, PluginVariable):
                # Set the name if not already set
                if attr.name is None:
                    attr.name = name
                self._variables[name] = attr

        # Validate and set variables
        for name, value in variables.items():
            if name not in self._variables:
                raise ValueError(f"Unknown variable: {name}")

            var = self._variables[name]
            is_valid, error = var.validate(value)
            if not is_valid:
                raise ValueError(f"Invalid value for {name}: {error}")

            self._values[name] = value

        # Set defaults for unspecified variables
        for name, var in self._variables.items():
            if name not in self._values:
                if var.default is not None:
                    self._values[name] = var.default
                else:
                    raise ValueError(f"Required variable not provided: {name}")

        # No need to create properties for each variable anymore
        # The descriptor protocol will handle that

    @classmethod
    def get_kernel_functions(cls) -> Dict[str, Any]:
        """Get all kernel functions defined in this plugin.

        Returns:
            Dictionary of function name to function object
        """
        return {name: func for name, func in inspect.getmembers(cls) if hasattr(func, "_is_kernel_function")}
