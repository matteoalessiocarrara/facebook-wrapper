#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>

import json
import logging
from sys import argv

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *


class Facebook:
	
	def __init__(self, username, password):
		self.__init_driver()
		self.__login(username, password)


	def __init_driver(self):
		firefoxCap = DesiredCapabilities.FIREFOX
		firefoxCap["marionette"] = True
		self.__driver = webdriver.Firefox(capabilities = firefoxCap)

		
	def get_driver(self):
		return self.__driver		

	
	def __login(self, username, password):
		self.get_driver().get("https://mbasic.facebook.com")
		self.get_driver().find_element_by_name("email").send_keys(username)
		self.get_driver().find_element_by_name("pass").send_keys(password)
		self.get_driver().find_element_by_name("login").click()
		WebDriverWait(self.get_driver(), 10).until(EC.title_is("Facebook"))
		
		
	def get_profile(self, url):
		return Profile(self, url)


class Profile:

	def __init__(self, facebook_object, url, url_is_id=False):
		"""Url senza prefisso"""
		self.__url = url
		self.__url_is_id = url_is_id
		self.__f = facebook_object
		
	def get_likes(self):
		if not self.__url_is_id:
			URL = "https://www.facebook.com/" + self.__url + "/likes"
		else:
			URL = "https://www.facebook.com/" + self.__url + "&sk=likes"

		self.__f.get_driver().get(URL)
		if self.__f.get_driver().current_url != URL:
			logging.warning("Il profilo " + self.__url + " non permette la visione dei mi piace")
			return []
		
		likes = []
		while True:	
			try:
				self.__f.get_driver().find_element_by_xpath("id('timeline-medley')/div/div[2]/div[1]/div/div/h3")
				likes = self.__f.get_driver().find_elements_by_xpath("id('pagelet_timeline_medley_likes')/div[2]/div[1]/ul/li/div/div/div/div/div[2]/div[1]/a")
				break
			except NoSuchElementException:
				self.__f.get_driver().execute_script("window.scrollTo(0, document.body.scrollHeight);")
		
		logging.info("Copiando elaborando i like trovati (%d)" % len(likes))
		ret = []
		for like in likes:
			t = like.text
			logging.debug(t)
			ret.append(t)
			
		return ret
		