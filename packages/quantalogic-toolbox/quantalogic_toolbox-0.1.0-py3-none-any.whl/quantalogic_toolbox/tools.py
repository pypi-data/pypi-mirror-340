import inspect
import typing
from dataclasses import dataclass
from typing import Callable, List, Optional, get_type_hints

from docstring_parser import Docstring, parse


@dataclass
class ToolArgument:
    """Represents a tool argument's metadata."""
    name: str
    arg_type: str
    description: str
    required: bool = True
    default_value: str = ""
    type_details: dict = None

@dataclass
class ToolMetadata:
    """Comprehensive metadata for a tool."""
    name: str
    description: str
    long_description: str
    arguments: List[ToolArgument]
    return_type: str
    return_type_details: dict
    examples: List[str]
    notes: List[str]
    category: str
    tags: List[str]

def tool_definer(
    name: Optional[str] = None,
    description: Optional[str] = None,
    arguments: Optional[List[ToolArgument]] = None,
    return_type: Optional[str] = None,
    category: str = "Uncategorized",
    tags: Optional[List[str]] = None
) -> Callable:
    """
    A standalone decorator to define tools with enhanced automatic metadata inference.

    Args:
        name: Custom name for the tool (defaults to function name).
        description: Tool description (defaults to docstring short description).
        arguments: List of ToolArgument objects (defaults to inferred from signature and docstring).
        return_type: Expected return type (defaults to inferred from return annotation).
        category: Category or group this tool belongs to.
        tags: List of tags for organizing and filtering tools.

    Returns:
        Callable: The decorated function with attached metadata.
    """
    def decorator(func: Callable) -> Callable:
        # Get function signature
        sig = inspect.signature(func)
        
        # Get detailed type hints
        type_hints = get_type_hints(func)
        
        # Parse docstring
        doc: Docstring = parse(func.__doc__ or "")
        
        # Name: Use provided name or function name
        tool_name = name or func.__name__
        
        # Description: Use provided description or docstring short description
        tool_description = description or doc.short_description or ""
        tool_long_description = doc.long_description or ""
        
        # Initialize arguments list
        tool_arguments = arguments if arguments is not None else []
        
        def get_type_details(type_hint):
            """Extract detailed information about a type hint."""
            if type_hint is None:
                return {}
            details = {}
            origin_type = typing.get_origin(type_hint)
            type_args = typing.get_args(type_hint)
            
            if origin_type:
                details['origin'] = str(origin_type)
                if type_args:
                    details['args'] = [str(arg) for arg in type_args]
            else:
                details['type'] = str(type_hint)
            return details
        
        # Arguments: Use provided arguments or infer from signature and docstring
        if not tool_arguments:
            param_descriptions = {p.arg_name: p.description for p in doc.params}
            for param_name, param in sig.parameters.items():
                arg_type = "Any"
                type_details = {}
                if param_name in type_hints:
                    arg_type = str(type_hints[param_name])
                    type_details = get_type_details(type_hints[param_name])
                required = param.default == inspect.Parameter.empty
                default_val = str(param.default) if param.default != inspect.Parameter.empty else ""
                arg_desc = param_descriptions.get(param_name, "")
                tool_arguments.append(ToolArgument(
                    name=param_name,
                    arg_type=arg_type,
                    description=arg_desc,
                    required=required,
                    default_value=default_val,
                    type_details=type_details
                ))
        
        # Return type: Use provided return_type or infer from annotation
        tool_return_type = return_type
        return_type_details = {}
        if tool_return_type is None:
            if 'return' in type_hints:
                tool_return_type = str(type_hints['return'])
                return_type_details = get_type_details(type_hints['return'])
            else:
                tool_return_type = "Any"
        else:
            # If return type is provided manually, we don't have access to the actual type object
            return_type_details = {'type': tool_return_type}
        
        # Extract examples and notes from docstring
        tool_examples = []
        tool_notes = []
        for meta in doc.meta:
            if meta.args and meta.args[0].lower() in ['example', 'examples']:
                tool_examples.append(meta.description)
            elif meta.args and meta.args[0].lower() in ['note', 'notes']:
                tool_notes.append(meta.description)
        
        # Set tags
        tool_tags = tags if tags is not None else []
        
        # Create comprehensive metadata
        metadata = ToolMetadata(
            name=tool_name,
            description=tool_description,
            long_description=tool_long_description,
            arguments=tool_arguments,
            return_type=tool_return_type,
            return_type_details=return_type_details,
            examples=tool_examples,
            notes=tool_notes,
            category=category,
            tags=tool_tags
        )
        
        # Attach metadata to the function
        func._tool_metadata = metadata
        
        return func
    return decorator


if __name__ == "__main__":
    from typing import List

    @tool_definer(
        category="Math Operations",
        tags=["math", "calculation"]
    )
    def calculate_average(numbers: List[float], precision: int = 2) -> float:
        """
        Calculate the average of a list of numbers with specified precision.

        Args:
            numbers: List of numbers to average.
            precision: Number of decimal places for the result.

        Returns:
            float: The average value rounded to specified precision.

        Examples:
            >>> calculate_average([1.0, 2.0, 3.0])
            2.0
            >>> calculate_average([1.234, 5.678, 9.012], 1)
            5.3

        Notes:
            - Returns 0.0 if the input list is empty.
        """
        if not numbers:
            return 0.0
        return round(sum(numbers) / len(numbers), precision)

    # Access and print metadata for demonstration
    metadata = calculate_average._tool_metadata
    print("Tool Metadata Example:")
    print(f"Name: {metadata.name}")
    print(f"Description: {metadata.description}")
    print(f"Category: {metadata.category}")
    print(f"Tags: {', '.join(metadata.tags)}")
    print("Arguments:")
    for arg in metadata.arguments:
        print(f"  - {arg.name}: {arg.arg_type}")
        if arg.type_details:
            print(f"    Details: {arg.type_details}")
        if arg.description:
            print(f"    Description: {arg.description}")
    print(f"Return Type: {metadata.return_type}")
    if metadata.return_type_details:
        print(f"Return Type Details: {metadata.return_type_details}")
    if metadata.examples:
        print("Examples:")
        for example in metadata.examples:
            print(f"  - {example}")
    if metadata.notes:
        print("Notes:")
        for note in metadata.notes:
            print(f"  - {note}")