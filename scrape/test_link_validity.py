# NetRank

import urllib2, sys

OUTPUT_FILE = open("team_urls.out", "w")

def get_redirected_url(url):
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    request = opener.open(url)
    return request.url

if __name__ == "__main__":

    i = 1
    for link in sys.stdin:
        link = link.replace("\n","")
        redir_link = get_redirected_url(link)
        if redir_link != link:
            print("link: " + str(link))
            print("redir_link: " + str(redir_link))
            print("ERROR: " + link)
        else:
            OUTPUT_FILE.write(link + "\n")
        print(str(i))
        i += 1

    OUTPUT_FILE.close()
