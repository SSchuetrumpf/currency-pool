from abc import ABCMeta, abstractmethod
from .. import Constants
from ..Utils import log


class Command(object):
    __metaclass__ = ABCMeta

    def __init__(self, settings, parent):
        self.settings = settings
        self.parent = parent
        self.command_name = '!pool'
        self.setting_group = 'Core'

    @abstractmethod
    def handle_command(self, data):
        pass

    @abstractmethod
    def should_execute_command(self, args, data):
        return str(args[0]).lower() == self.command_name

    @staticmethod
    def parse_args(data):
        return [data.GetParam(i) for i in range(0, data.GetParamCount())]

    def get_setting(self, setting_name, default=''):
        return self.settings.get(self.setting_group + setting_name, default)
    
    def get_aliases(self):
        aliases = self.get_setting('Aliases').split(',')
        aliases.append(self.command_name)
        return aliases

    def matches_command(self, arg):
        return str(arg).lower() in self.get_aliases()

    @staticmethod
    def has_args(args, minimum_args=1):
        return len(args) > minimum_args - 1

    def apply_cooldown(self, user=None):
        if user is not None:
            self.parent.AddUserCooldown(Constants.ScriptName, self.command_name, str(user), self.get_setting('Cooldown'))
        else:
            self.parent.AddCooldown(Constants.ScriptName, self.command_name, self.get_setting('Cooldown'))

    def on_cooldown(self, user=None):
        if user is not None:
            return self.parent.IsOnUserCooldown(Constants.ScriptName, self.command_name, str(user))
        else:
            return self.parent.IsOnCooldown(Constants.ScriptName, self.command_name)

    def enabled(self):
        return self.get_setting("Enabled")

    def has_permission(self, user, default_permission):
        return self.parent.HasPermission(user, self.get_setting('Permission', default_permission), '')
