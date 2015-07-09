from unittest import TestCase
from ..engine.settings import Settings


class TestSettings(TestCase):

    def test_getitem(self):
        settings = Settings()
        self.assertIsNotNone(settings['game']['speed'])
