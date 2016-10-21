#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>

from sys import argv
import logging

import fbwrapper


try:
	username, password, profile = argv[1:4]
except IndexError:
	exit("Uso: test.py username password profile")

logging.getLogger().setLevel(logging.DEBUG)
print(fbwrapper.Facebook(username, password).get_profile(profile).get_likes())