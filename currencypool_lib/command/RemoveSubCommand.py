import re as regex

from .Command import Command
from ..Utils import tail, parse_parameters, default_args
from ..model.CurrencyPool import pool


def get_number(arg):
    return int(arg) if regex.match('\\d+', arg) else 0


def check_user_contributed_currency(contribution, user):
    contributed = pool.get_user_contributed(user)
    return contributed >= contribution


class RemoveSubCommand(Command):
    parameters = {
        '$contribution': lambda **kwargs: kwargs.get('contribution', 0),
        '$total_contribution': lambda **kwargs: pool.get_user_contributed(kwargs.get('target', kwargs.get('user'))),
        '$user': lambda **kwargs: kwargs.get('user'),
        '$target': lambda **kwargs: kwargs.get('target', 'None'),
        '$currency': lambda **kwargs: kwargs.get('parent').GetCurrencyName()
    }

    def __init__(self, settings, parent):
        super(RemoveSubCommand, self).__init__(settings, parent)
        self.command_name = self.setting_group = 'remove'

    def handle_command(self, data, args=None):
        args = default_args(args)

        if self.should_execute_command(args, data):
            args = tail(args)
            if regex.match('\\d+', args[0]):
                contribution = get_number(args[0])
                if check_user_contributed_currency(contribution, data.User):
                    self.remove_contribution_from_user(data.User, get_number(args[0]))
                    self.parent.SendStreamMessage(parse_parameters(
                        self.parameters,
                        self.get_setting("SelfSuccess"),
                        parent=self.parent,
                        user=data.User,
                        contribution=contribution
                    ))
                else:
                    self.parent.SendStreamMessage(parse_parameters(
                        self.parameters,
                        self.get_setting("SelfFailure"),
                        parent=self.parent,
                        user=data.User,
                        contribution=contribution
                    ))
            elif self.has_permission(data.User, 'editor') and self.get_setting('ModeratorOnly', False):
                target = args[0]
                contribution = get_number(args[1])
                if check_user_contributed_currency(contribution, target):
                    self.remove_contribution_from_user(target, contribution)
                    self.parent.SendStreamMessage(parse_parameters(
                        self.parameters,
                        self.get_setting("OtherSuccess"),
                        parent=self.parent,
                        user=data.User,
                        target=target,
                        contribution=contribution
                    ))
                else:
                    self.parent.SendStreamMessage(parse_parameters(
                        self.parameters,
                        self.get_setting("OtherFailure"),
                        parent=self.parent,
                        user=data.User,
                        target=target,
                        contribution=contribution
                    ))
            self.apply_cooldown(data.User)

    def remove_contribution_from_user(self, user, contribution):
        pool.remove_contribution(user, contribution)
        self.parent.AddPoints(user, contribution)

    def should_execute_command(self, args, data):
        return Command.has_args(args) and self.matches_command(args[0]) and not self.on_cooldown(
            data.User) and self.has_permission(data.User, 'everyone')
