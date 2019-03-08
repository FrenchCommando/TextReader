import os
import argparse
from TextReader import run_application, set_line_split, set_word_split

set_line_split(.1)
set_word_split(.1)

parser = argparse.ArgumentParser()
parser.add_argument('--text_dir', help='folder path')
args = parser.parse_args()

print(args)
text_dir = os.path.expanduser('~/') if args.text_dir is None else args.text_dir
print("Text Directory", text_dir)


map_to_text = {u: lambda u=u: open(os.path.join(text_dir, u), "r")
               for u in os.listdir(text_dir) if os.path.isfile(os.path.join(text_dir, u))}
run_application(library=map_to_text, name="FileTextReader")
