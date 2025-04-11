"""Deployment endpoint call context."""

from typing import Dict, List, Optional, Union

import ikclient.exceptions
from ikclient.core.workflow import Workflow


class Context:
    """Object to manage endpoint call context."""

    def __init__(self, workflow: Workflow):
        """Initialize a new context.

        Args:
            workflow: A workflow object from endpoint
        """
        self.workflow = workflow

        self._parameters: Dict[str, dict] = {}
        self._outputs: List[dict] = []

    def set_parameters(self, task_name: str, parameters: dict[str, object]):
        """Set workflow parameters.

        Args:
            task_name: A task name
            parameters: parameters values for given task

        Raises:
            TaskParameterNotFoundException: when a parameter name not found on workflow task
        """
        # Get task from workflow
        task = self.workflow.get_task(task_name)

        # Ensure parameters fit task
        task_parameter_names = [parameter["name"] for parameter in task["task_data"]["parameters"]]
        for name in parameters:
            if name not in task_parameter_names:
                raise ikclient.exceptions.TaskParameterNotFoundException(task_name, task_parameter_names, name)

        # Store parameters by task name, ensure parameter values are all str
        self._parameters[task_name] = {k: str(v) for k, v in parameters.items()}

    def add_output(self, task_name: str, index: Optional[int] = None, save_temporary: bool = False):
        """Add wanted outputs to be returned by the endpoint call.

        Args:
            task_name: A task name
            index: zero-based index of the wanted output among all task outputs
            save_temporary: Whether to save the output as a temporary object
        """
        # Get task from workflow to ensure name is unique
        _ = self.workflow.get_task(task_name)

        # Craft output data
        data: Dict[str, Union[str, int]] = {"task_name": task_name}
        if index is not None:
            data["output_index"] = index

        if save_temporary:
            data["save_temporary"] = save_temporary

        # Append it to output list if not already done
        try:
            self._outputs.index(data)
        except ValueError:
            self._outputs.append(data)

    def payload(self, inputs: List[dict]) -> dict:
        """Get request payload.

        Args:
            inputs: A list of endpoint call input.

        Returns:
            A payload as dict

        Raises:
            OutputNotFoundException: when no output was defined
        """
        # Ensure output where defined
        if len(self._outputs) == 0:
            raise ikclient.exceptions.OutputNotFoundException()

        # Transform internal parameters to workflow expected format
        parameters = [
            {"task_name": task_name, "parameters": parameters} for task_name, parameters in self._parameters.items()
        ]

        # Return payload
        return {
            "inputs": inputs,
            "outputs": self._outputs.copy(),
            "parameters": parameters,
        }
