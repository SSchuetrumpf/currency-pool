from .AddSubCommand import AddSubCommand
from .Command import Command
from .CommitSubCommand import CommitSubCommand
from .DefaultSubCommand import DefaultSubCommand
from .GoalSubCommand import GoalSubCommand
from .HelpSubCommand import HelpSubCommand
from .RemoveSubCommand import RemoveSubCommand
from .TargetSubCommand import TargetSubCommand
from .TopSubCommand import TopSubCommand
from .TransferSubCommand import TransferSubCommand
from ..Utils import tail

sub_commands = [
    AddSubCommand,
    DefaultSubCommand,
    RemoveSubCommand,
    TopSubCommand,
    GoalSubCommand,
    TransferSubCommand,
    TargetSubCommand,
    HelpSubCommand,
    CommitSubCommand
]


class CurrencyPoolCommand(Command):
    def __init__(self, settings, parent):
        super(CurrencyPoolCommand, self).__init__(settings, parent)
        self.sub_commands = [sub_command(settings, parent) for sub_command in sub_commands]

    def handle_command(self, data):
        args = self.parse_args(data)

        if self.should_execute_command(args, data):
            args = tail(args)
            [c.handle_command(data, args) for c in self.sub_commands]

    def should_execute_command(self, args, data):
        return super(CurrencyPoolCommand, self).should_execute_command(args, data) \
           and data.IsFromTwitch()
