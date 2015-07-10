import time
from unittest import TestCase
from ..engine.easy_spin import *


class TestEasySpinCore(TestCase):

    def setUp(self):
        self.easy_spin = EasySpinCore({
            'easy_spin': {
                'limit': 2,
                'timeout': 2    # seconds
            }
        })

    def test_add_cycle(self):
        self.easy_spin.start()

        self.assertTrue(self.easy_spin.add_cycle())
        self.assertTrue(self.easy_spin.is_running())

        self.assertTrue(self.easy_spin.add_cycle())
        self.assertTrue(self.easy_spin.is_running())

        self.assertFalse(self.easy_spin.add_cycle())
        time.sleep(0.01)
        self.assertFalse(self.easy_spin.is_running())

    def test_reset(self):
        self.easy_spin.start()

        self.assertTrue(self.easy_spin.add_cycle())
        self.assertTrue(self.easy_spin.add_cycle())
        self.easy_spin.reset()

        self.assertTrue(self.easy_spin.add_cycle())
        self.assertTrue(self.easy_spin.add_cycle())
        self.assertFalse(self.easy_spin.add_cycle())

    def test_hard_drop(self):
        self.easy_spin.hard_drop()
        self.assertFalse(self.easy_spin.start())

    def test_starting(self):
        self.assertTrue(self.easy_spin.start())
        self.easy_spin.add_cycle()

        self.assertTrue(self.easy_spin.start())
        self.easy_spin.add_cycle()

        self.assertFalse(self.easy_spin.start())
