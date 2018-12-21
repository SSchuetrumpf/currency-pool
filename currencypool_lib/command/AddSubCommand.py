import re as regex

from .Command import Command
from ..Utils import parse_parameters, default_args
from ..model.CurrencyPool import pool


def get_value(args):
    # Should match examples
    # !pool add 123
    # !pool 123
    return int(args[0] if len(args) == 1 else args[1])


class AddSubCommand(Command):
    parameters = {
        '$currency': lambda **kwargs: kwargs.get('parent').GetCurrencyName(),
        '$user': lambda **kwargs: kwargs.get('user'),
        '$contribution': lambda **kwargs: kwargs.get('contribution'),
        '$total_contribution': lambda **kwargs: pool.get_user_contributed(kwargs.get('user')),
        '$currency_available': lambda **kwargs: kwargs.get('parent').GetPoints(kwargs.get('user'))
    }

    def __init__(self, settings, parent):
        super(AddSubCommand, self).__init__(settings, parent)
        self.command_name = self.setting_group = 'add'

    def handle_command(self, data, args=None):
        args = default_args(args)

        if self.should_execute_command(args, data):
            contribution = get_value(args)
            if self.check_user_has_currency(args, data.User):
                contribution = get_value(args)
                if contribution > 0 and not self.get_setting('Generous'):
                    pool_reached = pool.goal_reached()
                    if not pool_reached:
                        contribution = min(pool.get_target() - pool.get_total(), contribution)
                        self.do_contribution(contribution, data)
                    self.parent.SendStreamMessage(parse_parameters(
                        self.parameters,
                        self.get_setting('Success') if not pool_reached else self.get_setting('GenerousMessage'),
                        parent=self.parent,
                        user=data.UserName,
                        contribution=contribution
                    ))
                elif contribution > 0:
                    self.do_contribution(contribution, data)
                    self.parent.SendStreamMessage(parse_parameters(
                        self.parameters,
                        self.get_setting('Success'),
                        parent=self.parent,
                        user=data.UserName,
                        contribution=contribution
                    ))
            else:
                self.parent.SendStreamMessage(parse_parameters(
                    self.parameters,
                    self.get_setting("Failure"),
                    parent=self.parent,
                    user=data.UserName,
                    contribution=contribution
                ))
            self.apply_cooldown(data.User)

    def do_contribution(self, contribution, data):
        pool.add_contribution(data.UserName, contribution)
        self.parent.RemovePoints(data.User, data.UserName, contribution)

    def should_execute_command(self, args, data):
        return self.has_args(args) and \
               (self.matches_command(args[0]) or
                regex.match('\\d+', str(args[0]))) and \
               not self.on_cooldown(data.User) and self.enabled() and self.has_permission(data.User, 'everyone')

    def check_user_has_currency(self, args, user):
        # Should match examples
        # !pool add 123
        # !pool 123
        contribution = get_value(args)
        return self.parent.GetPoints(user) >= contribution
