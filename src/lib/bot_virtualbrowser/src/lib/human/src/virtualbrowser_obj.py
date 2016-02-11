#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>
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

""" Componenti principali del browser """

import logging

from bs4 import BeautifulSoup

import requests2
import requests
import version


# Configurazione del sistema di logging
logger = logging.getLogger(version.lib_name)
logger.addHandler(logging.NullHandler())


class Window(object):
	"""Una finestra del browser"""
	
	def __init__(self, parent_browser, window_id, tabs_manager_class):
		"""
		Crea una nuova finestra, con dentro una scheda vuota
		
		Parameters
		----------
		parent_browser : virtualbrowser.Browser
			Il browser che ha aperto questa finestra
		window_id : str
			Un identificatore per la finestra, di solito generato automaticamente
			dall'oggetto WindowsManager
		tabs_manager_class : managers.TabsManager
			La classe del gestore delle schede, è possibile specificare una classe
			derivata da managers.TabsManager
		"""
		
		logger.info("Aprendo una nuova finestra")
		
		# Prima di tutto, impostiamo le informazioni della finestra
		self.__set_parent_browser(parent_browser)
		self.__set_window_id(window_id)

		# Poi creiamo l'oggetto session
		self.session = self.new_session()

		# Impostiamo lo user agent predefinito per le nuove finestre
		self.set_session_ua(parent_browser.default_ua)

		# Ora creiamo il gestore delle schede
		logger.debug("Tabs manager class = %s", tabs_manager_class)
		self.tabs_manager = tabs_manager_class(self)
		
		# E per finire, apriamo una scheda vuota
		self.tabs_manager.add_tab()
		
	def __set_parent_browser(self, browser):
		"""Imposta il browser che ha creato questa finestra"""
		self.__parent_browser = browser

	def get_parent_browser(self):
		"""Restituisce il browser che ha creato questa finestra"""
		return self.__parent_browser

	def __set_window_id(self, id_):
		"""Imposta un identificatore per questa finestra"""
		self.__window_id = id_
		logger.debug("Window id: %s", id_)

	def get_window_id(self):
		"""Restituisce l'idenficatore di questa finestra"""
		return self.__window_id

	def new_session(self):
		"""Restituisce un nuovo oggetto requests2.Session"""
		return requests2.Session()

	def set_session_ua(self, ua):
		"""
		Cambia l'ua usato in questa finestra
		
		ATTENZIONE: l'ua verrà salvato nell'oggetto self.session, nel caso questo 
		fosse sostituito, l'ua dovrebbe essere reimpostato
		"""
		self.session.headers['User-Agent'] = ua
		logger.info("Ua aggiornato nella finestra %s: %s", self.win_id, ua)

	def get_session_ua(self):
		"""Restituisce l'ua usato in questa finestra"""
		return self.session.headers['User-Agent']

	def close(self):
		"""Chiude questa finestra"""
		logger.info("Chiudendo la finestra %s", self.win_id)
		
		# Prima dobbiamo chiudere tutte le schede aperte in questa finestra

		# Attenzione, non si può usare direttamente la lista delle schede:
		#
		# for tab_id in self.tabs_manager.tabs:
		# RuntimeError: dictionary changed size during iteration
		tabs = tuple(self.tabs_manager.tabs.values())
		
		for tab in tabs:
			 tab.close(closing_window=True)
		
		# E ora chiudiamo questa finestra
		self.parent_browser.windows_manager.remove_window(self.win_id)

	parent_browser = property(get_parent_browser)
	session_ua = property(get_session_ua, set_session_ua)
	win_id = property(get_window_id)


