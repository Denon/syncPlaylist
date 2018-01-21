# syncPlaylist
中文版本: `README_CN.md`
Sync playlist between WY and QQ.

## platform
1. Windows
2. MacOS
3. Linux

---------------
## requirement
1. beautifulsoup4
2. requests
3. selenium

---------------
## Usage


### Step 1: input config
input config in `config.json`.

* If you choose WY to QQ:
1. add your qq account and password in `config.json`[account, password]
2. copy 163 playlist url in `config.json`[source_playlist_url]
3. input qq playlist url in `config.json`[target_playlist_url]


* If you choose QQ to WY:
1. add your wy email account and password in `config.json`[account, password], currently only support WY email account.
2. copy qq playlist url in `config.json`[source_playlist_url]
3. input wy user playlist url in `config.json`[target_playlist_url]

### Step 2:run script!
run `python run.py`

> If you are not sure how to input the correct url config, please see the screenshot in dir `example`. Or you can email me.

### windows exe
1. unzip win32.rar
2. Input config in `win32/config.json` according step1
3. run `win32/run.exe`
4. according the notice, chose sync mode.

---------------
## debug
you can use chrome driver.
1. Uncomment line 59 and line 64
2. download chrome driver
3. set driver path in `settings.py`
