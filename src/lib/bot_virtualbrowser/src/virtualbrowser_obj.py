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

from lib.human.src import virtualbrowser_obj
from lib.human.src import version as virtualbrowser_version

import version


# configurazione del sistema di logging
logger = logging.getLogger(version.lib_name)
logger.addHandler(logging.NullHandler())


if virtualbrowser_version.version_major != version.virtualbrowser_version_required:
	n = virtualbrowser_version.lib_name
	r = version.virtualbrowser_version_required
	f = virtualbrowser_version.version_major
	e = "Versione di %s incompatibile, richiesta %s, trovata %s" % (n, r, f)

	raise NotImplementedError(e)


class BotWindow(virtualbrowser_obj.Window):
	"""Una finestra del browser"""
	
	def get(self, url):
		"""
		Apre una scheda, scarica la pagina, chiude la scheda
		Restituisce il contenuto della pagina
		
		Utile quando si deve scaricare velocemente una sola pagina
		"""
		
		tab = self.tabs_manager.add_tab(url)
		ret = tab.load()
		tab.close()
		
		return ret
		
	def bs_get(self, url):
		"""
		Apre una scheda, scarica la pagina, chiude la scheda
		Restituisce il contenuto della pagina, in un oggetto BeautifulSoup
		
		Utile quando si deve scaricare velocemente una sola pagina
		"""
		tab = self.tabs_manager.add_tab(url)
		ret = tab.bs_load()
		tab.close()
		
		return ret
	

class BotTab(virtualbrowser_obj.Tab):
	"""Una scheda"""
	
	def load(self, url=None):
		"""
		Imposta l'url, e carica il contenuto della scheda
		Restituisce il contenuto della scheda
		"""

		# imposta l'url, se specificato
		if url is not None:
			self.set_url(url)

		# carica la scheda
		self.download_content()

		# restituisce il contenuto della scheda
		return self.get_content()
		
	def bs_load(self, url=None):
		"""
		Imposta l'url, e carica il contenuto della scheda
		Restituisce il contenuto della scheda, in un oggetto BeautifulSoup
		"""
		# carica la scheda
		self.load(url)

		# restituisce il contenuto, in versione "oggetto BeautifulSoup"
		return self.get_bs_content()
