from .Command import Command
from ..Utils import parse_parameters, default_args, log
from ..model.CurrencyPool import pool
from ..exception.ExceptionHandler import ExceptionHandler


class DefaultSubCommand(Command):
    parameters = {
        '$total': lambda **kwargs: pool.get_total(),
        '$currency': lambda **kwargs: kwargs.get('parent').GetCurrencyName(),
        '$goal': lambda **kwargs: pool.get_goal(),
        '$remaining': lambda **kwargs: pool.get_remaining()
    }

    def __init__(self, settings, parent):
        super(DefaultSubCommand, self).__init__(settings, parent)
        self.command_name = 'default'

    def handle_command(self, data, args=None):
        args = default_args(args)

        if self.should_execute_command(args, data):
            log(self.parent, ExceptionHandler.dump_data(data))
            self.parent.SendStreamMessage(parse_parameters(
                self.parameters,
                self.get_setting('Message'),
                parent=self.parent
            ))
            self.apply_cooldown()

    def should_execute_command(self, args, data):
        return not Command.has_args(args) and not self.on_cooldown() and self.has_permission(data.User, 'everyone')
