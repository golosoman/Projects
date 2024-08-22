import logging
from logging.handlers import RotatingFileHandler
import os
import datetime


class ProgramLogger:
    """
    Класс для создания настраиваемого логгера с записью в файл и вывод в консоль.
    """

    def __init__(self, log_file_name='./app/Log/app.log', log_level=logging.INFO,
                 console_level=logging.INFO, max_bytes=25000000, backup_count=1):
        """
        Инициализирует логгер.

        Args:
            log_file_name (str): Имя файла для записи логов.
            log_level (int): Уровень логирования для файла (например, logging.DEBUG, logging.INFO, logging.WARNING).
            console_level (int): Уровень логирования для консоли (например, logging.DEBUG, logging.INFO, logging.WARNING).
            max_bytes (int): Максимальный размер файла в байтах.
            backup_count (int): Количество резервных файлов.
        """

        # Создаем объект логгера с именем текущего модуля
        self.logger = logging.getLogger(__name__)
        # Устанавливаем уровень DEBUG для логгера
        self.logger.setLevel(logging.DEBUG)

        # Создаем обработчик для записи в файл
        self.file_handler = RotatingFileHandler(
            os.path.join(os.getcwd(), log_file_name),
            maxBytes=max_bytes,
            backupCount=backup_count,
        )
        self.file_handler.setLevel(log_level)

        # Создаем обработчик для вывода в консоль
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(console_level)

        # Создаем форматтер для логов
        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Устанавливаем форматтер для обработчиков
        self.file_handler.setFormatter(self.formatter)
        self.console_handler.setFormatter(self.formatter)

        # Добавляем обработчики к логгеру
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)

        # Добавляем очистку старых файлов
        self.clean_old_logs()

    def clean_old_logs(self):
        """
        Удаляет файлы логов старше одной недели.
        """
        log_dir = os.getcwd()
        now = datetime.datetime.now()
        one_week_ago = now - datetime.timedelta(weeks=1)

        for filename in os.listdir(log_dir):
            if filename.endswith(".log"):
                file_path = os.path.join(log_dir, filename)
                modified_time = datetime.datetime.fromtimestamp(
                    os.path.getmtime(file_path))
                if modified_time < one_week_ago:
                    os.remove(file_path)
                    print(f"Удален старый файл лога: {filename}")

    def debug(self, msg):
        """
        Запись отладочного сообщения.

        Args:
            msg (str): Сообщение.
        """
        self.logger.debug(msg)

    def info(self, msg):
        """
        Запись информационного сообщения.

        Args:
            msg (str): Сообщение.
        """
        self.logger.info(msg)

    def warning(self, msg):
        """
        Запись предупреждающего сообщения.

        Args:
            msg (str): Сообщение.
        """
        self.logger.warning(msg)

    def error(self, msg):
        """
        Запись сообщения об ошибке.

        Args:
            msg (str): Сообщение.
        """
        self.logger.error(msg)

    def critical(self, msg):
        """
        Запись критического сообщения.

        Args:
            msg (str): Сообщение.
        """
        self.logger.critical(msg)


# Создаем экземпляр логгера с настройками:
# - Запись в файл "app.log" с уровнем DEBUG
# - Вывод в консоль с уровнем INFO
logger = ProgramLogger(log_level=logging.DEBUG, console_level=logging.INFO)
