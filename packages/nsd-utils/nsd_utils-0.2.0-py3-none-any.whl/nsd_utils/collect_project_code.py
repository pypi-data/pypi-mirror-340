import os

# Папка проекта (можешь указать конкретную, если не текущая)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Имя файла, куда всё будет собрано
OUTPUT_FILE = os.path.join(PROJECT_DIR, "FULL_PROJECT_DUMP.txt")

# Расширения, которые стоит собирать
TARGET_EXTENSIONS = {".py", ".sql", ".ini", ".json", ".yaml", ".yml", ".txt", ".md"}

# Папки, которые нужно исключить
EXCLUDE_DIRS = {".venv", "__pycache__", ".git", "node_modules", ".idea", ".vscode"}

with open(OUTPUT_FILE, "w", encoding="utf-8") as out_file:
    for root, dirs, files in os.walk(PROJECT_DIR):
        # Убираем лишние директории из обхода
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in TARGET_EXTENSIONS:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, PROJECT_DIR)

                out_file.write(f"\n\n{'='*80}\n# FILE: {relative_path}\n{'='*80}\n\n")
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        out_file.write(f.read())
                except Exception as e:
                    out_file.write(f"[ОШИБКА ЧТЕНИЯ ФАЙЛА: {e}]")

print(f"\n✅ Сборка завершена! Файл сохранён как: {OUTPUT_FILE}")
