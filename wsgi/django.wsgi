import os
import sys

# redirect sys.stdout to sys.stderr for bad libraries like geopy that uses
# print statements for optional import exceptions.
sys.stdout = sys.stderr

from os.path import abspath, dirname, join
from site import addsitedir

path = addsitedir(abspath(join(dirname(__file__), "../libs")), set())
if path:
    sys.path = list(path) + sys.path

sys.path.insert(0, abspath(join(dirname(__file__), "../components")))
sys.path.insert(0, abspath(join(dirname(__file__), "../apps")))

# emulate manage.py path hacking.
sys.path.insert(0, abspath(join(dirname(__file__), "..//core/")))
sys.path.insert(0, abspath(join(dirname(__file__), "../")))

from django.core.handlers.wsgi import WSGIHandler

os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
from core.models import Question
application = WSGIHandler()


