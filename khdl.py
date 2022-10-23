import requests, subprocess, sys, validators, os, eyed3
from html.parser import HTMLParser
from html.entities import name2codepoint

ver = "b1.0"

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

def toValidFileName(input:str):
    input_split = []
    output_dir = input
    for char in ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]:
        if char in output_dir:
            dir_split = output_dir.split(char)
            output_dir = ""
            for x in dir_split:
                output_dir += x
    return output_dir

def help_message():
    print('''
Welcome to khinsider-streamer beat 1.0!
    
To run, you can simply execute `python3 khdl.py`.

The program will then prompt you to search for an album.

Once an album is selected, the program will create a playlist in mpv and start streaming each song from the album.

Custom arguments:
* you may specify the mode (either stream or download)
* Examples: 

`python3 khdl.py dl`

`python3 khdl.py stream`
''')
    sys_exit()

mode = "stream"
format = "mp3"
link = ""
search = True

if len(sys.argv) > 1:
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
                search = False
            else:
                print(testlink)
                print("Error! Invalid link provided.")
                sys_exit()

        elif sys.argv[j] == "stream" or sys.argv[j] == "dl":
            mode = sys.argv[j]

        elif sys.argv[j] == "help" or sys.argv[j] == "h":
            help_message()
    
if not validators.url(link) and not search:
    print("Please provide a valid link.")
    sys_exit()

prefix = "https://downloads.khinsider.com"
link_list = []

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if len(attr) > 1:
                if str(attr[1]).endswith(".mp3"):
                    if (prefix + attr[1]) not in link_list:
                        link_list.append(prefix + attr[1])

search_list = []

class MySearchParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        #print("Start tag:", tag)
        for attr in attrs:
            #print("     attr:", attr)
            if len(attr) > 1:
                if str(attr[1]).startswith("/game-soundtracks/album/"):
                    if (prefix + attr[1]) not in link_list:
                        link_list.append(prefix + attr[1])

    def handle_data(self, data):
        if not data.isspace():
            search_list.append(data)

data_list = []

grouping = []

class MyTRParser(HTMLParser):
    def handle_endtag(self, tag):
        if tag == 'tr':
            data_list.append(tag)

    def handle_data(self, data):
        if not data.isspace():
            grouping[len(data_list)-1].append(data)

search2 = True

while(True):

    query = ""
    if (search2):
        query = input("Search: ")
        if query == "q" or query == "quit":
            sys_exit()
        if len(query) < 3:
            print("Your search query must be 3 characters or longer!")
            query = "a"

    while(search2):
        link_list = []
        query_split = query.split(" ")
        query = ""
        for q in query_split:
            query += q + "+"

        link = "https://downloads.khinsider.com/search?search="+query

        r = requests.get(link)

        with open(temp_dir + "/temp.html", "wb") as w_file:
            w_file.write(r.content)

        w_file.close()

        parser = MySearchParser()

        with open(temp_dir + '/temp.html', 'r', encoding='utf-8') as myFile:
            data = myFile.read()

        parser.feed(data)

        myFile.close()

        title_list = []
        
        data_list = []
        grouping = []
        for m in range(0, len(link_list)+1):
            grouping.append([])

        parser = MyTRParser()

        parser.feed(data)

        title_str = "N/A  "

        counter = 0
        for z in range(len(grouping)-(len(link_list)+1), len(grouping)-1):
            title_str = ""
            for v in grouping[z]:
                title_str += v + " "
            title_list.append(title_str)

        '''for l in link_list:
            l_split = l.split("/")
            title_list.append(l_split[-1])'''

        for t in range(0, len(title_list)):
            print("[" + str(t+1) + "] " + title_list[t])
        
        while(True):
            selection = input("Select a album number, or search again. \"q\" to quit: ")
            if selection == "q" or selection == "quit":
                sys_exit()
            elif selection.isdigit():
                if int(selection)-1 in range(0, len(title_list)):
                    print("Selection made: " + title_list[int(selection)-1])
                    link = link_list[int(selection)-1]
                    search2 = False
                    break
            else:
                query = selection
                if len(query) < 3:
                    print("Your search query must be 3 characters or longer!")
                    query = "a"
                break


        link_list = []

    r = requests.get(link)

    with open(temp_dir + "/temp.html", "wb") as w_file:
        w_file.write(r.content)

    w_file.close()

    parser = MyHTMLParser()

    with open(temp_dir + '/temp.html', 'r', encoding='utf-8') as myFile:
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
            output_dir = toValidFileName(eyed3tempfile.tag.album)

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
                title = toValidFileName(eyed3tempfile.tag.title)

            
            os.replace(temp_file, output_dir + "/" +
                    str(i+1).zfill(num_0) + ". " + title + "." + format)


    elif mode == 'stream' and format == 'mp3':
        playlist = ""
        for e in range(0, len(link_list)):
            playlist += link_list[e] + "\n"

        if os.path.isfile(temp_dir + "/playlist.txt"):
            os.remove(temp_dir + "/playlist.txt")
        
        open(temp_dir + "/playlist.txt", 'x')

        with open(temp_dir + "/playlist.txt", 'w') as playlist_file:
            playlist_file.write(playlist)
        playlist_file.close()
        
        subprocess.run(["mpv", "--playlist="+temp_dir + "/playlist.txt"])
    
    if not search:
        break
    else:
        search2 = True


sys_exit()