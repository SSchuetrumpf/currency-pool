import calendar
import codecs
import json
import os
import time
from ..Constants import ScriptRoot


class CurrencyPool(object):
    pool = None
    api = None

    def __init__(self):
        self.storage_path = os.path.join(ScriptRoot, 'storage.json')
        self.reload()

    def reload(self):
        try:
            self.pool = self.load_json(self.storage_path)
        except IOError:
            self.pool = self.get_default()

    def save(self):
        with codecs.open(self.storage_path, encoding="utf-8-sig", mode="w+") as f:
            json.dump(self.pool, f, encoding="utf-8")

    def set_api(self, api):
        self.api = api

    def get_user_contributed(self, user):
        contributions = self.get_contributions()
        return contributions.get(str(user).lower(), 0)

    def get_total(self):
        return sum(self.get_contributions().values())

    def get_remaining(self):
        return max(self.pool.get('target', 0) - self.get_total(), 0)

    def get_goal(self):
        return self.pool.get('goal', '')

    def set_goal(self, user, goal):
        self.pool['goal'] = goal
        self.audit('GOAL', user, goal)
        self.api.refresh_overlay()
        self.save()

    def set_target(self, user, target):
        self.pool['target'] = int(target)
        self.audit('TARGET', user, target)
        self.api.refresh_overlay()
        self.save()

    def get_target(self):
        return self.pool['target']

    def add_contribution(self, user, contribution):
        """
        :param user: User making the contribution
        :type user: str
        :param contribution: Amount to contribute
        :type contribution: int
        :return:
        """
        total_user_contribution = self.get_user_contributed(user) + contribution
        self._set_contribution(user, total_user_contribution)
        self.audit('ADD', user, contribution)
        self.update_overlay(user, contribution, 'ADD')
        self.save()

    def remove_contribution(self, user, contribution):
        total_user_contribution = max(self.get_user_contributed(user) - contribution, 0)
        self._set_contribution(user, total_user_contribution)
        self.audit('REMOVE', user, contribution)
        self.update_overlay(user, contribution, 'REMOVE')
        self.save()

    def _set_contribution(self, user, contribution):
        contributions = self.get_contributions()
        contributions[str(user).lower()] = contribution
        self.pool['contributions'] = contributions

    def _delete_contribution(self, user):
        contributions = self.get_contributions()
        contributions.pop(str(user).lower())

    def transfer_contribution(self, user_from, user_to):
        new_total = self.get_user_contributed(user_from) + self.get_user_contributed(user_to)

        self._delete_contribution(user_from)
        self._set_contribution(user_to, new_total)

        self.audit('TRANSFER', user_to, user_from)
        self.save()

    def get_contributions(self):
        return self.pool.get('contributions', {})

    def audit(self, action, user, value):
        pool_history = self.pool.get('history', [])
        pool_history.append({
            "action": action,
            "value": value,
            "user": user,
            "timestamp": calendar.timegm(time.gmtime())
        })
        self.pool['history'] = pool_history

    def update_overlay(self, contributor, contribution, action):
        self.api.send_update(contributor, contribution, action)

    def goal_reached(self):
        return self.get_total() >= self.get_target()

    def clear(self, user):
        self.pool = self.get_default()
        self.audit('RESET', user, 'NOT_APPLICABLE')
        self.api.refresh_overlay()
        self.save()

    @staticmethod
    def load_json(file):
        with codecs.open(file, encoding="utf-8-sig", mode="r") as f:
            return json.load(f, encoding="utf-8")

    @staticmethod
    def get_default():
        return {
            "goal": '',
            "target": 0,
            "contributions": {},
            "history": []
        }


pool = CurrencyPool()
