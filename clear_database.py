"""
Удаление базы данных и всех миграций
"""

import os
import subprocess

DATABASE = "db.sqlite3"
command_migrate = "python manage.py migrate"


if os.path.exists(DATABASE):
    os.remove(DATABASE)

try:
    subprocess.run(command_migrate, shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Ошибка выполнения команды: {e}")

