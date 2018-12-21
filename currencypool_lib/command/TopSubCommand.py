import re as regex

from .Command import Command
from ..Utils import parse_parameters, default_args
from ..model.CurrencyPool import pool


class TopSubCommand(Command):
    parameters = {
        '$top': lambda **kwargs: ", ".join(["{} ({})".format(n, pool.get_user_contributed(n)) for n in kwargs.get('top', [])]),
        '$currency': lambda **kwargs: kwargs.get('parent').GetCurrencyName()
    }

    def __init__(self, settings, parent):
        super(TopSubCommand, self).__init__(settings, parent)
        self.command_name = self.setting_group = 'top'

    def handle_command(self, data, args=None):
        args = default_args(args)
        if self.should_execute_command(args, data):
            top = self.get_number(args)
            contributions = {k: v for k, v in pool.get_contributions().items() if v > 0}
            sorted_contributors = sorted(contributions, key=contributions.get, reverse=True)
            top_contributors = sorted_contributors[0:top]
            self.parent.SendStreamMessage(parse_parameters(
                self.parameters,
                self.get_setting("Message"),
                parent=self.parent,
                top=top_contributors,
                contributions=contributions))
            self.apply_cooldown()

    def should_execute_command(self, args, data):
        return Command.has_args(args) and self.matches_command(args[0]) and \
               not self.on_cooldown() and self.has_permission(data.User, 'everyone')

    def get_number(self, args):
        val = args[1] if len(args) > 1 else self.settings.get('Default', '3')
        val = int(val) if regex.match('\\d+', str(val)) else self.settings.get('Default', '3')
        return val
