""" Class responsible for """


class Invoker:
    def __init__(self):
        self.cmd = None

    def store_command(self, cmd):
        self.cmd = cmd

    def execute(self):
        self.cmd.execute()
