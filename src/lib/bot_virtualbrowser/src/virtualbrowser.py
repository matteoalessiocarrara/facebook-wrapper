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

""" Browser """

import logging

from lib.human.src import virtualbrowser
from lib.human.src import version as virtualbrowser_version

import managers
import version


# configurazione del sistema di logging
logger = logging.getLogger(version.lib_name)
logger.addHandler(logging.NullHandler())


# TODO Migliorare il sistema di controllo della versione
if virtualbrowser_version.version_major != version.virtualbrowser_version_required:
	n = virtualbrowser_version.lib_name
	r = version.virtualbrowser_version_required
	f = virtualbrowser_version.version_major
	e = "Versione di %s incompatibile, richiesta %s, trovata %s" % (n, r, f)

	raise NotImplementedError(e)


class BotBrowser(virtualbrowser.Browser):

	def __init__(self, default_ua=virtualbrowser.DEFAULT_UA):
		"""
		Apre un browser, quindi apre anche una finestra del browser
		
		Parameters
		----------
		default_ua : str
			Imposta l'ua predefinito per le nuove finestre
			
		"""
		
		# Usiamo il nostro windows manager
		super(BotBrowser, self).__init__(default_ua, wm_class=managers.BotWindowsManager)
		
		
