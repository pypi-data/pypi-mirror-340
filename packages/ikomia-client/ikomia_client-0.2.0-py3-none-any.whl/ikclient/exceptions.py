"""Custom lib exceptions."""

from typing import List


class IkClientBaseException(Exception):
    """Custom base exception."""

    pass


class TaskNotFoundException(IkClientBaseException):
    """When task is not found on workflow."""

    def __init__(self, workflow, task_name: str):
        """Initialize a new exception.

        Args:
            workflow: A workflow object
            task_name: Task name not found on workflow
        """
        super().__init__(f"Can't task '{task_name}' on workflow '{workflow}'")
        self.workflow = workflow
        self.task_name = task_name


class FinalTaskNotFoundException(IkClientBaseException):
    """When no final (leaf) task found on workflow."""

    def __init__(self, workflow):
        """Initialize a new exception.

        Args:
            workflow: A workflow object
        """
        super().__init__(
            f"Can't find a final task on workflow '{workflow}'. You have to specify which task you want to run."
        )


class MultipleTaskFoundException(IkClientBaseException):
    """When more than one task match a given name."""

    def __init__(self, workflow, task_name: str):
        """Initialize a new exception.

        Args:
            workflow: A workflow object
            task_name: Task name found multiple time on workflow
        """
        super().__init__(f"Found more than one task that match '{task_name}' on workflow '{workflow}'.")
        self.workflow = workflow
        self.task_name = task_name


class TaskParameterNotFoundException(IkClientBaseException):
    """When a parameter name not found on task."""

    def __init__(self, task_name: str, parameter_names: List[str], parameter_name: str):
        """Initialize a new exception.

        Args:
            task_name: Task name found multiple time on workflow
            parameter_names: A list of existing parameter names for task
            parameter_name: A mismatching parameter name
        """
        super().__init__(
            f"Parameter '{parameter_name}' not found on '{', '.join(parameter_names)}' for task '{task_name}'"
        )
        self.task_name = task_name
        self.parameter_names = parameter_names
        self.parameter_name = parameter_name


class OutputNotFoundException(IkClientBaseException):
    """When output is missing on Context."""

    def __init__(self):
        """Initialize a new exception."""
        super().__init__("Outputs information are mandatory. Please provide at least one output task name.")


class NoResultsException(IkClientBaseException):
    """When give up getting endpoint call results."""

    def __init__(self):
        """Initialize a new exception."""
        super().__init__("Can't get run call results.")


class CannotInferPathDataTypeException(IkClientBaseException):
    """When path data type cannot be inferred from the file extension or metadata."""

    def __init__(self):
        """Initialize a new exception."""
        super().__init__("Cannot infer path data type from the provided file. Please specify `data_type` explicitly.")
