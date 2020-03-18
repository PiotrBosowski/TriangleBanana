import argparse
import sqlite3
import datetime
from hashlib import sha256
from pathlib import Path


def db_connect():
    home = Path.home()
    db_path = home / "tasks_database.db"
    connection = sqlite3.connect(str(db_path))
    connection.execute('''CREATE TABLE IF NOT EXISTS tasks (hash text, name text, deadline text, description text)''')
    return connection


def action_add(args):
    hashed_content = sha256((str(args.name) + str(args.deadline) + str(args.description)).encode('utf-8')).hexdigest()
    trimmed_hash = hashed_content[:10]
    connection = db_connect()
    connection.execute('''INSERT INTO tasks VALUES (?, ?, ?, ?)''',
                       (trimmed_hash, args.name, args.deadline, args.description))
    connection.commit()
    connection.close()


def action_update(args):
    connection = db_connect()
    connection.execute('''UPDATE tasks SET name = ?, deadline = ?, description = ? WHERE hash = ?''',
                       (args.name, args.deadline, args.description, args.TASK_HASH))
    connection.commit()
    connection.close()


def action_remove(args):
    connection = db_connect()
    connection.execute('''DELETE FROM tasks WHERE hash=?''', (args.TASK_HASH,))
    connection.commit()
    connection.close()


def action_list(args):
    connection = db_connect()
    if args.today:
        today = str(datetime.datetime.today().date())
        records = connection.execute('''SELECT * FROM tasks WHERE deadline=?''', (today,))
    else:
        records = connection.execute('''SELECT * FROM tasks''')
    for row in records:
        print(row)
    connection.close()


if __name__ == '__main__':
    # create the top=level parser
    parser_initial = argparse.ArgumentParser()
    subparsers = parser_initial.add_subparsers()

    # create adding parser
    parser_add = subparsers.add_parser('add', help="add help")
    parser_add.add_argument('--name', required=True, help="name of the task")
    parser_add.add_argument('--deadline', help="deadline of the task")
    parser_add.add_argument('--description', help="brief description of the task")
    parser_add.set_defaults(func=action_add)

    # create updating parser
    parser_update = subparsers.add_parser('update', help="update help")
    parser_update.add_argument('--name', help="name of the task")
    parser_update.add_argument('--deadline', help="deadline of the task")
    parser_update.add_argument('--description', help="brief description of the task")
    parser_update.add_argument('TASK_HASH', help="hash of the task")
    parser_update.set_defaults(func=action_update)

    # create removing parser
    parser_remove = subparsers.add_parser('remove', help="remove help")
    parser_remove.add_argument('TASK_HASH', help="hash of the task")
    parser_remove.set_defaults(func=action_remove)

    # create listing parser
    parser_list = subparsers.add_parser('list', help="list help")
    group = parser_list.add_mutually_exclusive_group()
    group.add_argument('--all', help="all tasks", action="store_true")
    group.add_argument('--today', help="today's tasks", action="store_true")
    parser_list.set_defaults(func=action_list)

    arguments = parser_initial.parse_args()
    arguments.func(arguments)
