import json

CONFIG = {
    'donation-goal': 'donation_goal',
    'follower-goal': 'follower_goal',
    'bit-goal': 'bit_goal',
    'sub-goal': 'sub_goal'
}


class StreamlabsApi(object):
    parent = None

    def __init__(self, settings, parent):
        self.parent = parent
        self.settings = settings

    def get_donation_goal_config(self, api_key):
        overlay_style = self.settings.get('OverlayStyle', 'donation-goal')
        request_url = "https://streamlabs.com/api/v5/widget/config?token={}&profile=NaN&widget={}".format(api_key, CONFIG[overlay_style])
        return json.loads(self.parent.GetRequest(request_url, self.get_widget_headers(api_key, overlay_style))).get('response')

    @staticmethod
    def get_widget_headers(api_key, widget):
        return {
            'Referer': 'https://streamlabs.com/widgets/{}?token={}'.format(widget, api_key)
        }
