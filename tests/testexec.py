# https://stackoverflow.com/questions/3906232/python-get-the-print-output-in-an-exec-statement
import sys
from io import StringIO
import io
import contextlib

file = 'testsum.py'
with open(file, 'r', encoding='utf-8') as file:
    lines = file.read()

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

with stdoutIO() as s:
    exec(lines, {'a': 1, 'b': 2})

print("out:", s.getvalue())

print(repr(lines))