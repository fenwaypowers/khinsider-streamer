import requests
import subprocess
import sys
import os
import logging
import argparse
import tempfile
import shutil
import re
import string
import yt_dlp
from urllib.parse import unquote
from bs4 import BeautifulSoup

logging.basicConfig(format='%(message)s', stream=sys.stdout, level=logging.INFO)

class album():
    title: str
    platforms: str
    album_type: str
    year: str
    link: str

    songs: list = []

    def __init__(self, title: str, platforms: str, album_type: str, year: str, link: str):
        self.title = title
        self.platforms = platforms
        self.album_type = album_type
        self.year = year
        self.link = url_base + link

    def __str__(self) -> str:
        # Check if any of the attributes are empty or None, and replace with placeholders
        title = self.title if self.title else "Unknown Title"
        platforms = self.platforms.rstrip() if self.platforms else "Unknown Platforms"
        album_type = self.album_type if self.album_type else "Unknown Type"
        year = self.year if self.year else "Unknown Year"
        return f'{title} ({platforms}) ({album_type}, {year})'

class song():
    title: str
    link: str
    flac_link: str

    def __init__(self, title: str, link: str, flac_link = ""):
        self.title = title
        self.link = url_base + link
        self.flac_link = flac_link

    def __str__(self) -> str:
        return self.title

def main():

    global format
    global temp_dir
    global url_base
    global download
    global output_dir

    url_base = "https://downloads.khinsider.com"

    temp_dir = tempfile.mkdtemp()

    parser = argparse.ArgumentParser(
        description='Stream or download video game music from khinsider (https://downloads.khinsider.com).')
    parser.add_argument(
        '-d', '--download', help='download albums instead of streaming them.', action='store_true')
    parser.add_argument('-o', '--output-path',
                        help="specify a path where you want your files to go.", default="albums")
    parser.add_argument('-f', '--format', help="specify what format you would like to stream/download in.",
                        choices=["mp3", "flac"], default="mp3")

    args = parser.parse_args()
    format = args.format
    output_dir = os.path.abspath(args.output_path)
    download = args.download

    if not os.path.exists(output_dir) and download:
        os.mkdir(output_dir)

    while (True):
        try:
            sel_album: album = search()

            song_list = parse_alb_page(sel_album)

            sel_album.songs = song_list

            if download:
                try:
                    download_album(sel_album)
                except:
                    logging.info(f"Failed to download album: {sel_album.title}")
            else:
                play_list(sel_album)
                try:
                    pass
                except:
                    logging.info(f"Failed to play album: {sel_album.title}")
        except:
            logging.info(f"Failed to parse the page")
        
def download_album(sel_album: album) -> None:
    output_path = os.path.join(output_dir, sanitize_filename(str(sel_album)))
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    num_digits = len(str(len(sel_album.songs)))
    fmt_string = f"{{:0{num_digits}}}."

    for index, song in enumerate(sel_album.songs):
        ydl_opts = {
            'outtmpl': os.path.join(output_path, fmt_string.format(index+1) + f" {song.title}.%(ext)s")
        }

        dl_link = song.link

        if format == "flac":
            if sel_album.songs[index].flac_link != '':
                dl_link = sel_album.songs[index].flac_link

            if dl_link == song.link:
                dl_link = get_flac_link(dl_link)
                sel_album.songs[index].flac_link = dl_link

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(dl_link)

def play_list(sel_album: album):
    make_playlist(sel_album)
    mpv_args = ["mpv", "--playlist=" + str(os.path.join(temp_dir, "playlist.txt"))]
    subprocess.run(mpv_args)

def make_playlist(sel_album: album):
    song_list = sel_album.songs
    if format == "flac":
        logging.info("FLAC is selected. Depending on the number of songs in the album, it may take an extended period of time to extract the FLAC links.")

    with open(os.path.join(temp_dir, "playlist.txt"), "w") as playlist_file:
        for i, song in enumerate(song_list):
            link = song.link
            # Fall back to mp3 if flac not available
            if song.flac_link == "":
                sel_album.songs[i].flac_link = get_flac_link(sel_album.songs[i].link)
                link = sel_album.songs[i].flac_link
            
            playlist_file.write(link + "\n")

