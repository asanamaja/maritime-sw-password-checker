import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.checker import evaluate, suggest_password


class PasswordCheckerTest(unittest.TestCase):
    def test_weak_short_lowercase(self) -> None:
        result = evaluate("abc")
        self.assertEqual(result["grade"], "취약")
        self.assertEqual(result["score"], 0)

    def test_weak_length_only(self) -> None:
        result = evaluate("abcdefgh")
        self.assertEqual(result["grade"], "취약")
        self.assertEqual(result["score"], 1)

    def test_medium_lecture_example(self) -> None:
        result = evaluate("Pass12!")
        self.assertEqual(result["length"], 7)
        self.assertFalse(result["length_ok"])
        self.assertTrue(result["has_upper"])
        self.assertTrue(result["has_lower"])
        self.assertTrue(result["has_digit"])
        self.assertTrue(result["has_special"])
        self.assertEqual(result["score"], 3)
        self.assertEqual(result["grade"], "보통")

    def test_strong_password(self) -> None:
        result = evaluate("Abcd1234!")
        self.assertEqual(result["score"], 4)
        self.assertEqual(result["grade"], "강력")

    def test_suggestion_is_strong(self) -> None:
        for _ in range(20):
            password = suggest_password()
            result = evaluate(password)
            self.assertGreaterEqual(len(password), 8)
            self.assertEqual(result["grade"], "강력")


if __name__ == "__main__":
    unittest.main()
