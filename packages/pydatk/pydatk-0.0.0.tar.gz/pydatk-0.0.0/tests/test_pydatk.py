# OS agnostic - sets path to allow importing pydatk from src
# https://stackoverflow.com/a/34938623/25458574
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

# import pydatk
import pydatk as datk

# test
print(datk.dev.test_pkg('test pydatk'))