def parse_alb_page(sel_album : album):
    url = sel_album.link

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        all_tr = soup.find_all("tr")

        song_list = []

        for tr in all_tr:
            if "play track" in str(tr.get_text):
                song_list.append(parse_song(tr))

        return song_list

    else:
        logging.info(
            f"Failed to fetch the content. HTTP status code: {response.status_code}")

def parse_song(tr: BeautifulSoup) -> song:
    cells = tr.find_all("td")

    # Extract the relevant data from the cells
    title_cell = cells[3].find("a")
    title = title_cell.text
    link = title_cell["href"]
    link = decode_percent_encoding(link)

    # Check if the title is a timestamp
    if re.match(r"\d{1,2}:\d{1,2}", title):
        # If it is, use the title from the previous cell instead
        title = cells[2].text.strip()

    return song(title, link)

def get_flac_link(song_link: str):
    if not song_link.startswith(url_base):
        song_link = url_base + song_link

    # Send an HTTP GET request to the URL
    response = requests.get(song_link)

    link = song_link

    if "%25" in link or "%20" in link:
        link = decode_percent_encoding(link)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        for p in soup.find_all("p"):
            try:
                if "FLAC" in str(p.find("a").find("span").get_text):
                    link= decode_percent_encoding(str(p.find("a").get_text).split("href=\"")[1].split("\">")[0])
            except:
                pass
    
    return link

def decode_percent_encoding(s: str):
    if "%2523" in s:
        return s
    elif "%20%23" in s:
        return s
    else:
        s = s.replace('%25', '%')
        s = unquote(s)
        return s

def search():
    while (True):
        query = ""
        while (True):
            query = input("Search for an album (q to exit): ")
            if query == "q" or query == "quit":
                sys_exit(0)
            
            if len(query) < 3:
                logging.info("Your search query must be 3 characters or longer.")
            else:
                break

        url = url_base + f"/search?search={query}"

        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            all_tr = soup.find_all("tr")

            album_list = []

            for tr in all_tr:
                if "albumIcon" in str(tr.get_text):
                    try:
                        album_list.append(parse_search(tr))
                    except:
                        logging.info(f"ERROR: Failed to parse album \n{tr.text}")

            selection = select(album_list, "Albums")
            if selection != "q":
                return album_list[selection]

        else:
            logging.info(
                f"Failed to fetch the content. HTTP status code: {response.status_code}")

def parse_search(tr: BeautifulSoup) -> album:
    # Find all <td> tags in the table row
    cells = tr.find_all("td")

    # Extract the relevant data from the cells
    title = cells[1].find("a").text.strip()
    platforms = cells[2].text.strip()
    album_type = cells[3].text.strip()
    year = cells[4].text.strip()
    link = cells[0].find("a")["href"]

    return album(title, platforms, album_type, year, link)

def select(inputlist: list, selectiontype: str):
    for j, name in enumerate(inputlist):
        print(f"[{j + 1}] {name}")

    while (True):
        selection = input(
            f"Make a selection of {selectiontype} [1-{len(inputlist)}] (q to exit): ")

        if selection.isdigit():
            if int(selection) in range(1, len(inputlist) + 1):
                break

        if selection == "q":
            break

    if selection == "q":
        return selection

    selection = int(selection) - 1

    logging.info(f"Selection made: {inputlist[selection]}")
    return selection

def sanitize_filename(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleaned_filename = ''.join(c for c in filename if c in valid_chars)
    return cleaned_filename

def sys_exit(code: int):
    on_exit()
    sys.exit(code)

def on_exit():
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)

if __name__ == "__main__":
    main()
