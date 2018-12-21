import json

from ..model.CurrencyPool import pool
from ..api.StreamlabsApi import StreamlabsApi

EVENTS = {
    'REFRESH': 'EVENT_POOL_REFRESH',
    'DONATION': 'EVENT_POOL_DONATION'
}

settings_fields = (
    "background_color",
    "bar_color",
    "bar_bg_color",
    "text_color",
    "bar_text_color",
    "font",
    "bar_thickness",
    "custom_enabled",
    "custom_html",
    "custom_css",
    "custom_js",
    "custom_json",
    "layout",
    "whitelist"
)


class OverlayApi(object):
    def __init__(self, settings, parent):
        self.parent = parent
        self.settings = settings
        self.streamlabs = StreamlabsApi(settings, parent)

    def refresh_overlay(self):
        self.parent.BroadcastWsEvent(EVENTS['REFRESH'], json.dumps(self.append_streamlabs_config(self.get_pool_data())))

    def send_update(self, contributor, contribution, action):
        data = self.get_pool_data()
        data['contributor'] = contributor
        data['contribution'] = contribution
        data['action'] = action

        self.parent.BroadcastWsEvent(EVENTS['DONATION'], json.dumps(data))

    def get_pool_data(self):
        data = {
            'progress': {
                'total': pool.get_total(),
                'goal': pool.get_goal(),
                'target': pool.get_target(),
                'percentage': 0 if pool.get_target() == 0 else round((float(pool.get_total()) / pool.get_target()) * 100, 2),
                'currency_name': self.parent.GetCurrencyName()
            }
        }

        return data

    def append_streamlabs_config(self, data):
        overlay_token = self.settings.get('OverlayApiToken', '')
        settings = {}
        if overlay_token:
            streamlabs_config = json.loads(self.streamlabs.get_donation_goal_config(overlay_token)).get('settings')
            for key in settings_fields:
                settings[key] = streamlabs_config.get(key)
        data['settings'] = settings
        return data
