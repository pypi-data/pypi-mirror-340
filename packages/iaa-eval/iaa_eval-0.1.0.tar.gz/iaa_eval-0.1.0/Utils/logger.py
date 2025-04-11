import sys
import threading
from datetime import datetime
from typing import TextIO
import os
from enum import Enum
from functools import wraps


class LogLevel(Enum):
    """Enumeration of available log levels."""
    DEBUG = 0    # Most verbose
    INFO = 1
    WARNING = 2
    ERROR = 3    # Least verbose
    CRITICAL = 4  # Added CRITICAL level


class ContextLogger:
    """
    A logger for function entry and exit points.
    This class automatically logs when a function is entered (at creation)
    and exited (at destruction), including file name, line number,
    and thread information.
    """
    def __init__(self, func_or_logger, func_or_none=None):
        """
        Initialize the context logger and log the function entry.

        Args:
            func_or_logger: Either the function to log or a logger instance.
            func_or_none: If func_or_logger is a logger, this should be the
                                function.
                         If func_or_logger is a function, this can be None.
        """
        # Determine which parameter is the function and which is the logger
        if func_or_none is None:
            # First parameter is the function, use singleton logger
            func = func_or_logger
            self.logger = get_logger()
        else:
            # First parameter is the logger, second is the function
            self.logger = func_or_logger
            func = func_or_none

        # Store function information
        self.function_name = func.__name__
        self.function_file = os.path.basename(func.__code__.co_filename)
        self.function_line = func.__code__.co_firstlineno

    def __enter__(self):
        try:
            if self.logger.level.value <= LogLevel.DEBUG.value:
                entry_message = (
                    f"File: {self.function_file} | "
                    f"Line: {self.function_line} | "
                    f"++ {self.function_name}() ++"
                )
                self.logger.debug(entry_message)
        except Exception as e:
            self.logger.warning(
                f"Failed to initialize logging context: {str(e)}"
            )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Log function exit when the context is exited.

        Args:
            exc_type: The type of the exception that occurred, if any
            exc_value: The instance of the exception that occurred, if any
            traceback: The traceback of the exception that occurred, if any
        """
        if hasattr(self, 'logger') and hasattr(self, 'function_name'):
            if self.logger.level.value <= LogLevel.DEBUG.value:
                exit_message = (
                    f"File: {self.function_file} | "
                    f"Line: {self.function_line} | "
                    f"-- {self.function_name}() --"
                )
                self.logger.debug(exit_message)


class Logger:
    """
    A logging utility class that provides different levels of logging
    with optional verbosity control and function call tracing.
    Supports context-based logging for function entry/exit points.

    This class is implemented as a singleton to ensure only one logger
    instance exists throughout the application.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, level: LogLevel = LogLevel.INFO,
                output: TextIO = sys.stdout):
        """
        Create a singleton instance of Logger.

        Args:
            level (LogLevel): The logging level. Defaults to LogLevel.DEBUG.
            output (TextIO): Output stream to write logs to. Defaults to stdout

        Returns:
            Logger: The singleton instance of Logger
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Logger, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self, level: LogLevel = LogLevel.DEBUG,
                 output: TextIO = sys.stdout):
        """
        Initialize the Logger singleton (only once).

        Args:
            level (LogLevel): The logging level. Defaults to LogLevel.DEBUG.
            output (TextIO): Output stream to write logs to. Defaults to stdout

        Raises:
            ValueError: If level is not a valid LogLevel
        """
        # Only initialize once
        if hasattr(self, '_initialized') and self._initialized:
            return

        if not isinstance(level, LogLevel):
            raise ValueError("Level must be a valid LogLevel enum value")
        self.level = level
        self.output = output
        self._initialized = True

    def __write__(self, message: str) -> None:
        """Write a message to the output stream."""
        try:
            self.output.write(message)
            self.output.flush()
        except AttributeError as e:
            sys.stderr.write("Logger error: Output is not writable\n")
            err_msg = (
                f"Logger error: Failed to write message: "
                f"message {message}, error {str(e)}\n"
            )
            sys.stderr.write(err_msg)
            sys.stderr.flush()
        except Exception as e:
            err_msg = (
                f"Logger error: Failed to write message: "
                f"message {message}, error {str(e)}\n"
            )
            sys.stderr.write(err_msg)
            sys.stderr.flush()

    def _format_message(self, level: LogLevel, message: str) -> str:
        """
        Format a log message according to the configured format.

        Args:
            level (LogLevel): The log level (DEBUG, INFO, WARNING, ERROR)
            message (str): The message to log

        Returns:
            str: The formatted message with timestamp, thread ID,
                                                                and level name
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        thread_id = threading.get_ident()
        return (
            f"[{timestamp}] [TID: {thread_id}] "
            f"[{level.name}] {message}\n"
        )

    def _log(self, level: LogLevel, message: str) -> None:
        """
        Log a message if its level is greater than or equal to logger's level.

        Args:
            level (LogLevel): The level of the message.
            message (str): The message to log.
        """
        if level.value >= self.level.value:
            formatted_message = self._format_message(level, message)
            self.__write__(formatted_message)

    def info(self, message: str) -> None:
        """Log an informational message if level is INFO or lower."""
        self._log(LogLevel.INFO, message)

    def warning(self, message: str) -> None:
        """Log a warning message if level is WARNING or lower."""
        self._log(LogLevel.WARNING, message)

    def error(self, message: str) -> None:
        """Log an error message if level is ERROR or lower."""
        self._log(LogLevel.ERROR, message)

    def debug(self, message: str) -> None:
        """Log a debug message if level is DEBUG."""
        self._log(LogLevel.DEBUG, message)

    def critical(self, message: str) -> None:
        """Log a critical message if level is CRITICAL."""
        self._log(LogLevel.CRITICAL, message)

    def set_level(self, level: LogLevel) -> None:
        """
        Change the logging level.

        Args:
            level (LogLevel): The new logging level

        Raises:
            ValueError: If level is not a valid LogLevel
        """
        if not isinstance(level, LogLevel):
            raise ValueError("Level must be a valid LogLevel enum value")
        self.level = level

    def log_scope(self, func):
        """
        Decorator for logging function entry and exit.

        Args:
            func: The function to be decorated

        Returns:
            The wrapped function with logging

        Usage:
            @logger.log_scope
            def my_function():
                # Function code here
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            with ContextLogger(func_or_logger=func, func_or_none=None):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    self.error(f"Exception in {func.__name__}: {str(e)}")
                    raise
        return wrapper


# Convenience function to get the logger instance
def get_logger(level: LogLevel = None,
               output: TextIO = None) -> Logger:
    """
    Get the singleton instance of the Logger.

    Args:
        level (LogLevel, optional):
            The logging level (only used if creating a new instance)
        output (TextIO, optional):
            Output stream (only used if creating a new instance)

    Returns:
        Logger: The singleton Logger instance
    """
    # Check if the singleton instance already exists
    if Logger._instance is not None:
        # Return the existing instance without modifying its properties
        return Logger._instance

    # If no instance exists, create a new one with the provided or
    # default values
    default_level = level if level is not None else LogLevel.INFO
    default_output = output if output is not None else sys.stdout

    return Logger(default_level, default_output)


def init_logger(level: LogLevel = LogLevel.INFO,
                output: TextIO = sys.stdout) -> Logger:
    """
    Initialize or reinitialize the logger singleton with specified settings.
    This function will reset any existing logger instance and create a new one.

    Args:
        level (LogLevel, optional): The logging level. Defaults to
                                    LogLevel.INFO.
        output (TextIO, optional): Output stream. Defaults to sys.stdout.

    Returns:
        Logger: The newly initialized logger instance
    """
    # Reset the singleton instance
    Logger._instance = None

    # Create and return a new instance
    return Logger(level, output)
