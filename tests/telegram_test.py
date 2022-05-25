import unittest
import time

from src.telegram_send import TelegramJustSend


class TelegramTestCase(unittest.TestCase):
    def test_send_message(self):

        chat_id = "211945135"
        alias = "TEST: TelegramJustSend"
        t = TelegramJustSend(chat_id, alias)
        t.start()
        t.send("Message from unittest")

        time.sleep(5)
        t.stop()

        self.assertEqual(True, True)  # add assertion here

if __name__ == '__main__':
    unittest.main()
