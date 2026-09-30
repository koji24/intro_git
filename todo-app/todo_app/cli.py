from collections.abc import Callable
from pathlib import Path

from .models import PRIORITIES, Task
from .storage import load_tasks, save_tasks


Input = Callable[[str], str]
Output = Callable[[str], None]


def display_tasks(tasks: list[Task], output_fn: Output = print) -> None:
    if not tasks:
        output_fn("Todoリストは空です。")
        return

    output_fn("Todoリスト:")
    for index, task in enumerate(tasks, start=1):
        status = "完了" if task.completed else "未完了"
        output_fn(f"{index}. [{status}] {task.title}（優先度: {task.priority}）")


def _save(tasks: list[Task], data_path: str | Path | None, output_fn: Output) -> None:
    try:
        save_tasks(tasks, data_path)
    except OSError as error:
        output_fn(f"タスクを保存できませんでした: {error}")


def _select_task(
    tasks: list[Task], input_fn: Input, output_fn: Output, action: str
) -> int | None:
    if not tasks:
        output_fn("Todoリストは空です。")
        return None

    display_tasks(tasks, output_fn)
    try:
        number = int(input_fn(f"{action}するタスク番号: ").strip())
    except ValueError:
        output_fn("番号を入力してください。")
        return None

    if number < 1 or number > len(tasks):
        output_fn("その番号のタスクはありません。")
        return None
    return number - 1


def _add_task(
    tasks: list[Task], input_fn: Input, output_fn: Output, data_path: str | Path | None
) -> None:
    title = input_fn("タスク名: ").strip()
    if not title:
        output_fn("タスク名を入力してください。")
        return

    priority = input_fn("優先度（高・中・低）: ").strip()
    if priority not in PRIORITIES:
        output_fn("優先度は「高」「中」「低」から選択してください。")
        return

    task_id = max((task.id for task in tasks), default=0) + 1
    tasks.append(Task(id=task_id, title=title, priority=priority))
    _save(tasks, data_path, output_fn)
    output_fn(f"タスク「{title}」を追加しました。")


def _complete_task(
    tasks: list[Task], input_fn: Input, output_fn: Output, data_path: str | Path | None
) -> None:
    index = _select_task(tasks, input_fn, output_fn, "完了")
    if index is None:
        return
    task = tasks[index]
    if task.completed:
        output_fn(f"タスク「{task.title}」はすでに完了しています。")
        return
    task.completed = True
    _save(tasks, data_path, output_fn)
    output_fn(f"タスク「{task.title}」を完了にしました。")


def _delete_task(
    tasks: list[Task], input_fn: Input, output_fn: Output, data_path: str | Path | None
) -> None:
    index = _select_task(tasks, input_fn, output_fn, "削除")
    if index is None:
        return
    deleted_task = tasks.pop(index)
    _save(tasks, data_path, output_fn)
    output_fn(f"タスク「{deleted_task.title}」を削除しました。")


def run(
    input_fn: Input | None = None,
    output_fn: Output = print,
    data_path: str | Path | None = None,
) -> None:
    input_fn = input if input_fn is None else input_fn
    try:
        tasks = load_tasks(data_path)
    except (OSError, ValueError) as error:
        output_fn(f"タスクデータを読み込めませんでした: {error}")
        return

    actions = {
        "1": lambda: _add_task(tasks, input_fn, output_fn, data_path),
        "2": lambda: display_tasks(tasks, output_fn),
        "3": lambda: _complete_task(tasks, input_fn, output_fn, data_path),
        "4": lambda: _delete_task(tasks, input_fn, output_fn, data_path),
    }
    try:
        while True:
            output_fn("\n=== Todoリスト ===")
            output_fn("1. タスクを追加")
            output_fn("2. タスクを一覧表示")
            output_fn("3. タスクを完了にする")
            output_fn("4. タスクを削除")
            output_fn("0. 終了")
            choice = input_fn("番号を選択: ").strip()

            if choice == "0":
                output_fn("Todoリストを終了します。")
                return
            action = actions.get(choice)
            if action is None:
                output_fn("メニュー番号を選択してください。")
            else:
                action()
    except EOFError:
        output_fn("入力が終了しました。Todoリストを終了します。")


def main() -> None:
    try:
        run()
    except KeyboardInterrupt:
        print("\nTodoリストを終了します。")