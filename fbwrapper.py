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
from selenium.webdriver.common.by import By


class Facebook:
	MAX_PAGE_LOADING_TIME = 120
	
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
		WebDriverWait(self.get_driver(), self.MAX_PAGE_LOADING_TIME).until(EC.title_is("Facebook"))
		
		
	def get_profile(self, url):
		return Profile(self, url)
		

	def people_search(self, query, max_items=None):
		self.get_driver().get("https://www.facebook.com")
		self.get_driver().find_element_by_name("q").send_keys(query)
		self.get_driver().find_element_by_name("q").send_keys(Keys.ENTER)

		WebDriverWait(self.get_driver(), self.MAX_PAGE_LOADING_TIME).until(EC.visibility_of_element_located((By.ID, "browse_lhc_filter_pagelet")))
		
		try:
			self.get_driver().find_element_by_id("empty_result_error")
			return [{}]
		except NoSuchElementException:
			r = []
			links = []
			names = []
			
			try:
				# Andiamo alla lista completa
				self.get_driver().find_element_by_xpath("id('BrowseResultsContainer')/div[1]/div[3]/footer[1]/a[1]").click()
				WebDriverWait(self.get_driver(), self.MAX_PAGE_LOADING_TIME).until(EC.visibility_of_element_located((By.ID, "leftCol")))
				
				while (True):
					if (max_items != None) and (len(links) >= max_items):
						break

					links = self.get_driver().find_elements_by_xpath("id('pagelet_loader_initial_browse_result')/div[1]/div[1]//div/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/a[1]")
					names = self.get_driver().find_elements_by_xpath("id('pagelet_loader_initial_browse_result')/div[1]/div[1]//div/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/a[1]/div[1]")
				
					# XXX
					if self.get_driver().find_element_by_xpath("id('pagelet_loader_initial_browse_result')/div[1]/div[1]/div[last()]/div[1]/div[1]").text == "End of Results":
						break
					else:
						self.get_driver().execute_script("window.scrollTo(0, document.body.scrollHeight);")
					
			except NoSuchElementException:
				# C'è solo la prima pagina di risultati
				links = self.get_driver().find_elements_by_xpath("id('BrowseResultsContainer')/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/a[1]")
				names = self.get_driver().find_elements_by_xpath("id('BrowseResultsContainer')/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/a[1]/div[1]")
		
			for i in range(len(links)):
				if (max_items != None) and (len(r) == max_items):
					break
				else:
					r.append({"url": links[i].get_attribute("href"), "name": names[i].text})
			
			return r


class Profile:

	def __init__(self, facebook_object, url):
		"""Url senza prefisso facebook.com ne /"""
		self.__url = url
		self.__url_is_id = Profile.nick_is_id(url)
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
		
		logging.info("Elaborando i like trovati (%d)" % len(likes))
		ret = []
		for like in likes:
			t = like.text
			logging.debug(t)
			ret.append(t)
			
		return ret

		
	@staticmethod
	def nick_is_id(nick):
		return nick.startswith("profile.php?id=")
	
	
	@staticmethod
	def nick_from_url(url):
		"""https://facebook.com/foobar"""
		return url.split("/")[3].split("?")[0] if not Profile.nick_is_id(url.split("/")[3]) else url.split("/")[3]
	
	
		
