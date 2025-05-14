from orionis.luminate.contracts.config.config import IConfig
from orionis.luminate.config.filesystems import AWSS3, Disks, Filesystems, Local, Public
from orionis.luminate.services.environment.environment_service import env
from orionis.luminate.facades.files.path_facade import storage_path

class Config(IConfig):

    config = Filesystems(

        #--------------------------------------------------------------------------
        # Default File System Disk
        #--------------------------------------------------------------------------
        # This value defines the default file storage configuration to be used
        # in the application.
        #--------------------------------------------------------------------------

        default = env('FILESYSTEM_DISK', 'local'),

        #--------------------------------------------------------------------------
        # File System Disks
        #--------------------------------------------------------------------------
        # Configuration for each of the storage options that can be used in the system.
        # Here, you can define multiple disks for storing files locally or on cloud services
        # like Amazon S3.
        #--------------------------------------------------------------------------

        disks = Disks(

            #----------------------------------------------------------------------
            # Local Disk
            #----------------------------------------------------------------------
            # Defines the storage path for private files
            #----------------------------------------------------------------------

            local = Local(
                path=storage_path('app/private')
            ),

            #----------------------------------------------------------------------
            # Public Disk
            #----------------------------------------------------------------------
            # Defines the location where files will be publicly exposed
            # through the application's base URL.
            # The 'static' slug is defined so that static files are served
            #----------------------------------------------------------------------

            public = Public(
                path=storage_path('app/public'),
                slug='/'
            ),

            #----------------------------------------------------------------------
            # Amazon S3 Disk
            #----------------------------------------------------------------------
            # Configuration for using Amazon S3 to store files in the cloud. S3 is a
            # popular, scalable cloud storage service. You can configure the access
            # credentials, bucket name, and other options here.
            #----------------------------------------------------------------------

            s3 = AWSS3(
                key=env('AWS_ACCESS_KEY_ID'),
                secret=env('AWS_SECRET_ACCESS_KEY'),
                region=env('AWS_DEFAULT_REGION'),
                bucket=env('AWS_BUCKET'),
                url=env('AWS_URL'),
                endpoint=env('AWS_ENDPOINT'),
                use_path_style_endpoint=env('AWS_USE_PATH_STYLE_ENDPOINT', False),
                throw=False
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