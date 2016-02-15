#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
#  Copyright 2015 - 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

""" Browser """

import logging

from bs4 import BeautifulSoup
import requests

import virtualbrowser_obj
import requests2
import managers
import version


# Configurazione del sistema di logging
logger = logging.getLogger(version.lib_name)
logger.addHandler(logging.NullHandler())


# Ua usato nelle nuove finestre del browser, se non ne viene specificato un altro
DEFAULT_UA = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0"


class Browser(object):
	
	def __init__(self, default_ua=DEFAULT_UA, wm_class=managers.WindowsManager):
		"""
		Apre un browser, quindi apre anche una finestra del browser
		
		Parameters
		----------
		default_ua : str
			Imposta l'ua predefinito per le nuove finestre
		wm_class: managers.WindowsManager
			Si può specificare la classe del windows manager da usare
			
		"""
		
		logger.info("Aprendo il browser")
		
		# Imposta l'ua predefinito per le nuove finestre, prima di aprire una
		# finestra
		self.default_ua = default_ua

		# Crea il gestore delle finestre
		logger.debug("Windows manager class = %s", wm_class)
		self.windows_manager = wm_class(parent_browser=self)
		
		# Apre una finestra
		self.windows_manager.add_window()

	def set_default_ua(self, ua):
		"""Imposta lo user agent predefinito per le nuove finestre"""
		
		if ua == DEFAULT_UA:
			logger.info("L'ua per le nuove finestre è quello predefinito della libreria")
		else:
			logger.info("Verrà usato un ua personalizzato nelle nuove finestre: %s", ua)

		self.__default_ua = ua

	def get_default_ua(self):
		"""Restituisce lo user agent predefinito per le nuove finestre"""
		return self.__default_ua

	default_ua = property(get_default_ua, set_default_ua)
