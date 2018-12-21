from .Command import Command
from ..Utils import default_args, parse_parameters, log
from ..model.CurrencyPool import pool
from threading import Timer


class CommitSubCommand(Command):
    parameters = {
        '$user': lambda **kwargs: kwargs.get('user'),
    }

    def __init__(self, settings, parent):
        super(CommitSubCommand, self).__init__(settings, parent)
        self.command_name = self.setting_group = 'commit'
        self.confirmation = False
        self.confirmationTimer = None

    def handle_command(self, data, args=None):
        args = default_args(args)

        if self.should_execute_command(args, data):
            if self.confirmation:
                pool.clear(data.User)
                self.parent.SendStreamMessage(parse_parameters(
                    self.parameters,
                    self.get_setting('Success'),
                    user=data.User
                ))
                if self.confirmationTimer:
                    self.confirmationTimer.cancel()
                self.confirmation = False
                self.apply_cooldown()
            else:
                self.confirmationTimer = Timer(int(self.get_setting('Cooldown')), self.timeout)
                self.confirmationTimer.start()
                log(self.parent, 'Awaiting confirmation')
                self.confirmation = True
                self.parent.SendStreamMessage(parse_parameters(
                    self.parameters,
                    self.get_setting('Confirmation'),
                    user=data.User
                ))

    def should_execute_command(self, args, data):
        return self.has_args(args) and \
               self.matches_command(args[0]) and \
               self.enabled() and \
               not self.on_cooldown() and self.has_permission(data.User, 'editor')

    def timeout(self):
        self.confirmation = False
        log(self.parent, 'Confirmation timed out')
