import platform

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
    try:
        import settings
        driver_path = raw_input("Please input driver path: ")
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
        print e
        raw_input("Error! press Enter to exit")
