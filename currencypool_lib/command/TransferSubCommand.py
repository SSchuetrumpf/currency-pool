from .Command import Command
from ..Utils import parse_parameters, default_args
from ..model.CurrencyPool import pool


class TransferSubCommand(Command):
    parameters = {
        '$user': lambda **kwargs: kwargs.get('user'),
        '$from': lambda **kwargs: kwargs.get('user_from'),
        '$to': lambda **kwargs: kwargs.get('user_to'),
        '$amount': lambda **kwargs: kwargs.get('amount'),
        '$currency': lambda **kwargs: kwargs.get('parent').GetCurrencyName(),
    }

    def __init__(self, settings, parent):
        super(TransferSubCommand, self).__init__(settings, parent)
        self.command_name = self.setting_group = 'transfer'

    def handle_command(self, data, args=None):
        args = default_args(args)

        if self.should_execute_command(args, data):
            user_from = args[0]
            user_to = args[1]
            amount = pool.get_user_contributed(user_from)
            pool.transfer_contribution(user_from, user_to)
            self.parent.SendStreamMessage(parse_parameters(
                self.parameters,
                self.get_setting('Message'),
                parent=self.parent,
                user=data.User,
                user_from=user_from,
                user_to=user_to,
                amount=amount
            ))

    def should_execute_command(self, args, data):
        return Command.has_args(args) and self.matches_command(args[0]) \
               and self.has_permission(data.User, 'editor')
