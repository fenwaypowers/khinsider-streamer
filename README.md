# khinsider-streamer

This is a simple python script that allows you to easily stream or download your favorite video game soundtracks straight from the command line!

The program uses yt-dlp and mpv to get the .mp3 files from [downloads.khinsider.com](https://downloads.khinsider.com/).

All you need to provide is a link to the album from khinsider.

## Prerequisites: 

* [MPV](https://mpv.io)
* [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* [html.parser](https://docs.python.org/3/library/html.parser.html#module-html.parser)
* [requests](https://pypi.org/project/requests/)
* [validators](https://pypi.org/project/validators/)
* [eyed3](https://pypi.org/project/eyed3/)

## Example Use: 

To run, you can simply execute `python3 khdl.py [album link]`.

This will create a playlist in mpv and start streaming each song from the album.

Custom arguments:
* you may specify the mode (either stream or download)
* Examples: 

`python3 khdl.py dl [album link]`

`python3 khdl.py stream [album link]`

## Future Plans

* create executable files for Windows, MacOs, and Linux.
* add a search mode, where instead of having to provide a link, the user can simply search for the album.