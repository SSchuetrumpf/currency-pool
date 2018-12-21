from .Command import Command
from ..Utils import parse_parameters, tail, default_args
from ..model.CurrencyPool import pool


class TargetSubCommand(Command):
    parameters = {
        '$currency': lambda **kwargs: kwargs.get('parent').GetCurrencyName(),
        '$user': lambda **kwargs: kwargs.get('user'),
        '$target': lambda **kwargs: kwargs.get('target')
    }

    def __init__(self, settings, parent):
        super(TargetSubCommand, self).__init__(settings, parent)
        self.command_name = self.setting_group = 'target'

    def handle_command(self, data, args=None):
        args = default_args(args)

        if self.should_execute_command(args, data):
            args = tail(args)
            target = int(args[0])
            pool.set_target(data.User, target)
            self.parent.SendStreamMessage(parse_parameters(
                self.parameters,
                self.get_setting("Success"),
                user=data.User,
                target=target,
                parent=self.parent
            ))
            self.apply_cooldown()

    def should_execute_command(self, args, data):
        return Command.has_args(args) and self.matches_command(args[0]) and not self.on_cooldown() and \
               self.has_permission(data.User, 'editor')

