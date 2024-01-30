class Invoker:
    """
    Class for invoking commands.

    Attributes:
        cmd: The command to be executed.

    Methods:
        store_command(cmd): Store a command to be executed.
        execute(): Execute the stored command.
    """
    def __init__(self):
        """
        Initializes an Invoker instance.
        """
        self.cmd = None

    def store_command(self, cmd):
        """
        Store a command to be executed.

        Parameters:
            cmd: The command to be stored.
        """
        self.cmd = cmd

    def execute(self):
        """
        Execute the stored command.
        """
        self.cmd.execute()
