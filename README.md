# syncPlaylist
Sync music.163 playlist to music.qq

---------------
## requirement
1. beautifulsoup4
2. requests
3. selenium

---------------
## Usage
1. If you are Mac user, you can run `get_mac_phantomjs.sh` in `driver` dir. Or you can download phantoms from [here](http://phantomjs.org/download.html). Then rewrite the driver path in `settings.py`
2. add your qq account in `config.json`
3. copy 163 playlist url in `config.json`.wy_playlist_url
4. input qq playlist name in `config.json`.qq_playlist_name
5. run `python 163toQQ.py`


## debug
you can use chrome driver.