class Tab(object):
	"""Una scheda"""
	
	def __init__(self, parent_window, tab_id, url=None):
		"""
		Parameters
		----------
		parent_window : Window
			La finestra nella quale è aperta questa scheda
		tab_id : str
			Identificatore per la scheda, generato da un oggetto TabsManager
		url : str
			Url al quale punta la scheda, può anche essere impostato in seguito
		"""
		logger.info("Aprendo una nuova scheda")
		
		# Impostiamo le informazioni su questa scheda
		self.__set_parent_window(parent_window)
		self.__set_tab_id(tab_id)

		# Definiamo l'url al quale punta
		self.set_url(url)

		# Creiamo la variabile con il contenuto della scheda
		self.__init_content()

	def __set_parent_window(self, window):
		"""Imposta la finestra nella quale è aperta questa scheda"""
		self.__parent_window = window
		logger.debug("La finestra genitore è: %s", self.parent_window.win_id)

	def get_parent_window(self):
		"""Restituisce la finestra nella quale è aperta questa scheda"""
		return self.__parent_window
		
	def __set_tab_id(self, tab_id):
		"""Imposta un identificatore per questa scheda"""
		self.__tab_id = tab_id
		logger.debug("Tab id: %s", tab_id)

	def get_tab_id(self):
		"""Restituisce l'identificatore di questa scheda"""
		return self.__tab_id

	def set_url(self, url):
		"""Imposta l'url al quale punta la scheda"""
		self.__url = url
		logger.info("Impostato l'url %s nella scheda %s", url, self.tab_id)
		
	def get_url(self):
		"""Restituisce l'url al quale punta la scheda"""
		return self.__url

	def __init_content(self):
		"""
		METODO DA CHIAMARE IN __init__
		Va creata una variabile usata da get_content e download_content: la variabile
		è creata anche da download_content, ma se venisse chiamato get_content prima 
		di download_content si otterrebbe un errore
		"""
		self.__content = None
		
	def download_content(self):
		"""
		Imposta il contenuto della scheda, scaricando il contenuto dell'url impostato
		"""
		logger.info("Scaricando il contenuto della scheda %s", self.tab_id)
		self.__content = self.parent_window.session.get2(self.url)

	def get_content(self):
		"""Restituisce il contenuto della scheda"""
		return self.__content
		
	def get_bs_content(self):
		"""Restituisce il contenuto della scheda, in un oggetto BeautifulSoup"""
		ret = None
		
		# Se la pagina non è ancora stata caricata, self.content è None
		# Ma non possiamo passare direttamente None a BeautifulSoup, va sostituito
		# con una stringa vuota, che comunque ha lo stesso significato logico
		
		if self.content is None:
			ret = BeautifulSoup("", lxml)
		else:
			ret = BeautifulSoup(self.content.text, "lxml")
			
		return ret

	def re_load(self):
		"""Ricarica il contenuto della scheda"""
		logger.info("Ricaricando la scheda %s", self.tab_id)
		self.download_content()
		
	def post(self, url, data=None, **kwargs):
		"""Collegamento a requests.Session.post"""
		return self.parent_window.session.post(url, data, **kwargs)
	
	def close(self, closing_window=False):
		"""
		Chiude la scheda
		Se è l'ultima scheda della finestra, chiude anche la finestra
		
		Parameters
		----------
		closing_window : bool
			Significa che questa scheda deve essere chiusa perché la finestra 
			alla quale appartiene deve essere chiusa; quindi anche se è l'ultima
			scheda non chiamerà il metodo di chiusura della finestra, perché già 
			sta per essere chiusa
		"""
		is_last_tab = (len(self.parent_window.tabs_manager.tabs) == 1)
		logger.info("Chiudendo la scheda %s", self.tab_id)
		
		# Se è l'ultima scheda, chiude anche la finestra
		# ... se non la si sta già chiudendo
		if (is_last_tab and (not closing_window)):
			logger.info("È l'unica scheda nella finestra, verrà chiusa la finestra")
			self.parent_window.close()
			
		else:
			# Chiude la scheda
			self.parent_window.tabs_manager.remove_tab(self.tab_id)


	parent_window = property(get_parent_window)
	bs_content = property(get_bs_content)
	content = property(get_content)
	tab_id = property(get_tab_id)
	url = property(get_url, set_url)
