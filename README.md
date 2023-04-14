# khinsider-streamer

This is a simple python script that allows you to easily stream or download your favorite video game soundtracks straight from the command line!

The program uses yt-dlp and mpv to get the MP3 and FLAC files from [downloads.khinsider.com](https://downloads.khinsider.com/).

## Prerequisites
* [Python 3.7+](https://python.org/downloads)
* [MPV](https://mpv.io)
* [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* [requests](https://pypi.org/project/requests/)
* [beatifulsoup4](https://pypi.org/project/beautifulsoup4/)

## Getting Started

* First install [MPV](https://mpv.io).
* If you want the albums to be streamed to a GUI instead of CLI, then check [this](https://github.com/mpv-player/mpv/issues/1808) out.
* run `python3 -m pip install -r requirements.txt`

## Example Use

To run, you can simply execute `python3 khdl.py`.

The program will then prompt you to search for an album.

Once an album is selected, the program will create a playlist in mpv and start streaming each song from the album.

## Help Mesage

```
usage: khdl.py [-h] [-d] [-o OUTPUT_PATH] [-f {mp3,flac}] [-ds]

Stream or download video game music from khinsider (https://downloads.khinsider.com).

options:
  -h, --help            show this help message and exit
  -d, --download        download albums instead of streaming them
  -o OUTPUT_PATH, --output-path OUTPUT_PATH
                        specify a path where you want your files to go
  -f {mp3,flac}, --format {mp3,flac}
                        specify what format you would like to stream/download in
  -ds, --disable-save   disables the default ability of the program to save the download links associated with each album
  ```

## Future Features

Ranked by priority (1 being highest)

1. allow for the creation, playback, and download of playlists
2. create executable files for Windows, MacOS, and Linux.
3. allow for use of VLC when streaming.

## Known Issues

* the character "#" in a song link prevents yt-dlp and mpv from accessing the file. Therefore, these links will not be converted into regular text and will maintain their percent encoding.

## Notice

* I am not affiliated with [downloads.khinsider.com](https://downloads.khinsider.com/).
* If you are affiliated with [downloads.khinsider.com](https://downloads.khinsider.com/) and would like me to take down this repository, please contact me and I will do so.
* I do not endorse piracy.