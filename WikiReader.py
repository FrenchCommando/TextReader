from wikipedia import page, random, exceptions
from io import StringIO
from TextReader import run_application, set_line_split, set_word_split

set_line_split(.1)
set_word_split(.1)


def get_content_safe(p):
    print(p)
    try:
        return StringIO(page(p).content)
    except exceptions.DisambiguationError as E:
        selected_p = str(E).splitlines()[1]
        print(E)
        return StringIO(page(selected_p).content)


n = 5
map_content = {p: lambda p=p: get_content_safe(p) for p in random(n)}

run_application(library=map_content)
