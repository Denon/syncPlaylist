import urllib2
import platform
import functools
import traceback
import re

download_url = {
    "Windows": "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-windows.zip",
    "Darwin": "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-macosx.zip"
}


class RetryException(Exception):
    pass


def retry(retry_times=0, exc_class=Exception, notice_message=None, print_exc=False):
    def wrapper(f):
        @functools.wraps(f)
        def inner_wrapper(*args, **kwargs):
            current = 0
            while True:
                try:
                    return f(*args, **kwargs)
                except exc_class as e:
                    if print_exc:
                        traceback.print_exc()
                    if current >= retry_times:
                        raise RetryException()
                    if notice_message:
                        print notice_message
                    current += 1
        return inner_wrapper
    return wrapper


def download(file_path):
    """get code from https://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
    """
    phantomjs_file = file_path + download_url[platform.system()].split('/')[-1]
    u = urllib2.urlopen(download_url[platform.system()])
    f = open(phantomjs_file, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (phantomjs_file, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
        status = "%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        print status
    f.close()
    return phantomjs_file


def unzip(zip_file, file_path):
    import zipfile
    zip_ref = zipfile.ZipFile(zip_file, 'r')
    zip_ref.extractall(file_path)
    zip_ref.close()


def _print(msg):
    print msg.encode('utf8')


def clear_string(text):
    regex = re.compile(r'[\n\r\t]')
    return regex.sub('', text)
