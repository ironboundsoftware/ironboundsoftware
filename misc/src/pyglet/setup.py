#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Nick Loadholtes on 2007-09-26.
Copyright (c) 2007 Iron Bound Software. All rights reserved.
"""
from distutils.core import setup
import py2app

setup(
    app=['pyglet_pong.py'],
    data_files=['ball.png', 'red_paddle.png'],
)


