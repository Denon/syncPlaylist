# syncPlaylist
Sync music.163 playlist to music.qq

## platform
1. Windows
2. MacOS
3. Linux(need to download phantomjs driver yourself)

---------------
## requirement
1. beautifulsoup4
2. requests
3. selenium

---------------
## Usage

### First
Download phantomjs driver [here](http://phantomjs.org/download.html). Unzip it. So you can find driver in ./phantomjs-X.X.X/bin/phantomjs

### python script
1. write the driver absolute path in `settings.py`.`phantomjs_driver_path`
2. add your qq account and password in `config.json`
3. copy 163 playlist url in `config.json`.wy_playlist_url
4. input qq playlist name in `config.json`.qq_playlist_name
5. run `python WYtoQQ.py`

### windows exe
1. add your qq account and password in `win32/config.json`
2. copy 163 playlist url in `win32/config.json`.wy_playlist_url
3. input qq playlist name in `win32/config.json`.qq_playlist_name
4. run `win32/run.exe`
5. according the notice, input the driver absolute path.

---------------
## debug
you can use chrome driver.
1. Uncomment line 59 and line 64
2. download chrome driver
3. set driver path in `settings.py`

---------------
## enhancement
1. sync music.qq to music.163.
