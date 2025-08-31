import os
import shutil
import getpass
import logging

logging.basicConfig(level=logging.INFO, filename="tempdel.log",
                    filemode="w", format="%(asctime)s %(levelname)s %(message)s")


# Очистка директории
def clear_directory(path):
    try:
        if not os.path.exists(path):
            logging.warning(f"Path doesn't exist: {path}")
            return False
        if not os.path.isdir(path):
            logging.warning(f"Path isn't a directory: {path}")
            return False

        logging.info(f"Cleaning the directory: {path}")

        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                    logging.info(f"Deleted file: {item_path}")
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    logging.info(f"Deleted folder: {item_path}")
            except PermissionError:
                logging.warning(f"No permission to delete: {item_path}")
            except Exception as e:
                logging.error(f"Error occured while deleting {item_path}: {e}")
        return True

    except Exception as e:
        logging.error(f"Critical error occured while clearing {path}: {e}")
        return False


# Безопасная очистка директории
def safe_clear_directory(path):
    abs_path = os.path.abspath(path)
    forbidden_paths = [r"C:\\Windows", r"C:\\Program Files",
                       r"C:\\Program Files (x86)", r"C:\\", os.path.expanduser("~")]
    for forbidden_path in forbidden_paths:
        if abs_path.startswith(forbidden_path) and abs_path != forbidden_path:
            if abs_path not in [os.path.abspath(p) for p in filepaths]:
                logging.error(
                    f"Attempted to clear a forbidden path: {abs_path}")
                return False
    return clear_directory(abs_path)


def main():
    print("Starting the cleanup")
    print("Next paths will be cleaned:")
    for path in filepaths:
        print(f" - {path}")

    # Запрос подтверждения
    confirm = input("\nContinue? (y/n): ").lower()
    if confirm not in ["y", "yes", "д", "да"]:
        print("Cleanup cancelled")
        return

    print("\nStarting the cleanup...")

    for filepath in filepaths:
        print(f"\nCleaning: {filepath}")
        success = safe_clear_directory(filepath)
        if success:
            print(f"✓ {filepath} - cleanup succeeded")
        else:
            print(f"✗ {filepath} - error occured while cleaning")

    print("\nCleanup completed")


username = getpass.getuser()
filepaths = [fr"C:\Users\{username}\AppData\Local\Temp",
             r"C:\Windows\Prefetch", r"C:\Windows\Temp"]


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCleanup interrupted by user")
    except Exception as e:
        print(f"Unexpected cleanup: {e}")
