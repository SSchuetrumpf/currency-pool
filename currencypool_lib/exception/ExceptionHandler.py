from .. import Constants
import json

EXCEPTION_MESSAGE = "An exception occurred on {}'s channel. Type: {}, Message: {}, Data: {}"


class ExceptionHandler(object):
    def __init__(self, parent):
        self.parent = parent
        self.author = Constants.Creator

    def handle_exception(self, exception, data=''):
        if self.should_report_exception(exception):
            self.parent.SendStreamWhisper(self.author,
                                          EXCEPTION_MESSAGE.format(
                                              self.parent.GetChannelName(),
                                              type(exception).__name__,
                                              str(exception),
                                              json.dumps(self.dump_data(data))))

    @staticmethod
    def dump_data(data):
        if type(data) is not str:
            data_dict = {}
            for field in dir(data):
                attribute = getattr(data, field)
                if callable(attribute) and field not in ['GetParam', 'GetParamCount', 'RawData'] and '__' not in field:
                    data_dict[field] = attribute()
                elif field not in ['GetParam', 'GetParamCount', 'RawData'] and '__' not in field:
                    data_dict[field] = attribute
            return data_dict
        else:
            return data

    @staticmethod
    def should_report_exception(exception):
        return exception is not OSError and exception is not IOError