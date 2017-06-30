import platform
import os
import stat
import traceback
from utils import unzip

download_url = {
    "Windows": "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-windows.zip",
    "Darwin": "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-macosx.zip"  # Mac OS
}
driver_zip_file = {
    "Windows": "phantomjs-2.1.1-macosx.zip",
    "Darwin": "phantomjs-2.1.1-macosx.zip"
}
default_driver_path = {
    "Windows": "driver/phantomjs-2.1.1-windows/bin/phantomjs.exe",
    "Darwin": "driver/phantomjs-2.1.1-macosx/bin/phantomjs"  # Mac OS
}
current_os = platform.system()

if __name__ == '__main__':
    try:
        import settings
        if not os.path.exists(default_driver_path[current_os]):
            zip_file_path = driver_zip_file[current_os]
            if not os.path.exists(zip_file_path):
                raise Exception("Please Download driver first!!!")
            unzip(zip_file_path, 'driver')
        driver_path = default_driver_path[current_os]
        st = os.stat(driver_path)
        os.chmod(driver_path, st.st_mode | stat.S_IEXEC)
        settings.phantomjs_driver_path = driver_path
        mode = raw_input("Please select sync mode(1: from WY to QQ; 2: from QQ to WY)")
        if mode in ("1", 1):
            from WYtoQQ import *
            WYtoQQ().run()
        elif mode in ("2", 2):
            from QQtoWY import *
            QQtoWY().run()
        else:
            raise Exception("Please select 1 or 2")
    except Exception as e:
        traceback.print_exc()
        raw_input("Error! press Enter to exit")
    else:
        raw_input("Finish! press Enter to exit")
