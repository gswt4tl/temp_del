import os
import shutil
import getpass
import logging

logging.basicConfig(level=logging.INFO, filename='tempdel.log',
                    filemode='w', format='%(asctime)s %(levelname)s %(message)s')


# Очистка директории
def clear_directory(path):
    try:
        if not os.path.exists(path):
            logging.warning(f'Путь не существует: {path}')
            return False
        if not os.path.isdir(path):
            logging.warning(f'Путь не является директорией: {path}')
            return False

        logging.info(f'Очистка директории: {path}')

        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                    logging.info(f'Удален файл: {item_path}')
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    logging.info(f'Удалена папка: {item_path}')
            except PermissionError:
                logging.warning(f'Нет прав для удаления: {item_path}')
            except Exception as e:
                logging.error(f'Ошибка при удалении {item_path}: {e}')
        return True

    except Exception as e:
        logging.error(f'Критическая ошибка при очистке {path}: {e}')
        return False


# Безопасная очистка директории
def safe_clear_directory(path):
    abs_path = os.path.abspath(path)
    forbidden_paths = [r'C:\\Windows', r'C:\\Program Files',
                       r'C:\\Program Files (x86)', r'C:\\', os.path.expanduser('~')]
    for forbidden_path in forbidden_paths:
        if abs_path.startswith(forbidden_path) and abs_path != forbidden_path:
            if abs_path not in [os.path.abspath(p) for p in filepaths]:
                logging.error(f'Попытка очистки запрещённой папки: {abs_path}')
                return False
    return clear_directory(abs_path)


def main():
    print('Начинаем очистку временных файлов')
    print('Будут очищены следующие папки:')
    for path in filepaths:
        print(f' - {path}')

    # Запрос подтверждения
    confirm = input('\nПродолжить? (y/n): ').lower()
    if confirm not in ['y', 'yes', 'д', 'да']:
        print('Очистка отменена')
        return

    print('\nНачинаем очистку...')

    for filepath in filepaths:
        print(f'\nОчищаем: {filepath}')
        success = safe_clear_directory(filepath)
        if success:
            print(f'✓ {filepath} - очистка завершена')
        else:
            print(f'✗ {filepath} - ошибка при очистке')

    print('\nОчистка завершена')


username = getpass.getuser()
filepaths = [fr'C:\Users\{username}\AppData\Local\Temp',
             r'C:\Windows\Prefetch', r'C:\Windows\Temp']


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nОчистка прервана пользователем')
    except Exception as e:
        print(f'Неожиданная ошибка: {e}')
