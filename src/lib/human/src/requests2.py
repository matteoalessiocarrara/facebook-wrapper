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

""" Estensione della libreria requests """

import logging
import os

import requests

import version


# Configurazione del sistema di logging
logger = logging.getLogger(version.lib_name)
logger.addHandler(logging.NullHandler())


class Session(requests.Session):
	"""Versione modificata di requests.Session"""

	def __init__(self):
		super(Session, self).__init__()
		self.__set_owner_pid()
	
	def __set_owner_pid(self):
		"""Imposta il pid del processo creatore, ovvero quello attuale"""
		self.__owner_pid = os.getpid()
		logger.debug("Owner pid: %s", self.__owner_pid)
		
	def get_owner_pid(self):
		"""Restituisce il pid del processo creatore"""
		return self.__owner_pid

	def get2(self, url, **kwargs):
		"""
		Versione modificata di get
		
		* Controlla che questo oggetto non sia condiviso fra più processi
		* Crea un eccezione HTTPError quando necessario
		* Stampa informazioni di debug
		"""
		if os.getpid() != self.owner_pid:
			# STACCAAAA STACCAAAAAAAAAAH
			w = "Sembra che l'oggetto requests.Session sia utilizzato da più processi. Questo è sconsigliato e potrebbe creare dei problemi"
			logger.warning(w)

		if (url[:8] == "https://") and (os.getpid() != self.owner_pid):
			logger.info("Casini in arrivo... io ti avevo avvertito, auguri :)")
		
		ret = self.get(url, **kwargs)

		try:
			ret.raise_for_status()
		except requests.HTTPError as e:
			logger.error("url %s: %s ", url, e.message)
			logger.debug("<!-- ret.text -->\n%s", ret.text)
			raise

		return ret
	
	owner_pid = property(get_owner_pid)
