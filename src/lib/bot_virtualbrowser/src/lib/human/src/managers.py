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

""" Oggetti che gestiscono liste di oggetti """

import logging
import time

import virtualbrowser_obj
import version


# Configurazione del sistema di logging
logger = logging.getLogger(version.lib_name)
logger.addHandler(logging.NullHandler())

class Manager(object):
	"""
	Gestisce liste di oggetti associati ad id unici
	Ovvero dizionari nella forma: {'id_unico': oggetto, ...}
	"""

	def __init__(self):
		"""Attenzione!! Deve essere chiamato anche dalle classi derivate!!"""
		self.__init_id_system()
		self.__init_obj_dict()

	def __repr__(self):
		"""
		Questo oggetto viene rappresentato come un dizionario, con questa struttura:
		{'id_unico': oggetto, ...}
		"""
		return self.obj_dict

	def __init_id_system(self):
		"""Inizializza il sistema di creazione degli id unici"""
		# Si utilizza una variabile-contatore, una volta usato un id (un numero)
		# basta incrementare il contatore per avere un altro id unico
		self.__current_obj_id = 0

	def _get_new_obj_id(self):
		"""
		Restituisce un id unico per identificare un oggetto
		
		ATTENZIONE!! Una volta restituito, lo considera automaticamente come usato,
		quindi se si chiama due volte questo metodo si otterranno due id differenti
		"""
		# L'id attualmente libero
		# Deve essere una stringa. perché sarà la key di un dizionario
		free_id = str(self.__current_obj_id)
		
		# self.__current_obj_id lo restituiamo, quindi non è più disponibile
		# per avere un altro id unico basta aggiungere 1 (si passa al prossimo
		# numero/id)
		self.__current_obj_id += 1

		return free_id
		
	def __init_obj_dict(self):
		"""Crea il dizionario dove sono tenuti gli oggetti"""
		self.__obj_dict = {}

	def get_obj_dict(self):
		"""Restituisce il dizionario dove sono tenuti gli oggetti"""
		return self.__obj_dict

	def _add_obj(self, id_, obj):
		"""
		Aggiunge un oggetto al dizionario degli oggetti
		
		Parameters
		----------
		id_ : str
			Un id unico per identificare l'oggetto, generarlo con _get_new_obj_id()
		obj : object
			L'oggetto da aggiungere al dizionario
			
		Raises
		------
		KeyError
			Se l'id è già nel dizionario
		"""
		
		logger.debug("Aggiungendo un nuovo oggetto con id %s", id_)
		
		if self.__obj_dict.has_key(id_):
			e = "Impossibile aggiungere l'oggetto: id %s non valido, già nel dizionario" % id_
			
			logger.error(e)
			raise KeyError(e)
			
		else:
			self.__obj_dict[id_] = obj

	def _remove_obj(self, id_):
		"""
		Rimuove un oggetto dal dizionario degli oggetti
		
		Parameters
		----------
		id : str
			L'id dell'oggetto
			
		Raises
		------
		KeyError
			Non esistono oggetti con l'id specificato
		"""

		try:
			del self.__obj_dict[id_]
			logger.debug("Eliminato oggetto %s", id_)
			
		except KeyError:
			e = "Impossibile eliminare l'oggetto, id %s non valido" % id_
			d = "Id validi: %s" % self.obj_dict.keys()
			
			logger.error(e)
			logger.debug(d)
			raise KeyError(e)

	obj_dict = property(get_obj_dict)

