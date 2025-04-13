import logging
import sys
import os

logger = logging.getLogger("carpenter")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)


class SafeFormatter(logging.Formatter):
    """Custom formatter that safely handles output encoding issues"""

    COLORS = {
        "INFO": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "CRITICAL": "\033[91m",
        "DEBUG": "\033[94m",
        "RESET": "\033[0m",
    }

    def format(self, record):
        log_message = super().format(record)

        level_name = record.levelname
        if level_name in self.COLORS and sys.stdout.isatty():
            colored_message = (
                f"{self.COLORS[level_name]}{log_message}{self.COLORS['RESET']}"
            )
            try:
                colored_message.encode(sys.stdout.encoding)
                return colored_message
            except (UnicodeEncodeError, AttributeError):
                pass

        try:
            if hasattr(sys.stdout, "encoding") and sys.stdout.encoding:
                log_message.encode(sys.stdout.encoding)
            else:
                log_message.encode("cp1252", errors="replace")
            return log_message
        except UnicodeEncodeError:
            if hasattr(sys.stdout, "encoding") and sys.stdout.encoding:
                return log_message.encode(sys.stdout.encoding, errors="replace").decode(
                    sys.stdout.encoding
                )
            else:
                return log_message.encode("cp1252", errors="replace").decode("cp1252")


# Set formatter
formatter = SafeFormatter("%(message)s")
console_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(console_handler)

# Example of file handler (commented out)
"""
# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

file_handler = logging.FileHandler('logs/carpenter.log')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
"""
