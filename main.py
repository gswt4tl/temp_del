import os
import shutil


def clear_directory(path):
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                if os.path.isdir(item_path):
                    shutil.rmtree(dir, ignore_errors=True)
            except PermissionError:
                print(f'Нет прав для удаления: {item_path}')
            except Exception as e:
                print(f'Ошибка при удалении {item_path}: {e}')
        return True

    except Exception as e:
        print(f'Критическая ошибка при очистке {path}: {e}')
        return False
