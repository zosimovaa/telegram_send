import unittest
import time


from src.telegram_send.spam_filter import SpamFilter


class SpamFilterTestCase(unittest.TestCase):
    def test_threshold(self):
        threshold = 5
        control_period = 10
        silence_period = 10

        sp = SpamFilter(threshold=threshold, control_period=control_period, silence_period=silence_period)

        blocked = False
        i = 0
        while not blocked:
            blocked = sp.check_block()
            i = i + 1

        self.assertEqual(i, threshold + 1)

    def test_control_period(self):
        threshold = 3
        control_period = 4
        silence_period = 10

        sp = SpamFilter(threshold=threshold, control_period=control_period, silence_period=silence_period)

        blocked = False
        i = 0
        while i < 5:
            blocked = sp.check_block()
            i = i + 1
            time.sleep(2)
        self.assertEqual(False, blocked)

        sp = SpamFilter(threshold=threshold, control_period=control_period, silence_period=silence_period)
        blocked = False
        i = 0
        while i < 5:
            blocked = sp.check_block()
            i = i + 1
            time.sleep(1)
        self.assertEqual(True, blocked)

    def test_silence_period(self):
        threshold = 3
        control_period = 4
        silence_period = 10

        sp = SpamFilter(threshold=threshold, control_period=control_period, silence_period=silence_period)

        blocked = False
        i = 0
        while i < 5:
            blocked = sp.check_block()
            i = i + 1
            time.sleep(1)
        self.assertEqual(True, blocked)

        i = 0
        while i < 8:
            blocked = sp.check_block()
            self.assertEqual(True, blocked)
            i = i + 1
            time.sleep(1)
        time.sleep(1)
        blocked = sp.check_block()
        self.assertEqual(False, blocked)


if __name__ == '__main__':
    unittest.main()
