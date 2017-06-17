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
1. If you want to download phantomjs driver yourself, you can download from [here](http://phantomjs.org/download.html). Unzip it and then write the abs path in `settings.py`.`phantomjs_driver_path`
2. add your qq account and password in `config.json`
3. copy 163 playlist url in `config.json`.wy_playlist_url
4. input qq playlist name in `config.json`.qq_playlist_name
5. run `python run.py`


## debug
you can use chrome driver.
1. Uncomment line 59 and line 64
2. download chrome driver
3. set driver path in `settings.py`

## enhancement
1. sync music.qq to music.163.
2. convert script to exe.
