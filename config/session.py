from orionis.luminate.config.session import Cookie, Session
from orionis.luminate.contracts.config.config import IConfig
from orionis.luminate.services.environment.environment_service import env
from orionis.luminate.facades.files.path_facade import storage_path

class Config(IConfig):

    config = Session(

        #--------------------------------------------------------------------------
        # Session Driver
        #--------------------------------------------------------------------------
        # This value defines the driver to be used for session management.
        #--------------------------------------------------------------------------

        driver = env('SESSION_DRIVER', 'file'),

        #--------------------------------------------------------------------------
        # Session Lifetime
        #--------------------------------------------------------------------------
        # This value sets the duration (in minutes) for how long the session
        # will be valid before it expires.
        #--------------------------------------------------------------------------

        lifetime = env('SESSION_LIFETIME', 120),

        #--------------------------------------------------------------------------
        # Expire on Close
        #--------------------------------------------------------------------------
        # This value determines whether the session should expire when the user
        # closes their browser. If set to True, the session will not persist
        # after the browser is closed.
        #--------------------------------------------------------------------------

        expire_on_close = env('SESSION_EXPIRE_ON_CLOSE', False),

        #--------------------------------------------------------------------------
        # Session Encryption
        #--------------------------------------------------------------------------
        # This value specifies whether the session data should be encrypted
        # for additional security.
        # If set to True, the session will be encrypted.
        #--------------------------------------------------------------------------

        encrypt = env('SESSION_ENCRYPT', False),

        #--------------------------------------------------------------------------
        # Session File Path
        #--------------------------------------------------------------------------
        # This value defines the directory path where session files will be stored
        # when using the file driver.
        #--------------------------------------------------------------------------

        files = storage_path('framework/sessions'),

        #--------------------------------------------------------------------------
        # Session Cookie Configuration
        #--------------------------------------------------------------------------
        # This section configures the properties of the session cookie.
        #--------------------------------------------------------------------------

        cookie = Cookie(
            name=env('SESSION_COOKIE', None),
            path=env('SESSION_PATH', '/'),
            domain=env('SESSION_DOMAIN'),
            secure=env('SESSION_SECURE_COOKIE'),
            http_only=env('SESSION_HTTP_ONLY', True),
            same_site=env('SESSION_SAME_SITE', 'lax')
        ),

        #--------------------------------------------------------------------------
        # Additional Values
        #--------------------------------------------------------------------------
        # If your application requires additional configurations, you can define
        # them in this dictionary.
        #--------------------------------------------------------------------------

        custom = {}
    )