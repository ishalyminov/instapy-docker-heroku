import os
import sys

env = lambda name, default=None: os.environ.get(name, default)

#instapy_dir = env('INSTAPY_WORKSPACE')
#if instapy_dir is not None:
#    os.environ['INSTAPY_WORKSPACE'] = os.path.abspath(instapy_dir)
