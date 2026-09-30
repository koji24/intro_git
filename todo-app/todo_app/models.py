from dataclasses import dataclass


PRIORITIES = ("高", "中", "低")


@dataclass
class Task:
    id: int
    title: str
    priority: str
    completed: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.id, int) or self.id < 1:
            raise ValueError("タスクIDが不正です。")
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("タスク名を入力してください。")
        if self.priority not in PRIORITIES:
            raise ValueError("優先度は「高」「中」「低」から選択してください。")
        if not isinstance(self.completed, bool):
            raise ValueError("完了状態が不正です。")

    @classmethod
    def from_dict(cls, value: object) -> "Task":
        if not isinstance(value, dict):
            raise ValueError("タスクデータの形式が不正です。")
        try:
            return cls(
                id=value["id"],
                title=value["title"],
                priority=value["priority"],
                completed=value.get("completed", False),
            )
        except KeyError as error:
            raise ValueError("タスクデータに必須項目がありません。") from error