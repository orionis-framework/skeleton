from orionis.luminate.contracts.config.config import IConfig
from orionis.luminate.config.logging import Stack, Hourly, Daily, Weekly, Monthly, Chunked, Channels, Logging
from orionis.luminate.services.environment.environment_service import env
from orionis.luminate.facades.files.path_facade import storage_path

class Config(IConfig):

    config = Logging(

        #----------------------------------------------------------------------
        # Default Logging Configuration
        #----------------------------------------------------------------------
        # This value defines the default logging configuration used by the application.
        # It specifies which log channel to use for logging. The 'single' channel is
        # used by default, meaning all logs are written to a single log file.
        #----------------------------------------------------------------------
        default = env('LOG_CHANNEL', 'stack'),

        #----------------------------------------------------------------------
        # Logging Channels
        #----------------------------------------------------------------------
        # Here you can configure the different logging channels used by the application.
        # Each channel represents a way to write logs to a different location such as
        # a file, the console, or an external service. You can define multiple channels
        # with different configurations for log file rotation, retention, etc.
        #----------------------------------------------------------------------
        channels = Channels(

            #------------------------------------------------------------------
            # Single File Channel
            #------------------------------------------------------------------
            # This channel writes all log entries to a single log file.
            # Useful for applications that do not require rotation or segmentation
            # of log files.
            #------------------------------------------------------------------
            stack = Stack(
                path=storage_path('logs/orionis.log'),  # Path to store the log file
                level=env('LOG_LEVEL', 'debug')  # Log level, can be 'debug', 'info', etc.
            ),

            #------------------------------------------------------------------
            # Hourly Log Channel
            #------------------------------------------------------------------
            # This channel writes logs to a file and retains logs for a specific
            # number of hours. After the specified retention period, old logs are
            # automatically deleted.
            #------------------------------------------------------------------
            hourly = Hourly(
                path=storage_path('logs/orionis.log'),  # Path to store the log file
                level=env('LOG_LEVEL', 'debug'),  # Log level
                retention_hours=env('LOG_RETENTION_HOURS', 24)  # Retention period in hours
            ),

            #------------------------------------------------------------------
            # Daily Log Channel
            #------------------------------------------------------------------
            # This channel writes logs to a file and retains them for a specified
            # number of days. It also allows specifying the time of day when log
            # rotation should occur (e.g., at midnight).
            #------------------------------------------------------------------
            daily = Daily(
                path=storage_path('logs/orionis.log'),  # Path to store the log file
                level=env('LOG_LEVEL', 'debug'),  # Log level
                retention_days=env('LOG_RETENTION_DAYS', 30),  # Retention period in days
                at="00:00"  # Time of day when rotation occurs
            ),

            #------------------------------------------------------------------
            # Weekly Log Channel
            #------------------------------------------------------------------
            # This channel writes logs to a file and retains them for a specified
            # number of weeks. Logs older than the specified number of weeks are
            # automatically deleted.
            #------------------------------------------------------------------
            weekly = Weekly(
                path=storage_path('logs/orionis.log'),  # Path to store the log file
                level=env('LOG_LEVEL', 'debug'),  # Log level
                retention_weeks=env('LOG_RETENTION_WEEKS', 4)  # Retention period in weeks
            ),

            #------------------------------------------------------------------
            # Monthly Log Channel
            #------------------------------------------------------------------
            # This channel writes logs to a file and retains them for a specified
            # number of months. Logs older than the specified number of months
            # are automatically deleted.
            #------------------------------------------------------------------
            monthly = Monthly(
                path=storage_path('logs/orionis.log'),  # Path to store the log file
                level=env('LOG_LEVEL', 'debug'),  # Log level
                retention_months=env('LOG_RETENTION_MONTHS', 2)  # Retention period in months
            ),

            #------------------------------------------------------------------
            # Chunked Log Channel
            #------------------------------------------------------------------
            # This channel writes log entries to a series of files, each having
            # a maximum size. When the log file reaches the specified size limit,
            # a new file is created. This is useful for applications that generate
            # large log files and need to split them into smaller chunks.
            #------------------------------------------------------------------
            chunked = Chunked(
                path=storage_path('logs/orionis.log'),  # Path to store the log file
                level=env('LOG_LEVEL', 'debug'),  # Log level
                mb_size=env('LOG_CHUNKED_SIZE', 5),  # Max size of each chunk in MB (e.g., 5MB)
                files=env('LOG_CHUNKED_FILES', 5)  # Number of log files to retain
            )

        ),

        #----------------------------------------------------------------------
        # Additional Values
        #----------------------------------------------------------------------
        # If your application requires additional configurations, you can define
        # them in this dictionary. For example, custom settings for external services
        # or application-specific options.
        #----------------------------------------------------------------------
        custom = {}
    )
