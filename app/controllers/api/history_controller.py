'''
API controller for History objects.
'''
from ..enterprise.history_ec import history_ec


class HistoryController(object):

    def __init__(self):
        self.history_ec = history_ec

    def get(self) -> list:
        return self.history_ec.get()

    def add(self, url) -> None:
        self.history_ec.add(url)

    def clear(self) -> None:
        self.history_ec.clear()


history_controller = HistoryController()
