# khinsider-streamer

This is a simple python script that allows you to easily stream or download your favorite video game soundtracks straight from the command line!

The program uses yt-dlp and mpv to get the .mp3 files from [downloads.khinsider.com](https://downloads.khinsider.com/).

## Prerequisites: 

* [MPV](https://mpv.io)
* [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* [html.parser](https://docs.python.org/3/library/html.parser.html#module-html.parser)
* [requests](https://pypi.org/project/requests/)
* [validators](https://pypi.org/project/validators/)
* [eyed3](https://pypi.org/project/eyed3/)

## Example Use: 

To run, you can simply execute `python3 khdl.py`.

The program will then prompt you to search for an album.

Once an album is selected, the program will create a playlist in mpv and start streaming each song from the album.

Custom arguments:
* you may specify the mode (either stream or download)
* Examples: 

`python3 khdl.py dl`

`python3 khdl.py stream`

## Future Plans

* create executable files for Windows, MacOS, and Linux.
* allow download and stream in FLAC.

## Known Issues

* Sometimes album names don't display correctly. Try making your search more specific!

## Notice

* I am not affiliated with [downloads.khinsider.com](https://downloads.khinsider.com/).
* If you are affiliated with [downloads.khinsider.com](https://downloads.khinsider.com/) and would like me to take down this repository, please contact me and I will do so.
* I do not endorse piracy.