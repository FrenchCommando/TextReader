from io import StringIO
from TextReader import run_application, set_line_split, set_word_split
import newspaper

set_line_split(.1)
set_word_split(.1)

url = 'https://www.npr.org/'
url = 'https://www.breitbart.com/'


def get_content_safe(p):
    print(p)
    try:
        article = map_articles[p]
        print(article.url)
        article.download()
        article.parse()
        return StringIO(article.text)
    finally:
        print("Done", p)


paper = newspaper.build(url=url)
map_articles = {p.url: p for p in paper.articles}
map_content = {p: lambda p=p: get_content_safe(p) for p in map_articles}

run_application(library=map_content, name="NewsReader")
