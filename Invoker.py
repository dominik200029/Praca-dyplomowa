class Invoker:
    """
    Invoker class responsible for storing and executing commands.

    Attributes:
        commands (list): A list to store commands.

    Methods:
        store_commands: Store one or more commands in the list of commands.
        execute: Execute all stored commands.
    """

    def __init__(self):
        """
        Initialize an Invoker instance with an empty list of commands.
        """
        self.commands = []

    def store_commands(self, *commands):
        """
        Store one or more commands in the list of commands.

        Parameters:
            *commands: Variable number of command objects to be stored.

        Returns:
            None
        """
        for command in commands:
            self.commands.append(command)

    def execute(self):
        """
        Execute all stored commands.

        Returns:
            None
        """
        for command in self.commands:
            command.execute()
