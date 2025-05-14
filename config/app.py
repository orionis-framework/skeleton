from config import *

class Config(IConfig):

    config = App(

        #--------------------------------------------------------------------------
        # Application Name
        #--------------------------------------------------------------------------
        # Defines the name that will be displayed in the browser's title bar.
        # This application name may also be used in other parts of the application,
        # such as in view headers or similar places.
        #--------------------------------------------------------------------------

        name = env('APP_NAME', 'Orionis Application'),

        #--------------------------------------------------------------------------
        # Application Environment
        #--------------------------------------------------------------------------
        # Defines the environment in which the application is running.
        # This value can be 'development', 'testing', or 'production'.
        # Depending on the environment, the application may behave differently,
        # such as enabling or disabling debugging, showing detailed error messages, etc.
        #--------------------------------------------------------------------------

        env = env('APP_ENV', Environments.DEVELOPMENT),

        #--------------------------------------------------------------------------
        # Debug Mode
        #--------------------------------------------------------------------------
        # Enables or disables detailed error display.
        #
        # When set to True, the application will show detailed error messages,
        # which is useful during development but should be disabled in production
        # to avoid exposing sensitive information and unnecessary error processing.
        #--------------------------------------------------------------------------

        debug = env('APP_DEBUG', True),

        #--------------------------------------------------------------------------
        # Uvicorn Server Configuration
        #--------------------------------------------------------------------------
        # Defines the settings for running the application with Uvicorn.
        #
        # - `url`     : The host address for the application.
        # - `port`    : The port number on which the application will run.
        # - `workers` : Number of worker processes to handle requests.
        # - `reload`  : Enables auto-reloading when code changes (useful for development).
        #--------------------------------------------------------------------------

        url = env('APP_URL', 'http://127.0.0.1'),
        port = env('APP_PORT', 8000),
        workers = env('APP_WORKERS', 1),
        reload = env('APP_RELOAD', True),

        #--------------------------------------------------------------------------
        # Timezone Configuration
        #--------------------------------------------------------------------------
        # Defines the application's default timezone.
        #
        # This setting ensures consistency when handling timestamps, logs,
        # and scheduled tasks. The default value is 'UTC'.
        #--------------------------------------------------------------------------

        timezone = env('APP_TIMEZONE', 'UTC'),

        #--------------------------------------------------------------------------
        # Locale Configuration
        #--------------------------------------------------------------------------
        # Defines the default locale for the application.
        #
        # This setting is used for localization and internationalization.
        # It determines the language and regional settings for the application.
        # The default value is 'en' (English).
        #--------------------------------------------------------------------------

        locale = env('APP_LOCALE', 'en'),
        fallback_locale = env('APP_FALLBACK_LOCALE', 'en'),

        #--------------------------------------------------------------------------
        # Application Key
        #--------------------------------------------------------------------------
        # Defines the key used for encryption and decryption of sensitive data.
        #
        # The required key length and format depend on the selected encryption
        # algorithm. Supported algorithms include AES-128-CBC, AES-192-CBC,
        # AES-256-CBC, AES-128-GCM, AES-256-GCM, AES-CTR, AES-CFB, AES-CFB8,
        # AES-CFB128, AES-OFB, and AES-ECB.
        # Ensure the key matches the requirements of the chosen cipher and is kept
        # secret. It is recommended to set the key via environment variables.
        #--------------------------------------------------------------------------

        cipher = env('APP_CIPHER', Cipher.AES_256_CBC),
        key = env('APP_KEY'),

        #--------------------------------------------------------------------------
        # Maintenance Route
        #--------------------------------------------------------------------------
        # Defines the route that will return the response indicating
        # that the system is under maintenance.
        #--------------------------------------------------------------------------

        maintenance = env('APP_MAINTENANCE', '/maintenance'),
    )
