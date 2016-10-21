#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>

from sys import argv
import fbwrapper


try:
	username, password = argv[1:3]
except IndexError:
	exit("Uso: test.py username password")


fbwrapper.Facebook(username, password)