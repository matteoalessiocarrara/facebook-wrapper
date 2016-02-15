#!/usr/bin/python2
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

""" Oggetti che gestiscono liste di oggetti """

import logging

from lib.human.src import managers
from lib.human.src import version as virtualbrowser_version

import virtualbrowser_obj
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


class BotTabsManager(managers.TabsManager):
	"""Gestore delle schede"""
	
	def add_tab(self, url=None):
		"""
		Crea una nuova scheda, e restituisce la scheda creata

		Parameters
		----------
		url : str
			Url al quale punta la scheda, può anche essere impostato in seguito
		"""
		
		# Usiamo la nostra classe BotTab
		return super(BotTabsManager, self).add_tab(url, tab_class=virtualbrowser_obj.BotTab)
		
		
class BotWindowsManager(managers.WindowsManager):
	"""Gestisce le finestre del browser"""
	
	def add_window(self):
		"""
		Crea una nuova finestra
		Restituisce la finestra creata
		"""
		
		# usiamo la nostra classe BotWindow e BotTabsManager
		return super(BotWindowsManager, self).add_window(window_class=virtualbrowser_obj.BotWindow,
														tabs_manager_class=BotTabsManager)

