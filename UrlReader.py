import urllib3
from bs4 import BeautifulSoup
from io import StringIO
from TextReader import run_application, set_line_split, set_word_split

set_line_split(.1)
set_word_split(.1)

http = urllib3.PoolManager()


def get_content_safe(p):
    print(p)
    try:
        r = http.request('GET', p)
        soup = BeautifulSoup(r.data, "html.parser")
        text = soup.get_text()
        return StringIO(text)
    finally:
        print("Done", p)


quote_page = "https://www.crummy.com/software/BeautifulSoup/bs4/doc/"
q2 = "http://www.lefigaro.fr/"
urls = [quote_page, q2]
map_content = {p: lambda p=p: get_content_safe(p) for p in urls}

run_application(library=map_content, name="UrlReader")
