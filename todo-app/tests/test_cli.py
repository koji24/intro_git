import json
import tempfile
import unittest
from pathlib import Path

from todo_app.cli import run


class CliTests(unittest.TestCase):
    def test_add_list_complete_delete_and_persist(self) -> None:
        answers = iter(
            [
                "1",
                "Pythonを学ぶ",
                "高",
                "1",
                "本を読む",
                "低",
                "2",
                "3",
                "1",
                "4",
                "2",
                "2",
                "0",
            ]
        )
        messages: list[str] = []

        with tempfile.TemporaryDirectory() as directory:
            data_path = Path(directory) / "tasks.json"
            run(
                input_fn=lambda _prompt: next(answers),
                output_fn=messages.append,
                data_path=data_path,
            )

            saved_tasks = json.loads(data_path.read_text(encoding="utf-8"))

        self.assertEqual(len(saved_tasks), 1)
        self.assertEqual(saved_tasks[0]["title"], "Pythonを学ぶ")
        self.assertEqual(saved_tasks[0]["priority"], "高")
        self.assertTrue(saved_tasks[0]["completed"])
        self.assertTrue(any("[未完了] Pythonを学ぶ" in message for message in messages))
        self.assertTrue(any("[完了] Pythonを学ぶ" in message for message in messages))
        self.assertTrue(any("本を読む" in message and "削除しました" in message for message in messages))


if __name__ == "__main__":
    unittest.main()