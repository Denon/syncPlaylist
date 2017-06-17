import platform
from utils import download, unzip

download_url = {
    "Windows": "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-windows.zip",
    "Darwin": "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-macosx.zip"  # Mac OS
}
default_driver_path = {
    "Windows": "phantomjs-2.1.1-windows/bin/phantomjs.exe",
    "Darwin": "phantomjs-2.1.1-macosx/bin/phantomjs"  # Mac OS
}
current_os = platform.system()

if __name__ == '__main__':
    import settings
    local_driver = raw_input("Do you have phantomjs driver[Y/N](default is Y): ")
    if str.upper(local_driver) == 'N':
        file_path = 'driver/'
        download_file = download(current_os, file_path)
        unzip(download_file, file_path)
        driver_path = file_path + default_driver_path[current_os]
    elif str.upper(local_driver) == 'Y' or local_driver == '':
        driver_path = settings.phantomjs_driver_path[current_os]
    else:
        raise Exception('Please input Y or N')
    settings.phantomjs_driver_path = driver_path
    from WYtoQQ import *
    main()
