"""Extract information from json workflow representation."""

from typing import List

import ikclient.exceptions


class Workflow:
    """This class helps to manipulate raw json workflow."""

    def __init__(self, data: dict):
        """Initialize a new workflow.

        Args:
            data: Workflow JSON structure as Python dict
        """
        self.data = data

    @property
    def name(self) -> str:
        """Get workflow name.

        Returns:
            Workflow name
        """
        return self.data["metadata"]["name"]

    def __repr__(self) -> str:
        """Return a workflow human-readable representation.

        Returns:
            Workflow representation
        """
        pretty_task_names = ", ".join([task["task_data"]["name"] for task in self.data["tasks"]])
        return f"{self.data['metadata']['name']} ({pretty_task_names})"

    def find_task(self, task_name: str) -> List[dict]:
        """Return a list of task that match given name.

        Args:
            task_name: A task name

        Returns:
            A list of task that match name.
        """
        return [task for task in self.data["tasks"] if task["task_data"]["name"] == task_name]

    def get_task(self, task_name: str) -> dict:
        """Return a task from name or id.

        Args:
            task_name: A task name

        Returns:
            A task

        Raises:
            TaskNotFoundException: when no matching task found
            MultipleTaskFoundException: when more than one matching task found
        """
        # Find task
        tasks = self.find_task(task_name)

        # If no task found, raise an exception
        if len(tasks) == 0:
            raise ikclient.exceptions.TaskNotFoundException(self, task_name)

        # If more than one task found, raise an exception
        if len(tasks) > 1:
            raise ikclient.exceptions.MultipleTaskFoundException(self, task_name)

        # If here, only one match, return it
        return tasks.pop(0)

    def get_final_tasks(self) -> List[dict]:
        """Get all final or leaf tasks of the workflow.

        Returns:
            A list of final tasks.
        """
        # For each task, count how many times task is source of another one
        leaving_connections = {task["task_id"]: 0 for task in self.data["tasks"]}
        for connection in self.data["connections"]:
            if connection["source_id"] != -1:
                leaving_connections[connection["source_id"]] += 1

        return [task for task in self.data["tasks"] if leaving_connections[task["task_id"]] == 0]

    def get_first_final_task_name(self) -> str:
        """Return the first final task name.

        Returns:
            The first final task name.

        Raises:
            FinalTaskNotFoundException: when no final task find on workflow
            MultipleTaskFoundException: when final task name is not unique
        """
        # Get final task id list
        final_tasks = self.get_final_tasks()

        # Ensure there's one task at least
        if len(final_tasks) == 0:
            raise ikclient.exceptions.FinalTaskNotFoundException(self)

        # Get first final task name
        final_task_name = final_tasks.pop()["task_data"]["name"]

        # Ensure there's no other task with that name to avoid ambiguous call
        tasks = self.find_task(final_task_name)
        if len(tasks) > 1:
            raise ikclient.exceptions.MultipleTaskFoundException(self, final_task_name)

        # Return task name
        return final_task_name

    def get_input_types(self) -> list:
        """Return the list of inputs of the workflow (connected to root node).

        Returns:
            types (list of str)
        """
        inputs = []
        for conn in self.data["connections"]:
            if conn["source_id"] == -1:
                # Root connection
                inputs.append((conn["target_id"], conn["target_index"]))

        types = []
        for inp in inputs:
            task = self.data["tasks"][inp[0]]
            task_input = task["task_data"]["inputs"][inp[1]]
            types.append(task_input["name"])

        return types

    def get_task_output_types(self, task_name) -> list:
        """Return the list of outputs of the given task.

        If task_name is not provided, it returns the list of the first leaf task.

        Args:
            task_name (str): task name for which the output types are wanted

        Returns:
            types (list of str)
        """
        types = []

        if not task_name:
            task_name = self.get_first_final_task_name()

        for task in self.data["tasks"]:
            if task["task_data"]["name"] == task_name:
                for out in task["task_data"]["outputs"]:
                    types.append(out["name"])

        return types
