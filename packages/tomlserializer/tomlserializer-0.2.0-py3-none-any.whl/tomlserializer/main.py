import inspect
import tomllib
from pathlib import Path, PosixPath
from types import FunctionType
from typing import Any, Callable, Dict, List, Tuple, Type, TypeVar, Union

from loguru import logger

T = TypeVar("T")
ConversionFunction = Callable[[Any], Any]
TypeRegistry = Dict[Union[str, Tuple[str, ...]], ConversionFunction]


class TOMLSerializationError(Exception):
    """Custom exception for TOML serialization errors."""

    pass


class TOMLDeserializationError(Exception):
    """Custom exception for TOML deserialization errors."""

    pass


class TOMLSerializer:
    """Utility class to save and load dataclass models to/from TOML format."""

    _type_registry: Dict[str, TypeRegistry] = {
        "to_toml": {},
        "from_toml": {},
    }

    @classmethod
    def register_type(
        cls,
        type_: Union[Type[T], List[Type[T]], Tuple[Type[T], ...]],
        to_toml: ConversionFunction,
        from_toml: ConversionFunction,
    ) -> None:
        """
        Register type handlers for serialization and deserialization.

        Args:
            type_: Single type or collection of types to register
            to_toml: Function to convert type to TOML-safe format
            from_toml: Function to restore type from TOML format
        """
        if isinstance(type_, (list, tuple)):
            type_key = tuple(t.__name__ for t in type_)
        else:
            type_key = type_.__name__

        cls._type_registry["to_toml"][type_key] = to_toml
        cls._type_registry["from_toml"][type_key] = from_toml

    @classmethod
    def _convert_to_toml_safe(cls, value: Any) -> Any:
        """
        Convert a Python value to a TOML-safe format.

        Args:
            value: Value to convert

        Returns:
            TOML-safe version of the value

        Raises:
            TOMLSerializationError: If value cannot be converted
        """
        try:
            type_str = type(value).__name__

            if type_str in cls._type_registry["to_toml"]:
                return cls._type_registry["to_toml"][type_str](value)

            for type_key in cls._type_registry["to_toml"]:
                if isinstance(type_key, tuple) and type_str in type_key:
                    return cls._type_registry["to_toml"][type_key](value)

            return f'"{value}"'
        except Exception as e:
            raise TOMLSerializationError(f"Failed to convert {value} to TOML: {str(e)}")

    @classmethod
    def _convert_from_toml(cls, value: Any, original_type: str) -> Any:
        """
        Convert TOML value back to original Python type.

        Args:
            value: Value from TOML
            original_type: Expected Python type name

        Returns:
            Value converted to original type

        Raises:
            TOMLDeserializationError: If value cannot be converted
        """
        try:
            if original_type in cls._type_registry["from_toml"]:
                return cls._type_registry["from_toml"][original_type](value)

            for type_key in cls._type_registry["from_toml"]:
                if isinstance(type_key, tuple) and original_type in type_key:
                    return cls._type_registry["from_toml"][type_key](value)

            return value
        except Exception as e:
            raise TOMLDeserializationError(
                f"Failed to convert {value} from TOML: {str(e)}"
            )

    @classmethod
    def _extract_model_params(cls, model: Any) -> Dict[str, Any]:
        """
        Extract initialization parameters from a model instance.

        Args:
            model: Model instance

        Returns:
            Dictionary of parameter names and values

        Raises:
            TOMLSerializationError: If model parameters cannot be extracted
        """
        try:
            if hasattr(model, "__dict__"):
                return {
                    k: v for k, v in model.__dict__.items() if not k.startswith("_")
                }
            init_signature = inspect.signature(model.__init__)
            instance_vars = vars(model)
            return {
                name: instance_vars[name]
                for name in init_signature.parameters.keys()
                if name in instance_vars and name != "self"
            }
        except Exception as e:
            raise TOMLSerializationError(
                f"Failed to extract model parameters: {str(e)}"
            )

    @classmethod
    def save(cls, obj: Any, file_path: Union[str, Path]) -> None:
        """
        Save a dataclass model to a TOML file.

        Args:
            obj: Dataclass instance to save
            file_path: Path to save TOML file

        Raises:
            TOMLSerializationError: If save fails
        """
        file_path = Path(file_path) if isinstance(file_path, str) else file_path

        try:
            data = cls._extract_model_params(obj)
            types = {k: f'"{type(v).__name__}"' for k, v in data.items()}

            toml_string = cls._dict_to_toml("model", data, "")
            toml_string += "\n" + cls._dict_to_toml("types", types, "")

            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(toml_string)

        except Exception as e:
            raise TOMLSerializationError(f"Failed to save TOML file: {str(e)}")

    @classmethod
    def load_typed_dict(cls, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Load a dictionary from a TOML file with type conversion.

        Args:
            file_path: Path to TOML file

        Returns:
            Dictionary with converted values

        Raises:
            TOMLDeserializationError: If load fails
        """
        file_path = Path(file_path) if isinstance(file_path, str) else file_path

        try:
            if not file_path.exists():
                raise TOMLDeserializationError(f"File not found: {file_path}")

            with open(file_path, "rb") as f:
                data = tomllib.load(f)

            types = {k: v.strip('"') for k, v in data.get("types", {}).items()}
            result = {}

            for key, value in data["model"].items():
                expected_type = types.get(key, "Any")
                logger.debug(f"Converting {value} to type {expected_type}")
                result[key] = cls._convert_from_toml(value, expected_type)

            return result

        except TOMLDeserializationError:
            raise
        except Exception as e:
            raise TOMLDeserializationError(f"Failed to load TOML file: {str(e)}")

    @staticmethod
    def _dict_to_toml(name: str, data: Dict[str, Any], prefix: str = "") -> str:
        """
        Convert dictionary to TOML table format.

        Args:
            name: Table name
            data: Dictionary to convert
            prefix: Path prefix for nested tables

        Returns:
            TOML-formatted string
        """
        current_path = f"{prefix}.{name}" if prefix else name
        toml_lines = [f"[{current_path}]"]
        nested_tables = []

        for k, v in data.items():
            if isinstance(v, dict):
                nested = TOMLSerializer._dict_to_toml(k, v, current_path)
                nested_tables.append(nested)
            else:
                if name == "types":
                    v = str(v)
                else:
                    v = TOMLSerializer._convert_to_toml_safe(v)

                if isinstance(v, list):
                    v = str(v).replace("'", "")

                toml_lines.append(f"{k} = {v}")

        return "\n".join(toml_lines + nested_tables) + "\n"


def get_fun(fun_name: str) -> Union[Callable, str]:
    """
    Get function from string representation.

    Args:
        fun_name: String representation of function

    Returns:
        Function object or original string if import fails
    """
    if isinstance(fun_name, str):
        if fun_name.startswith("<") and fun_name.endswith(">"):
            fun_name = fun_name.strip("<>")

    try:
        module_path, func_name = str(fun_name).rsplit(".", 1)
        parts = module_path.split(".")

        module = __import__(parts[0])
        for part in parts[1:]:
            module = getattr(module, part)

        return getattr(module, func_name)

    except Exception as e:
        logger.error(f"Error importing {fun_name}: {e}")
        return fun_name


def fun_to_str(x: Callable) -> str:
    """Convert function to string representation."""
    return f'"<{x.__module__}.{x.__qualname__}>"'


# Register type conversions
TOMLSerializer.register_type(FunctionType, fun_to_str, get_fun)
TOMLSerializer.register_type((int, float, dict), lambda d: d, lambda d: d)
TOMLSerializer.register_type((Path, PosixPath), lambda s: f'"{s}"', Path)
TOMLSerializer.register_type(bool, lambda x: str(x).lower(), lambda x: x)
TOMLSerializer.register_type(type(None), lambda x: f'"{x}"', lambda x: None)

TOMLSerializer.register_type(
    list,
    lambda lst: [TOMLSerializer._convert_to_toml_safe(item) for item in lst],
    lambda lst: [
        TOMLSerializer._convert_from_toml(item, type(item).__name__) for item in lst
    ],
)

TOMLSerializer.register_type(
    tuple,
    lambda tpl: [TOMLSerializer._convert_to_toml_safe(item) for item in tpl],
    lambda tpl: tuple(
        TOMLSerializer._convert_from_toml(item, type(item).__name__) for item in tpl
    ),
)

TOMLSerializer.register_type(
    set,
    lambda s: [TOMLSerializer._convert_to_toml_safe(item) for item in s],
    lambda s: set(
        TOMLSerializer._convert_from_toml(item, type(item).__name__) for item in s
    ),
)


def from_str(value: str) -> Union[Callable, None, str]:
    """Convert string from TOML to appropriate type."""
    logger.debug(f"Processing string value: {value}")

    if value.startswith("<") and value.endswith(">"):
        value = value.strip("<>")
        return TOMLSerializer._convert_from_toml(value, "function")

    if value == "None":
        return None

    return value


TOMLSerializer.register_type(str, lambda s: f'"{s}"', from_str)

