VALID_PRIORITIES = ("高", "中", "低")

# Todoリストを画面に表示する関数
# todo_list: 表示したいタスクのリスト
# 空の場合は空であることを知らせる
# そうでなければ番号付きで各タスクを表示する
def display_todo_list(todo_list):
    if not todo_list:
        print("Todoリストは空です。")
    else:
        print("Todoリスト:")
        for index, item in enumerate(todo_list, start=1):
            print(f"{index}. {item['task']}（優先度: {item['priority']}）")

# Todoリストに新しいタスクを追加する関数
# task: 追加したいタスクの内容
# todo_list: 追加先のTodoリスト
# 末尾に新しいタスクを追加して、追加完了メッセージを表示する
def add_task(task, todo_list, priority):
    if priority not in VALID_PRIORITIES:
        print("優先度は「高」「中」「低」から選択してください。")
        return

    todo_list.append({"task": task, "priority": priority})
    print(f"タスク '{task}' が追加されました。")

# Todoリストからタスクを削除する関数
# task_number: 削除したいタスクの番号
# todo_list: 削除先のTodoリスト
# 番号が範囲外の場合はその番号のタスクはありませんというメッセージを表示し、削除しない
def delete_task(task_number, todo_list):
    if task_number < 1 or task_number > len(todo_list):
        print("その番号のタスクはありません。")
        return

    deleted_task = todo_list.pop(task_number - 1)
    print(f"タスク '{deleted_task['task']}' を削除しました。")

tasks = [
    {"task": "買い物をする", "priority": "中"},
    {"task": "本を読む", "priority": "低"},
    {"task": "メールを返信する", "priority": "高"},
]

add_task("提出物を仕上げる", tasks, "高")
delete_task(2, tasks)
display_todo_list(tasks)