class TabsManager(Manager):
	"""Gestore delle schede"""
	
	def __init__(self, parent_window):
		"""
		Parameters
		----------
		parent_window : virtualbrowser_obj.Window
			La finestra alla quale appartiene questo gestore delle schede
		"""
		super(TabsManager, self).__init__()
		self.__set_parent_window(parent_window)

	def __set_parent_window(self, window):
		"""Imposta la finestra alla quale appartiene questo gestore delle schede"""
		self.__parent_window = window
		logger.debug("Id della finestra genitore: %s", self.parent_window.win_id)

	def get_parent_window(self):
		"""Restituisce la finestra alla quale appartiene questo gestore delle schede"""
		return self.__parent_window

	# Tenere aggiornata la docstring, controllare quella di virtualbrowser_obj.Tab
	def add_tab(self, url=None, tab_class=virtualbrowser_obj.Tab):
		"""
		Crea una nuova scheda, e restituisce la scheda creata

		Parameters
		----------
		url : str
			Url al quale punta la scheda, può anche essere impostato in seguito
		tab_class : virtualbrowser_obj.Tab
			Si può specificare la classe della nuova scheda, dovrebbe
			eventualmente essere derivata da virtualbrowser_obj.Tab
		"""
		
		# Assegna un id alla nuova scheda
		id_ = self._get_new_obj_id()
		logger.debug("Id della nuova scheda: %s", id_)

		# Crea la nuova scheda
		logger.debug("Classe della nuova scheda = %s", tab_class)
		tab = tab_class(self.parent_window, id_, url)

		# La aggiunge alla lista delle schede
		self._add_obj(id_, tab)

		# Restituisce la scheda creata
		return tab

	def remove_tab(self, id_):
		"""Rimuove una scheda dalla lista delle schede"""
		logger.debug("Rimuovendo la scheda %s", id_)
		self._remove_obj(id_)

	def reload_tabs(self):
		"""Ricarica tutte le schede nella finestra"""
		logger.info("Ricaricando le schede della finestra %s", self.parent_window.win_id)
		
		for tab in self.tabs.values():
			tab.re_load()

	def get_tabs(self):
		"""Restituisce il dizionario con le schede"""
		return self.get_obj_dict()

	parent_window = property(get_parent_window)
	tabs = property(get_tabs)
	

class WindowsManager(Manager):
	"""Gestisce le finestre del browser"""
	
	def __init__(self, parent_browser):
		"""
		Parameters
		----------
		parent_browser : virtualbrowser.Browser
			Il browser al quale appartiene questo gestore delle finestre
		"""
		super(WindowsManager, self).__init__()
		self.__set_parent_browser(parent_browser)

	def __set_parent_browser(self, parent_browser):
		"""Imposta il browser al quale appartiene questo gestore delle finestre"""
		self.__parent_browser = parent_browser

	def get_parent_browser(self):
		"""Restituisce il browser al quale appartiene questo gestore delle finestre"""
		return self.__parent_browser

	def add_window(self, window_class=virtualbrowser_obj.Window, tabs_manager_class=TabsManager):
		"""
		Crea una nuova finestra
		Restituisce la finestra creata

		Parameters
		----------
		window_class : virtualbrowser_obj.Window
			Eventualmente, si può usare una classe derivata da virtualbrowser_obj.Window
			per la nuova finestra
		tabs_manager_class : managers.TabsManager
			La classe del gestore delle schede per la nuova finestra
		"""

		logger.debug("Classe della nuova finestra: %s", window_class)

		id_ = self._get_new_obj_id()
		logger.debug("Id della nuova finestra: %s", id_)

		window = window_class(self.parent_browser, id_, tabs_manager_class)
		
		# Aggiunge la finestra alla lista delle finestre
		self._add_obj(id_, window)

		# Restituisce la finestra creata
		return window

	def remove_window(self, id_):
		"""Rimuove una finestra dalla lista delle finestre"""
		
		# ATTENZIONE: eventuali procedure di chiusura dovranno essere contenute
		# nell'oggetto Window
		# Questo metodo si occupa solo di rimuovere la finestra dalla lista delle
		# finestre

		# XXX Chiudendo l'ultima finestra, si dovrebbe chiudere anche il browser
		# ma non lo possiamo chiudere... che si fa? Lasciamo un browser senza finestre?
		
		logger.debug("Rimuovendo la finestra %s", id_)
		self._remove_obj(id_)

	def get_windows(self):
		"""Restituisce la lista delle finestre"""
		return self.get_obj_dict()

	parent_browser = property(get_parent_browser)
	windows = property(get_windows)



