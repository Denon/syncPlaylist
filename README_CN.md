# syncPlaylist
在qq音乐和网易云音乐之间同步歌单

## 支持平台
1. Windows
2. MacOS
3. Linux

---------------
## requirement
1. beautifulsoup4
2. requests
3. selenium

---------------
## 使用方法


### 第一步: 设置配置
在 `config.json` 中输入相应配置.

* 如果从网易云音乐同步歌单到QQ:
1. 在 `config.json`[account, password] 添加qq账户(account) 和 密码(password)
2. 在 `config.json`[source_playlist_url] 中输入网易云音乐歌单url
3. 在 `config.json`[target_playlist_url] 中输入qq音乐歌单url


* 如果从qq音乐同步歌单到网易云音乐:
1. 在 `config.json`[account, password], 中输入网易邮箱账号和密码(暂时只支持邮箱方式登陆).
2. 在 `config.json`[source_playlist_url] 中输入qq音乐歌单url
3. 在 `config.json`[target_playlist_url] 中输入网易云音乐歌单url

### 第二部: 运行脚本!
在命令行中运行 `python run.py`

> 如果不确定参数如何输入, 在 `example` 文件夹中有相关的截图. 或者你可以发email给我.

### windows 平台相关
1. 解压 win32.rar 文件
2. 在 `win32/config.json` 下输入相应配置(和第一步一样)
3. 运行 `win32/run.exe`
4. 根据代码提示, 输入对应的模式.

---------------
## 原理
使用webdriver模拟账户登录和在歌单中添加歌曲。
