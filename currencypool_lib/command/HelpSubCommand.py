from .Command import Command
from ..Utils import default_args


class HelpSubCommand(Command):
    def __init__(self, settings, parent):
        super(HelpSubCommand, self).__init__(settings, parent)
        self.command_name = self.setting_group = 'help'
        self.command_aliases = (
            'help'
        )

    def handle_command(self, data, args=None):
        args = default_args(args)

        if self.should_execute_command(args, data):
            self.do_help()

    def do_help(self):
        self.parent.SendStreamMessage('Test help message')

    def should_execute_command(self, args, data):
        return Command.has_args(args) and self.matches_command(args[0])
