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
        from WYtoQQ import *
        main()
    except Exception as e:
        print e
        raw_input("Error! press Enter to exit")
