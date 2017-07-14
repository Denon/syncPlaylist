from distutils.core import setup
import py2exe
from glob import glob

setup(
    console=["run.py"],
    data_files=[
        (r'.', glob(r'D:\myproject\syncPlaylist\config.json')),
        (r'.', glob(r'D:\Anaconda3\envs\py27\Lib\site-packages\selenium\webdriver\remote\getAttribute.js')),
        (r'.', glob(r'D:\Anaconda3\envs\py27\Lib\site-packages\selenium\webdriver\remote\isDisplayed.js')),
        (r'.', glob(r'D:\myproject\syncPlaylist\phantomjs-2.1.1-windows.zip'))
    ]
)