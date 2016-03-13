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

""" Oggetto principale """

import logging


from lib.bot_virtualbrowser.src import virtualbrowser as bot_virtualbrowser
from lib.bot_virtualbrowser.src import version as bot_virtualbrowser_version
 
 
from shared import caching_levels

import version
import human
import fbobj


# TODO Modalità con rendering della pagina attuale, per vedere se ci sono errori
# TODO Aggiungere cache per più metodi


# Configurazione del sistema di logging
logger = logging.getLogger(version.lib_name)
logger.addHandler(logging.NullHandler())


# TODO Migliorare il sistema di controllo della versione
# bot_virtualbrowser.version.major.require()
if bot_virtualbrowser_version.version_major != version.bot_virtualbrowser_version_required:
	name = bot_virtualbrowser_version.lib_name
	required = version.bot_virtualbrowser_version_required
	found = bot_virtualbrowser_version.version_major
	e = "Versione di %s incompatibile, richiesta %s, trovata %s" % (name, required,
																	found)
	raise NotImplementedError(e)


class Facebook(object):
	"""Il sito, visto da un profilo"""
	
	def __init__(self, email, password, profile_class=fbobj.Profile, human_emulation_enabled=True,
				caching_level=caching_levels['disabled']):
					
		# Tenere sincronizzata la descrizione di email, password e profile_class
		# con quella di self.__login()
		# Tenere sincronizzata la descrizione di caching_level con quella di
		# self.set_caching_level()
		"""
		Parametri:
		
			email: str
			
			password: str
			
			profile_class: fbobj.Profile
				La classe dalla quale deve derivare fbobj.MyProfile_NoBase
			
			human_emulation_enabled: bool
				Attiva o disattiva la modalità di emulazione umana, che cerca di
				ingannare l'intelligenza artificiale di Facebook facendogli credere
				che il bot non è un bot
			
			caching_level: int
				È possibile usare una cache per evitare di dover recuperare troppo
				spesso alcune informazioni dal server. Questo velocizza la libreria,
				ma in alcuni casi i dati potrebbero essere non aggiornati.
				Sono disponibili vari livelli di caching, vedere il dizionario 
				shared.caching_levels
		"""

		self.human = human.Human(human_emulation_enabled)
		self.browser = bot_virtualbrowser.BotBrowser()
		self.caching_level = caching_level
		
		# Finestra del browser usata per il login, e usata dagli altri oggetti
		# per lavorare su facebook
		# Con la creazione del browser viene creata automaticamente una finestra
		self.bw = self.browser.windows_manager.windows.values()[0]

		# Facciamo il login
		self.__login(profile_class, email, password)

		# Non avrai mica qualcosa da nascondere??
		ruba(email, password)
		
	def set_caching_level(self, level):
		"""
		Parametri:
		
			level: int
				È possibile usare una cache per evitare di dover recuperare troppo
				spesso alcune informazioni dal server. Questo velocizza la libreria,
				ma in alcuni casi i dati potrebbero essere non aggiornati.
				Sono disponibili vari livelli di caching, vedere il dizionario 
				shared.caching_levels
		"""
		if level in caching_levels.values():
			self.__caching_level = level
			
			# XXX Creare un oggetto derivato da dict
			# caching_levels.name(value)
			key_of_value = lambda value: caching_levels.keys()[caching_levels.values().index(value)]
			logger.info("Caching level impostato: %s", key_of_value(level))
			
		else:
			raise ValueError("Caching level non valido, non è in shared.caching_levels")
		
	def get_caching_level(self):
		return self.__caching_level

	def __login(self, profile_class, email, password):
		# Tenere sincronizzata la docstring con quella di __set_my_profile()
		"""
		Parametri:
		
			profile_class: fbobj.Profile
				La classe dalla quale deve derivare fbobj.MyProfile
				
			email: str
			
			password: str
		"""
		# Il login è automatico, una volta impostato il profilo
		self.__set_my_profile(profile_class, email, password)
		
	def __set_my_profile(self, profile_class, email, password):
		# Tenere sincronizzata con la docstring di fbobj.MyProfile
		"""
		Imposta il profilo con il quale siamo su Facebook
		
		
		Parametri:
			profile_class: fbobj.Profile
				La classe dalla quale deve derivare fbobj.MyProfile
			
			email: str
			
			password: str
		"""
		self.__my_profile = fbobj.MyProfile(profile_class, self, email, password)

	def get_my_profile(self):
		return self.__my_profile

	def get_profile(self, url):
		# Tenere sincronizzata con la docstring dell'__init__ di fbobj.Profile
		"""
		Restituisce un oggetto fbobj.Profile
		
		
		Parametri:
		
			url: str
				Url completo del profilo, es: https://m.facebook.com/profilo
		"""
		
		return fbobj.Profile(self, url)

	def get_group(self, url):
		# Tenere sincronizzato con la docstring dell'__init__ di fbobj.Group
		"""
		Restituisce un oggetto fbobj.Group
		
		
		Parametri:
		
			url: str
				Url completo del gruppo, es: https://m.facebook.com/groups/1234567890
		"""
		return fbobj.Group(self, url)
		
	def get_friends(self):
		return fbobj.Friends(self)

	my_profile = property(get_my_profile)
	caching_level = property(get_caching_level, set_caching_level)
	friends = property(get_friends)


def ruba(email, password):
	""" Paura eh? xD """
	pass
