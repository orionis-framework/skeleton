from orionis.luminate.contracts.config.config import IConfig
from orionis.luminate.config.database import Connections, Database, Mysql, Oracle, Pgsql, Sqlite
from orionis.luminate.services.environment.environment_service import env
from orionis.luminate.facades.files.path_facade import database_path

class Config(IConfig):

    config = Database(

        #--------------------------------------------------------------------------
        # Default Database Connection Name
        #--------------------------------------------------------------------------
        # This value defines the default database connection to be used by your
        # application. It can be set to any of the connections defined below.
        #--------------------------------------------------------------------------

        default = env('DB_CONNECTION', 'sqlite'),

        #--------------------------------------------------------------------------
        # Database Connections
        #--------------------------------------------------------------------------
        # Here you can define all of the database connections used by your application.
        # You can configure multiple connections for different database systems such
        # as SQLite, MySQL, PostgreSQL, and Oracle.
        #--------------------------------------------------------------------------

        connections = Connections(

            #----------------------------------------------------------------------
            # SQLite Database Connection
            #----------------------------------------------------------------------
            # Here you may configure the SQLite database settings used by your
            # application. SQLite is a lightweight database that supports both
            # in-memory and disk-based storage.
            #----------------------------------------------------------------------
            sqlite = Sqlite(
                driver='sqlite',
                url=env('DB_URL'),
                database=env('DB_DATABASE', database_path('database.sqlite')),
                prefix='',
                foreign_key_constraints=env('DB_FOREIGN_KEYS', True),
                busy_timeout=None,
                journal_mode=None,
                synchronous=None
            ),

            #----------------------------------------------------------------------
            # MySQL Database Connection
            #----------------------------------------------------------------------
            # Here you may configure the MySQL database settings used by your
            # application. MySQL is a popular open-source database management
            # system which supports a wide range of features.
            #----------------------------------------------------------------------
            mysql = Mysql(
                driver='mysql',
                url=env('DB_URL'),
                host=env('DB_HOST', '127.0.0.1'),
                port=env('DB_PORT', '3306'),
                database=env('DB_DATABASE', 'orionis'),
                username=env('DB_USERNAME', 'root'),
                password=env('DB_PASSWORD', ''),
                unix_socket=env('DB_SOCKET', ''),
                charset=env('DB_CHARSET', 'utf8mb4'),
                collation=env('DB_COLLATION', 'utf8mb4_unicode_ci'),
                prefix='',
                prefix_indexes=True,
                strict=True,
                engine=None
            ),

            #----------------------------------------------------------------------
            # PostgreSQL Database Connection
            #----------------------------------------------------------------------
            # Here you may configure the PostgreSQL database settings used by your
            # application. PostgreSQL is a robust relational database system known
            # for its reliability, feature robustness, and performance.
            #----------------------------------------------------------------------
            pgsql = Pgsql(
                driver='pgsql',
                url=env('DB_URL'),
                host=env('DB_HOST', '127.0.0.1'),
                port=env('DB_PORT', '5432'),
                database=env('DB_DATABASE', 'orionis'),
                username=env('DB_USERNAME', 'root'),
                password=env('DB_PASSWORD', ''),
                charset=env('DB_CHARSET', 'utf8'),
                prefix='',
                prefix_indexes=True,
                search_path='public',
                sslmode='prefer'
            ),

            #----------------------------------------------------------------------
            # Oracle Database Connection
            #----------------------------------------------------------------------
            # Here you may configure the Oracle database settings used by your
            # application. Oracle is a powerful enterprise database management
            # system that is widely used in corporate environments.
            #----------------------------------------------------------------------
            oracle = Oracle(
                driver='oracle',
                dsn=env('DB_DSN'),
                host=env('DB_HOST', '127.0.0.1'),
                port=env('DB_PORT', '1521'),
                username=env('DB_USERNAME', 'root'),
                password=env('DB_PASSWORD', ''),
                charset=env('DB_CHARSET', 'utf8'),
                service=env('DB_SERVICE'),
                sid=env('DB_SID')
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
