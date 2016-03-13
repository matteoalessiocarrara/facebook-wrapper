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

""" Essere umano virtuale """

import logging
import random
import time

import version

# TODO Mettere in repo separato, fa comodo anche per altri progetti

# Configurazione del sistema di logging
logger = logging.getLogger(version.lib_name)
logger.addHandler(logging.NullHandler())


class Human(object):
	"""Un essere umano virtuale :)"""
	
	def __init__(self, enabled=True):
		
		if enabled:
			self.enable()
		else:
			self.disable()
		
		self.brain = Brain(human=self)
		self.hand = Hand(human=self)
	
	def enable(self):
		logger.info("Essere umano attivato")
		self.enabled = True
		
	def disable(self):
		logger.info("Essere umano disattivato")
		self.enabled = False
		
	def do(self, min_time, max_time, msg=None):
		"""
		L'uomo sta facendo qualcosa. 
		Blocca il processo per un  tempo casuale compreso fra min_time e max_time 
		(in secondi)
		Stampa msg con logger.info()
		"""
		
		if self.enabled:
			logger.info("L'uomo sta facendo qualcosa")
			
			if msg != None:
				logger.info("%s", msg)
				
			logger.info("Tempo minimo %ss, tempo massimo %ss", min_time, max_time)
			time.sleep(random.choice(range(min_time, max_time)))


class HumanPart(object):
	"""Un pezzo di uomo"""
	
	def __init__(self, human):
		"""
		Imposta self.human
		
		
		Parametri:
		
			human: Human
				L'uomo al quale appartiene questo oggetto
		"""
		self.human = human 
		

class Brain(HumanPart):
	
		def __init__(self, human):
			# Tenere sincronizzata docstring con quella di HumanPart
			"""
			Parametri:
			
				human: Human
					L'uomo al quale appartiene questo cervello
			"""
			super(Brain, self).__init__(human)
	
		def process(self, min_time, max_time, msg=None):
			# Tenere sincronizzata la docstring con quella di human.do()
			"""
			L'uomo sta elaborando delle informazioni.
			Blocca il processo per un  tempo casuale compreso fra min_time e max_time 
			(in secondi)
			Stampa msg con logger.info()
			"""
			if self.human.enabled:
				logger.info("Il cervello sta elaborando delle informazioni")
				self.human.do(min_time, max_time, msg)


class Hand(HumanPart):
	
	# Unità di misura: caratteri al minuto
	writing_speeds = {
					'fast': 160,
					'moderate': 140,
					'slow': 92,
					'transcription': 132,
					'composition': 76,
					'professional': 240,
					'advanced': 480,
					'fastest': 864
					}
						
	def __init__(self, human, writing_speed=writing_speeds['fast']):
		# Tenere sincronizzata docstring con quella di HumanPart
		"""
		Parametri:
		
			human: Human
				L'uomo al quale appartiene questa mano
				
			writing_speed: int
				Velocità di scrittura, unità di misura caratteri al minuto. Ci sono
				alcuni valori predefinit nel dizionario self.writing_speeds
		"""
		super(Hand, self).__init__(human)
		self.writing_speed = writing_speed
	
	def set_writing_speed(self, characters_per_minute):
		if characters_per_minute > self.writing_speeds['fastest']:
			logger.error("%s caratteri al minuto? Non sei un umano, sei una macchina! ... e facebook banna le macchine :(", characters_per_minute)
		else:
			self.__characters_per_minute = characters_per_minute
	
	def get_writing_speed(self):
		return self.__characters_per_minute
	
	def write(self, text):
		"""Fa finta di scrivere il testo"""
		
		# TODO Troppo regolare, dovrebbe essere più variabile
		if self.human.enabled:
			wtime = len(text) / float(self.writing_speed) * 60
			
			# Nascondere meglio il tempo preciso, può essere un problema di sicurezza
			# nel caso per esempio il testo fosse una password
			logger.info("L'uomo sta scrivendo, tempo necessario: %ss", int(wtime))
			time.sleep(wtime)
		
	writing_speed = property(get_writing_speed, set_writing_speed)
