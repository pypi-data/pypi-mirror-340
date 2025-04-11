"""Endpoint call results."""

from typing import Generator, Optional, Type, TypeVar, overload

from ikclient.core.io import BaseTaskIO, ImageIO, StorageObjectIO, TaskIO

T = TypeVar("T", bound=BaseTaskIO)


class Results:
    """To easily manage endpoint call results."""

    IO_TYPE_MAPPING = {
        "storage_object": StorageObjectIO,
        "image": ImageIO,
    }

    def __init__(self, uuid: str, inputs: list[dict], outputs: list[dict]):
        """Initialize a new Results object.

        Args:
            uuid: Deployment run call UUID
            inputs: Raw run inputs
            outputs: Raw run outputs
        """
        self.uuid = uuid
        self._inputs = inputs
        self._outputs = outputs

    def __len__(self) -> int:
        """Get results output length.

        Returns:
            Output length
        """
        return len(self._outputs)

    def __repr__(self):
        """Get string representation of the Results object.

        Returns:
            String representation of the Results object
        """
        return (
            f"Results(uuid={self.uuid}, "
            f"inputs=[{', '.join([inp.__class__.__name__ for inp in self.get_inputs()])}], "
            f"outputs=[{', '.join([out.__class__.__name__ for out in self.get_outputs()])}]"
        )

    @overload
    def get_output(self, index=0, *, assert_type: Type[T]) -> T: ...

    @overload
    def get_output(self, index=0, *, assert_type: None = None) -> BaseTaskIO: ...

    def get_output(self, index=0, *, assert_type: Optional[Type[T]] = None) -> T:
        """Get a well formatted output.

        Args:
            index: Output index. Default to 0.
            assert_type: Optional type assertion for the output type.

        Raises:
            ValueError: When the provided assert_type does not match the output type.

        Returns:
            A BaseTaskIO object containing the output data.
        """
        output_type = next(iter(self._outputs[index].keys()))

        output_class = self.IO_TYPE_MAPPING.get(output_type, TaskIO)

        if assert_type is not None:
            if not issubclass(output_class, assert_type):
                assert_type_name = getattr(assert_type, "__name__", str(assert_type))
                output_class_name = getattr(output_class, "__name__", str(output_class))
                raise ValueError(f"Output type mismatch: expected {assert_type_name}, got {output_class_name}")

        return output_class(self._outputs[index])

    def get_outputs(self) -> Generator[BaseTaskIO, None, None]:
        """Get all results outputs.

        Yields:
            Formatted output as BaseTaskIOs
        """
        for index in range(len(self)):
            yield self.get_output(index)

    # To get Results output, pythonic way
    __iter__ = get_outputs

    @overload
    def get_input(self, index=0, *, assert_type: Type[T]) -> T: ...

    @overload
    def get_input(self, index=0, *, assert_type: None = None) -> BaseTaskIO: ...

    def get_input(self, index=0, *, assert_type: Optional[Type[T]] = None) -> T:
        """Get a well formatted input.

        Args:
            index: Input index. Default to 0.
            assert_type: Optional type assertion for the input type.

        Raises:
            ValueError: When the provided assert_type does not match the input type.

        Returns:
            A BaseTaskIO object containing the input data.
        """
        input_type = next(iter(self._inputs[index].keys()))

        input_class = self.IO_TYPE_MAPPING.get(input_type, TaskIO)

        if assert_type is not None:
            if not issubclass(input_class, assert_type):
                assert_type_name = getattr(assert_type, "__name__", str(assert_type))
                input_class_name = getattr(input_class, "__name__", str(input_class))
                raise ValueError(f"Input type mismatch: expected {assert_type_name}, got {input_class_name}")

        return input_class(self._inputs[index])

    def get_inputs(self) -> Generator[BaseTaskIO, None, None]:
        """Get all results inputs.

        Yields:
            Formatted input as BaseTaskIOs
        """
        for index in range(len(self._inputs)):
            yield self.get_input(index)
