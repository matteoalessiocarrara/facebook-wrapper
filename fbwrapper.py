#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>

import json
from sys import argv

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Facebook:
	
	def __init__(self, username, password):
		self.__init_driver()
		self.__login(username, password)
		
	
	def __init_driver(self):
		firefoxCap = DesiredCapabilities.FIREFOX
		firefoxCap["marionette"] = True
		self.__driver = webdriver.Firefox(capabilities = firefoxCap)

	
	def __login(self, username, password):
		self.__driver.get("https://mbasic.facebook.com")
		self.__driver.find_element_by_name("email").send_keys(username)
		self.__driver.find_element_by_name("pass").send_keys(password)
		self.__driver.find_element_by_name("login").click()