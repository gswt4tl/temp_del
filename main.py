import os
import shutil
import getpass
import logging

logging.basicConfig(level=logging.INFO, filename='tempdel.log',
                    filemode='w', format='%(asctime)s %(levelname)s %(message)s')


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


username = getpass.getuser()
filepaths = [fr'C:\Users\{username}\AppData\Local\Temp',
             'C:\Windows\Prefetch', 'C:\Windows\Temp']
