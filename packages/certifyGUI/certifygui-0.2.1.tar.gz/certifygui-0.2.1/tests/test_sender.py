import unittest
from easyemail.sender import send_email

class TestEmailSender(unittest.TestCase):
    def test_send_email(self):
        result = send_email("muthukumaran@gamil.com", "Millionaire$1", "muthukumarandev001@gmail.com", "Test", "Hello!")
        self.assertIn("Email sent", result)

if __name__ == "__main__":
    unittest.main()
