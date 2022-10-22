import requests, subprocess, sys, validators, os, eyed3
from html.parser import HTMLParser
from html.entities import name2codepoint

temp_dir = "khdl-temp"

if (os.path.isdir(temp_dir)):
    for file in os.listdir(temp_dir):
        os.remove(temp_dir + "/" + file)

if (os.path.isdir(temp_dir)) == False:
    os.mkdir(temp_dir)

def sys_exit():
    for file in os.listdir(temp_dir):
        os.remove(temp_dir + "/" + file)

    os.rmdir(temp_dir)

    sys.exit(0)

def help_message():
    print('''
    
To run, you can simply execute `python3 khdl.py [album link]`.

This will create a playlist in mpv and start streaming each song from the album.

Custom arguments:
* you may specify the mode (either stream or download)
* Examples: 

`python3 khdl.py dl [album link]`

`python3 khdl.py stream [album link]`
''')
    sys_exit()

mode = "stream"
format = "mp3"
link = ""

if len(sys.argv) == 1:
    help_message()
elif len(sys.argv) > 1:
    for j in range(1, len(sys.argv)):
        if "." in sys.argv[j]:
            testlink = ""

            if "http://" in sys.argv[j]:
                testlink += "https://" + sys.argv[j][7:]
            elif "https://" not in sys.argv[j]:
                testlink += "https://" + sys.argv[j]
            else:
                testlink += sys.argv[j]

            if validators.url(testlink):
                link = testlink
            else:
                print(testlink)
                print("Error! Invalid link provided.")
                sys_exit()

        elif sys.argv[j] == "stream" or sys.argv[j] == "dl":
            mode = sys.argv[j]

        elif sys.argv[j] == "help" or sys.argv[j] == "h":
            help_message()
    
if not validators.url(link):
    print("Please provide a valid link.")
    sys_exit()

r = requests.get(link)

with open(temp_dir + "/temp.html", "wb") as w_file:
    w_file.write(r.content)

w_file.close()

link_list = []

prefix = "https://downloads.khinsider.com"

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if len(attr) > 1:
                if str(attr[1]).endswith(".mp3"):
                    if (prefix + attr[1]) not in link_list:
                        link_list.append(prefix + attr[1])

parser = MyHTMLParser()

with open(temp_dir + '/temp.html', 'r') as myFile:
    data = myFile.read()

parser.feed(data)

myFile.close()

output_dir = "output"

if mode == "dl" and format == "mp3":
    
    num_0 = len(str(len(link_list)))

    temp_file = temp_dir + "/" + str(1).zfill(num_0) + "." + format

    subprocess.run(["yt-dlp", link_list[0], "-o", temp_file])

    eyed3tempfile = eyed3.load(temp_file)
    if eyed3tempfile.tag.album:
        output_dir = eyed3tempfile.tag.album

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    os.remove(temp_file)

    for i in range(0, len(link_list)):

        split = link_list[i].split("/")
        split = split[-1].split("%2520")

        title = ""
        for k in range(0, len(split)):
            if split[-1] == split[k]:
                title += split[k]
            else:
                title += split[k] + " "

        temp_file = output_dir + "/" + str(i+1).zfill(num_0) + "." + format

        subprocess.run(["yt-dlp", link_list[i], "-o", temp_file])

        eyed3tempfile = eyed3.load(temp_file)
        if eyed3tempfile.tag.title:
            title = eyed3tempfile.tag.title
        
        os.replace(temp_file, output_dir + "/" +
                  str(i+1).zfill(num_0) + ". " + title + "." + format)


elif mode == 'stream' and format == 'mp3':
    playlist = ""
    for e in range(0, len(link_list)):
        playlist += link_list[e] + "\n"

    open(temp_dir + "/playlist.txt", 'x')

    with open(temp_dir + "/playlist.txt", 'w') as playlist_file:
        playlist_file.write(playlist)
    playlist_file.close()
    
    subprocess.run(["mpv", "--playlist="+temp_dir + "/playlist.txt"])

sys_exit()