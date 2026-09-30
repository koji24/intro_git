import json
import os
from dataclasses import asdict
from pathlib import Path

from .models import Task


def get_data_path() -> Path:
    configured_path = os.environ.get("TODO_APP_DATA")
    if configured_path:
        return Path(configured_path).expanduser()
    return Path.home() / ".todo-app" / "tasks.json"


def load_tasks(path: str | Path | None = None) -> list[Task]:
    data_path = Path(path) if path is not None else get_data_path()
    if not data_path.exists():
        return []

    try:
        raw_tasks = json.loads(data_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError("タスクデータのJSON形式が不正です。") from error

    if not isinstance(raw_tasks, list):
        raise ValueError("タスクデータはリスト形式である必要があります。")
    try:
        return [Task.from_dict(raw_task) for raw_task in raw_tasks]
    except ValueError as error:
        raise ValueError(f"タスクデータを読み込めません: {error}") from error


def save_tasks(tasks: list[Task], path: str | Path | None = None) -> None:
    data_path = Path(path) if path is not None else get_data_path()
    data_path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps([asdict(task) for task in tasks], ensure_ascii=False, indent=2)
    data_path.write_text(content + "\n", encoding="utf-8")