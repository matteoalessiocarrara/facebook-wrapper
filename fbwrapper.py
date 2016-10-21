#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>

import json
from sys import argv

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Facebook:
	
	def __init__(self, username, password):
		__init_driver()
		__login(username, password)
		
	
	def __init_driver(self):
		firefoxCap = DesiredCapabilities.FIREFOX
		firefoxCap["marionette"] = True
		self.__driver = webdriver.Firefox(capabilities = firefoxCap)
	
	
	def __login(self, username, password):
		__driver.get("http://mbasic.facebook.com")