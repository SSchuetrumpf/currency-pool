from .Command import Command
from ..Utils import tail, parse_parameters, default_args
from ..model.CurrencyPool import pool


class GoalSubCommand(Command):
    parameters = {
        '$user': lambda **kwargs: kwargs.get('user'),
        '$goal': lambda **kwargs: kwargs.get('goal'),
        '$currency': lambda **kwargs: kwargs.get('parent').GetCurrencyName()
    }

    def __init__(self, settings, parent):
        super(GoalSubCommand, self).__init__(settings, parent)
        self.command_name = self.setting_group = 'goal'

    def handle_command(self, data, args=None):
        args = default_args(args)

        if self.should_execute_command(args, data):
            args = tail(args)
            if len(args) > 0:
                if self.get_setting("Clear", False):
                    pool.clear(data.User)
                goal_string = " ".join(args)
                pool.set_goal(data.User, goal_string)
                self.parent.SendStreamMessage(parse_parameters(
                    self.parameters,
                    self.get_setting('Success'),
                    parent=self.parent,
                    goal=goal_string,
                    user=data.User
                ))
                self.apply_cooldown()

    def should_execute_command(self, args, data):
        return Command.has_args(args) and self.matches_command(args[0]) \
               and self.has_permission(data.User, 'editor') \
               and not self.on_cooldown()
