from orionis.luminate.contracts.config.config import IConfig
from orionis.luminate.config.cors import Cors

class Config(IConfig):

    config = Cors(

        #--------------------------------------------------------------------------
        # Application Methods
        #--------------------------------------------------------------------------
        # Value to determine the HTTP methods allowed by CORS to be configured.
        # These are the methods that can be used by the client when making requests.
        #--------------------------------------------------------------------------

        allowed_methods = ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE'],

        #--------------------------------------------------------------------------
        # Application Origins
        #--------------------------------------------------------------------------
        # Value to determine the allowed origins by CORS.
        # This specifies which domains are allowed to access the resources of the
        # application. The wildcard '*' allows all origins.
        #--------------------------------------------------------------------------

        allowed_origins = '*',

        #--------------------------------------------------------------------------
        # Application Headers
        #--------------------------------------------------------------------------
        # Value to define the allowed headers by CORS.
        # This specifies which HTTP headers can be used when making the actual request.
        # The wildcard '*' allows all headers.
        #--------------------------------------------------------------------------

        allowed_headers = '*',

        #--------------------------------------------------------------------------
        # Exposed Headers
        #--------------------------------------------------------------------------
        # Value to define headers that can be exposed to the browser by CORS.
        # These headers are not available by default, but you can allow specific ones
        # if needed. `None` means no additional headers will be exposed.
        #--------------------------------------------------------------------------

        exposed_headers = None,

        #--------------------------------------------------------------------------
        # Max Age
        #--------------------------------------------------------------------------
        # Value to set the maximum time (in seconds) for which the results of a preflight
        # request can be cached by the browser.
        # This avoids sending a preflight request every time the resource is accessed.
        # `None` means there is no specific time set.
        #--------------------------------------------------------------------------

        max_age = None,

        #--------------------------------------------------------------------------
        # Additional Values
        #--------------------------------------------------------------------------
        # If your application requires additional configurations, you can define
        # them in this dictionary.
        #--------------------------------------------------------------------------

        custom = {}

    )