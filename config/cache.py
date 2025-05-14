import orionis

class Config(IConfig):

    config = Cache(

        #--------------------------------------------------------------------------
        # Cache Configuration
        #--------------------------------------------------------------------------
        # Defines the default caching mechanism for the application.
        #
        # If set to `None`, the system will use in-memory caching by default.
        # Otherwise, you can specify the desired cache store.
        #
        # Available options:
        # - none: Loads the configuration into memory once and accesses data from there.
        #         This data is lost and reloaded every time the server restarts.
        # - file: Stores cache data as byte files, ensuring persistence even after server restarts.
        #--------------------------------------------------------------------------

        default = env('CACHE_STORE', None),

        #--------------------------------------------------------------------------
        # Cache Stores
        #--------------------------------------------------------------------------
        # Defines the available cache storage drivers for the application.
        #--------------------------------------------------------------------------

        stores = Stores(

            file = File(
                path = storage_path('framework/cache/data')
            )

        ),

        #--------------------------------------------------------------------------
        # Additional Values
        #--------------------------------------------------------------------------
        # If your application requires additional configurations, you can define
        # them in this dictionary.
        #--------------------------------------------------------------------------

        custom = {}
    )
