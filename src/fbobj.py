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

"""Oggetti di Facebook"""

import multiprocessing
import logging
import Queue
import time
import sys


from cachetools import LRUCache, TTLCache, cached
from lxml import etree
from bs4 import BeautifulSoup



from myexceptions import *
from shared import caching_levels

import version


# Configurazione del sistema di logging
logger = logging.getLogger(version.lib_name)
logger.addHandler(logging.NullHandler())


class GenericFbObj(object):
	"""
	Un oggetto che è su facebook: ha un url, e un oggetto Facebook per visualizzare
	l'url
	"""
	
	def __init__(self, facebook_obj, url):
		"""
		Imposta self.fb e self.url
		
		
		Parametri:
			
			facebook_obj: fbwrapper.Facebook
				L'oggetto Facebook utilizzato per visualizzare l'url
			
			url: str
				Url dell'oggetto
				
		"""
		
		self.__set_url(url)
		self.fb = facebook_obj

	def __str__(self):
		"""Restituisce l'url dell'oggetto"""
		return self.url
		
	def __set_url(self, url):
		self.__url = url

	def get_url(self):
		return self.__url
		
	def get_browser(self):
		"""
		Il browser utilizzato per visualizzare questo oggetto
		Scorciatoia per self.fb.browser
		"""
		return self.fb.browser
		
	def get_bw(self):
		"""
		La finestra del browser nella quale siamo loggati su fb, utilizzata per
		visualizzare questo oggetto
		
		Scorciatoia per self.fb.bw
		"""
		return self.fb.bw

	url = property(get_url)

	browser = property(get_browser)
	bw = property(get_bw)
	


class Profile(GenericFbObj):

	def __init__(self, facebook_obj, url):
		"""
		Parametri:
		
			facebook_obj: fbwrapper.Facebook
				Oggetto Facebook utilizzato per visualizzare questo profilo
				
			url: str
				Url completo del profilo, es: https://m.facebook.com/profilo
		"""
		super(Profile, self).__init__(facebook_obj, url)

	def get_nickname(self):
		"""
		Estrae il nickname dall'url
		Non tutti i profili hanno un nickname, a volte potrebbe restituire roba
		tipo profile.php?id=1234567890
		"""
		ret = self.url.split("/")[-1]
		logger.debug("Url del profilo: %s, nickname: %s", self.url, ret)
		
		return ret

	def get_gender(self):
		# AL ROKO AL ROKO!!1
		"""
		Restituisce "bho" nel caso non lo trovi
		
		Eccezioni:
		
			KeyError
				Manca una costante per la lingua del profilo
		"""
		
		logger.info("Cercando il genere di %s", self.nickname)
		
		# Stringa da cercare nel codice HTML, cambia con la lingua
		div_title = {'Italiano': "Genere", 'English (US)': "Gender"}

		# La pagina con le informazioni sul profilo
		info_url = "https://m.facebook.com/" + self.nickname + "?v=info"

		pag = self.bw.bs_get(info_url)
		
		self.fb.human.brain.process(2, 7, "Cercando il genere")

		try:
			# Cerca nella pagina
			div_attrs = {'title': div_title[self.fb.my_profile.lang]}
			
			gender = pag.find("div", attrs=div_attrs).findAll("div")[1].text
			logger.info("Genere di %s: %s", self.nickname, gender)
			
			return gender
			
		except AttributeError:
			# Non trovato
			logger.info("Genere di %s non trovato", self.nickname)
			logger.debug(pag)
			
			return "bho"
			
		except KeyError:
			e = "Questo metodo attualmente non funziona con la lingua del profilo"
			i = "Il dizionario \"div_title\" non ha una stringa per la lingua del profilo"

			logger.error(e)
			logger.info(i)
			logger.debug("Lingua: %s", self.fb.my_profile.lang)

			raise KeyError(i)

	# XXX Troppo incasinato qui, usare un oggetto separato
	
	# Titolo dell'album con le immagini del profilo
	__profile_pictures_text = {
								'English (US)': "Profile Pictures",
								'Italiano': "Immagini del profilo"
								}
							
	def get_profile_picture_small(self):
		raise NotImplementedError

	def get_profile_picture_medium(self, album_list_url_suffix="/photos"):
		"""
		Restituisce il link all'immagine del profilo, o una stringa vuota
		in caso di errore
		Questo metodo non sempre funziona, perché non sempre è disponible un'immagine
		
		
		Parametri:
		
			album_list_url_suffix: str
				La stringa da aggiungere dopo a "https://m.facebook.com/" + self.nickname
				per andare alla pagina con la lista degli album. 
			
		
		Eccezioni:
		
			KeyError
				Questo metodo attualmente non funziona con la lingua del profilo
		"""
		
		logger.info("Cercando la foto del profilo di %s, dimensione media", self.nickname)
		
		tab = self.bw.tabs_manager.add_tab()
		
		
		# In questa pagina ci sono alcuni album. Ce ne sono anche altri ma a noi 
		# bastano questi, l'album con le immagini del profilo dovrebbe essere all'inizio
		album_list_url = "https://m.facebook.com/" + self.nickname + album_list_url_suffix

		logger.debug("Scaricando la lista degli album")
		pag = tab.bs_load(album_list_url)


		# Profile Pictures, link all'album con le immagini del profilo
		pp_url = None

		self.fb.human.brain.process(2, 5, "Cercando l'album con le foto del profilo")
		
		for link in pag.findAll("a"):
			
			try:
				if self.__profile_pictures_text[self.fb.my_profile.lang] in link.text:
					
					pp_url = "https://m.facebook.com" + link.get("href")
					logger.debug("Album con le immagini del profilo: %s" % pp_url)
					
					break
					
			except KeyError:
				e = "Questo metodo attualmente non funziona con la lingua del profilo"
				i = "Costante mancante in \"self.__profile_pictures_text\" per la lingua del profilo"

				logger.error(e)
				logger.info(i)
				logger.debug("Lingua del profilo: %s", self.fb.my_profile.lang)

				raise KeyError(i)

		if pp_url is None:
			# A volte l'album non esiste, perché non sono proprio visibili le
			# foto
			logger.info("L'album con le foto del profilo non esiste")
			return ""


		# Se ha trovato l'album
		logger.debug("Scaricando l'album")
		pag = tab.bs_load(pp_url)


		self.fb.human.brain.process(0, 2, "Cercando l'immagine del profilo più recente")
		
		try:
			latest_url = pag.find("div", attrs={'id': "thumbnail_area"}).find("a").get("href")
			latest_url = "https://m.facebook.com" + latest_url
			logger.debug("Immagine più recente = %s", latest_url)
			
		except AttributeError:
			# 'NoneType' object has no attribute 'get'
			# A volte l'album è vuoto
			logger.info("L'album è vuoto")
			return ""


		# Va alla pagina dell'anteprima della foto
		logger.debug("Scaricando l'anteprima della foto")
		pag = tab.bs_load(latest_url)

		# Estrae il link dell'anteprima visualizzata in questa pagina
		ret = pag.find("div", attrs={'id': "root"}).find("img").get("src")

		# Finito :)
		tab.close()
		
		logger.info("Immagine trovata")
		return ret

	def get_profile_picture_large(self):
		raise NotImplementedError
	
	# TODO Spostare in un oggetto questi metodi
	# Profile.profile_picture.size
	profile_picture_small = property(get_profile_picture_small)
	profile_picture_medium = property(get_profile_picture_medium)
	profile_picture_large = property(get_profile_picture_large)
	
	nickname = property(get_nickname)
	gender = property(get_gender)


def MyProfile(profile_class, facebook_obj, email, password):
	"""
	La classe MyProfile_NoBase dovrebbe derivare da fbobj.Profile.
	Ma in pratica deve derivare da una classe variabile, perché fbobj.Profile 
	può essere esteso da librerie esterne e in quel caso anche MyProfile_NoBase
	dovrebbe derivare dalla versione estesa
	
	
	Parametri:
	
		profile_class: fbobj.Profile
			La classe dalla quale deve derivare MyProfile_NoBase
		
		facebook_obj: fbwrapper.Facebook
			L'oggetto Facebook nel quale dobbiamo loggarci con questo profilo
		
		email: str
		
		password: str
	
	"""
	
	logger.debug("MyProfile_NoBase profile_class %s", profile_class)
	
	
	class MyProfile_NoBase(profile_class):
	
		def __init__(self, facebook_obj, email, password):
			# Questo url dovrebbe rimandare al proprio profilo
			url = "https://m.facebook.com/profile.php"
			
			super(MyProfile_NoBase, self).__init__(facebook_obj, url)
	
			self.__set_email(email)
			self.__set_password(password)
			
			self.__login()
	
		def __set_email(self, email):
			self.__email = email
	
		def get_email(self):
			return self.__email
	
		def __set_password(self, password):
			self.__password = password
	
		def get_password(self):
			return self.__password
	
		def __login(self):
			"""
			Prova ad accede a Facebook, usa la finestra del browser self.fb.bw
	
			Eccezioni:
			
				myexceptions.LoginError
					Login rifiutato da Facebook
			"""
	
			# TODO usare la versione m.facebook.com, è più leggera e veloce
	
			login_url = "https://www.facebook.com/login.php"
			login_ok_title = "Facebook"
	
			tab = self.bw.tabs_manager.add_tab()
			
	
			logger.info("Login in corso")
			logger.debug("Finestra del browser %s", self.bw.win_id)
	
			logger.debug("Get login form datas")
			res = tab.load(login_url)
	
			# Get login form and add email and password fields
			datas = self.__get_login_form(res.text)
	
			# Facciamo finta di scrivere l'email e la password :)
			self.fb.human.hand.write(self.email)
			self.fb.human.hand.write(self.password)
			
			datas['email'] = self.email
			datas['pass'] = self.password
	
			cookies2 = {
						'_js_datr': self.__get_reg_instance(),
						'_js_reg_fb_ref': "https%3A%2F%2Fwww.facebook.com%2F",
						'_js_reg_fb_gate': "https%3A%2F%2Fwww.facebook.com%2F"
					}
	
			logger.debug("Call login API with login form")
			login_res = tab.post(login_url, data=datas, cookies=cookies2)
			res_title = BeautifulSoup(login_res.text, "lxml").title.text
	
			# XXX Questo controllo a volte non funziona, da login ok anche quando
			# in realtà non è proprio così
			if res_title != login_ok_title:
				logger.error("Login fallito")
	
				logger.debug("title: ok = %s ricevuto = %s", login_ok_title, res_title)
				logger.debug("<!-- login_res.text --> %s", login_res.text)
	
				e = "Testo non atteso nel tag title: %s" % res_title
				raise LoginError(e, res_title, login_res.text, email, password)
				
			else:
				logger.info("Login OK")
	
			tab.close()
	
		def __get_reg_instance(self):
			"""Fetch "javascript-generated" cookie"""
	
			home_url = "https://www.facebook.com/"

			content = self.bw.get(home_url).text
			root = etree.HTML(content)
			instance = root.xpath('//input[@id="reg_instance"]/@value')
			return instance[0]
	
		def __get_login_form(self, content):
			"""Scrap post datas from login page"""
	
			# Get login form
			root = etree.HTML(content)
			form = root.xpath('//form[@id="login_form"][1]')
	
			# Can't find form tag
			if not form:
				raise ConstError("No form datas (can't find form tag)")
	
			fields = {}
			# Get all input tags in this form
			for input in form[0].xpath('.//input'):
				name = input.xpath('@name[1]')
				value = input.xpath('@value[1]')
	
				# Check name and value are both not empty
				if all([name, value]):
					fields[name[0]] = value[0]
	
			return fields

		def get_profile_picture_medium(self):
			return super(MyProfile_NoBase, self).get_profile_picture_medium(album_list_url_suffix="?v=photos")
		
		def get_server_lang(self):
			"""
			Eccezioni:
			
				ConstError
					Non funziona più il metodo, va aggiornato l'algoritmo
			"""

			logger.info("Scaricando la lingua del proprio profilo")
			
			# graph.facebook.com non funziona più :(
			pag = self.bw.bs_get("https://m.facebook.com/settings/language/")
	
			self.fb.human.brain.process(0, 2, "Cercando la lingua del mio profilo")
			
			try:
				return pag.find("a", attrs={'href': "/language.php"}).find("span").text
				
			except AttributeError:
				e = "Impossibile ottenere la lingua del profilo! Metodo da aggiornare"
	
				# Senza lingua del profilo, tanti metodi che dipendono dalle stringhe
				# traducibili non funzionano
				raise ConstError(e)
		
		# Cambiare la lingua del profilo non è una cosa che si fa molto spesso
		# E soprattutto non è una cosa che si dovrebbe fare mentre un bot sta 
		# lavorando con il profilo
		# Quindi se la lib non funziona più arrangiati
		__safe_lang_cache = TTLCache(maxsize=1, ttl=10 * 60)
		__unsafe_lang_cache = TTLCache(maxsize=1, ttl=30 * 60)
		__offline_lang_cache = LRUCache(maxsize=1)
		
		get_cached_lang_safe = cached(__safe_lang_cache)(get_server_lang)
		get_cached_lang_unsafe = cached(__unsafe_lang_cache)(get_server_lang)
		get_cached_lang_offline = cached(__offline_lang_cache)(get_server_lang)
		
		def get_lang(self, caching_level=None):
			"""
			Restituisce la lingua del profilo, usa automaticamente la cache se
			attiva
			
			
			Parametri:
			
				caching_level: int
					Specifica il livello di caching, e quindi il metodo da usare
					per restituire la lingua. Il valore di caching_level deve 
					essere preso da shared.caching_levels.
					Se non è specificato, usa quello predefinito per il profilo.
				
				
			Eccezioni:
			
				ValueError
					caching_level non è valido
			"""
			
			if caching_level == None:
				caching_level = self.fb.caching_level
	
			logger.debug("caching_level: %s", caching_level)
			
			if caching_level == caching_levels['disabled']:
				return self.get_server_lang()
				
			elif caching_level == caching_levels['safe']:
				return self.get_cached_lang_safe()
				
			elif caching_level == caching_levels['unsafe']:
				return self.get_cached_lang_unsafe()
				
			elif caching_level == caching_levels['offline']:
				return self.get_cached_lang_offline()
				
			else:
				# XXX Questo controllo deve essere generalizzato, perché serve spesso
				raise ValueError("caching_level non valido, non è in caching_levels")
				

		email = property(get_email)
		password = property(get_password)
		
		profile_picture_medium = property(get_profile_picture_medium)
		lang = property(get_lang)

	return MyProfile_NoBase(facebook_obj, email, password)


class Group(GenericFbObj):

	def __init__(self, facebook_obj, url):
		"""
		Parametri:
		
			facebook_obj: fbwrapper.Facebook
				L'oggetto Facebook con il quale visualizzare questo gruppo
				
			url: str
				Url completo del gruppo, es: https://m.facebook.com/groups/1234
		"""
		super(Group, self).__init__(facebook_obj, url)

	def get_id(self):
		"""
		Restituisce l'id del gruppo, un numero usato come identificatore su Facebook
		Attenzione: l'id è un numero, ma viene restituita una stringa
		"""
		ret = self.url.split("/")[-1]
		logger.debug("Url del gruppo: %s id: %s", self.url, ret)
		
		return ret

	def get_name(self):
		# Attualmente il nome è nel tag <title> di questa pagina
		url = "https://m.facebook.com/groups/" + self.gid + "?view=info"
		
		pag = self.bw.bs_get(url)
		self.fb.human.brain.process(0, 2, "Cercando il nome del gruppo")
		
		return pag.title.text

	# TODO Eliminare il contatore dei profili, è brutto... sostituirlo con logging.info
	# TODO Gestire meglio l'emulazione umana in questo metodo
	def get_members(self, out=sys.stderr, verbose=False, processes=1, queue_get_timeout=5,
					sleep_before_login=5):

		# Tenere sincronizzata la descrizione di sleep_before_login con quella in
		# self.__members_download_process()
		"""
		Parametri:
		
			out: file
				Dove verrà scritto il contatore dei download (sys.stdout/sys.stderr/...),
				attivabile con verbose
				
			verbose: bool
				Se true, scrive su out il numero di profili attualmente scaricati
				
			processes: int
				Il numero di processi da utilizzare per il download
				ATTENZIONE: usando troppi processi Facebook potrebbe dare un errore
				di login per i troppi tentativi; inoltre questo potrebbe rallentare
				invece che velocizzare se il gruppo è piccolo, visto che ogni processo
				deve rifare il login. Potrebbe metterci di più a fare il login 
				in ogni processo, che a scaricare i profili con un processo solo
				
			queue_get_timeout: int
				Quanti secondi aspettare che arrivi un profilo dai processi, prima
				di considerare i profili finiti
				
			sleep_before_login: int
				Tempo di attesa fra il login di ogni processo. Può essere anche 0,
				ma molto probabilmente Facebook vi prenderà a calci in culo e si 
				bloccherà il programma con un errore di login


		Restituisce una lista di dizionari. Ogni dizionario rappresenta un profilo
		con alcune informazioni.
		
		Descrizione delle chiavi:
		
			image: str
				Link alla (piccola) immagine del profilo visualizzata nella lista
			
			name: str
			
			info: str
				Alcune informazioni sul profilo, per es: "Admin · Joined over a
		        year ago"
			
			url:  str
				Link al profilo	
			
			add_friend: str
				Link per aggiungere il profilo agli amici. ATTENZIONE: il link 
				non funziona se siamo loggati con un profilo diverso da quello usato
				per ottenere questo link
			
			table_id: str
				 Un'informazione che si trova nel codice HTML
		"""
		
		logger.info("Scaricando i membri del gruppo %s", self.url)
		
		# Verranno scaricate delle pagine con una lista di profili in ogni pagina

		# Una coda con i profili, utilizzabile da più processi contemporaneamente
		members_q = multiprocessing.Queue()


		# Costante da aggiungere al parametro "start" nell'url per andare
		# alla pagina successiva
		# Si potrebbe anche cercare il link, ma è più comodo così per dividere
		# il lavoro fra più processi
		start_offset = None

		# Cerca il valore di start_offset
		
		# XXX Usare args in session.get2
		pag1 = "https://m.facebook.com/browse/group/members/?id=%s&start=0" % self.gid
		
		logger.debug("Cercando il valore di start_offset, scaricando la prima pagina")

		pag = self.bw.bs_get(pag1)

		try:
			# Cerca il link alla pagina successiva
			pag2 = pag.find("div", attrs={'id': "m_more_item"}).a.get("href")
			
			# Se non c'è stata un eccezione, ha trovato il link ed estrae il numero
			start_offset = int(pag2[pag2.find("start="):].split("=")[1].split("&")[0])
			logger.debug("start_offset = %d", start_offset)
			
		except AttributeError:
			# AttributeError: 'NoneType' object has no attribute 'a'
			# Il link non è stato trovato, è una sola pagina
			logger.debug("Il link alla pagina successiva non è stato trovato")


		# Se c'è una sola pagina non ha senso usare più processi
		if start_offset is None:
			logger.info("Scaricamento di una pagina")
			self.__members_download_process(members_q, start_offset=0, start=0, 
											sleep_before_login=0, open_new_window=False)

		else:
			if processes == 1:
				logger.info("Download con un solo processo")
				
				# Un solo processo equivale a chiamare normalmente il metodo
				self.__members_download_process(members_q, start_offset, start=0,
												sleep_before_login=0, open_new_window=False)
												
			else:
				logger.info("Download con più processi")

				if self.fb.human.enabled:
					logger.warning("Emulazione umana attiva, ma questo non è un comportamento umano!")

					
				# Lista dei processi
				proc_l = []

				# Valore di start per il processo
				proc_start = 0

				# start_offset per i processi
				p_start_offset = int(start_offset) * int(processes)


				# Creazione dei processi
				for i in range(0, processes):
					logger.debug("Creando il processo %d", i + 1)

					proc_args = (members_q, p_start_offset, proc_start, 
								sleep_before_login * i)
					tmp_proc = multiprocessing.Process(target=self.__members_download_process,
														args=proc_args)
					
					# Per ora mettiamo il processo nella lista, si avvia dopo
					proc_l.append(tmp_proc)
					
					# Il prossimo processo deve partire dalla pagina successiva
					proc_start += start_offset


				# Avvio dei processi
				for process in proc_l:
					logger.debug("Avviando il processo %d", proc_l.index(process) + 1)
					process.start()


		# Ora riceviamo i profili dai processi
		try:
			members_l = []
			profiles = 0

			logger.debug("Aspettando i profili, timeout %d", queue_get_timeout)
			
			while(True):
				try:
					# XXX Inviare un qualcosa di particolare per dire che
					# i profili sono finiti, eliminare il timeout
					tmp_prof = members_q.get(timeout=queue_get_timeout)
					
				except Queue.Empty:
					logger.debug("Tutti i profili ricevuti")
					break

				members_l.append(tmp_prof)
				profiles += 1

				if verbose:
					# XXX Come unire questo output e quello di logging?
					# È brutto così :(
					out.write("Profili scaricati: %d\r"  % profiles)
					out.flush()

		except KeyboardInterrupt:
			logger.warning("Parent received ctrl-c")

			# Terminiamo i processi
			for process in proc_l:
				process.terminate()
				process.join()

			# ed usciamo
			return


		if verbose:
			# Per il contatore dei profili
			# Perché fino ad ora ho riscritto la stessa riga con \r
			out.write("\n")
		
		return members_l

	def __members_download_process(self, queue, start_offset, start, sleep_before_login, open_new_window=True):
		"""
		Metodo usato da self.get_members() per il download e l'estrazione dei profili
		Questo è un metodo separato in modo da poter usare più processi

		
		Parametri:
		
			queue: multiprocessing.Queue()
				L'oggetto  dove inviare i profili trovati
			
			start_offset: int
				Il numero da aggiungere a start per andare alla prossima pagina 
				da scaricare
			
			start: int
				Il valore del parametro start nell'url, ovvero la prima pagina
				da scaricare
			
			sleep_before_login: int
				Tempo di attesa fra il login di ogni processo. Può essere anche 0,
				ma molto probabilmente Facebook vi prenderà a calci in culo e si
				bloccherà il programma con un errore di login
				
			open_new_window: bool
				Se si sta scaricando con un processo solo, allora si può evitare 
				di aprire una nuova finestra del browser		
		
		Eccezioni:
		
			AttributeError
				Non ha trovato un informazione per un profilo, ma ci si aspettava
				che la trovasse
			
			ConstError
				Come AttributeError
		"""

		# Questa verrà impostata sotto
		window = None
		
		if open_new_window:
			# HACK Le schede del browser usano lo stesso oggetto requests.Session,
			# ma non può essere utilizzato contemporanemanete da più processi
			# requests.exceptions.SSLError: [Errno 1] _ssl.c:1429: error:1408F119:SSL routines:SSL3_GET_RECORD:decryption failed or bad record mac
			
			# Quindi si crea una nuova finestra per ogni processo
			# E si lascia stare la prima finestra, che è quella usata normalmente dal
			# processo genitore
			
			# XXX Non aprire una nuova finestra, quando si scarica con un processo solo
			logger.debug("Creando una nuova finestra per il processo")
			window = self.browser.windows_manager.add_window()
	
			# Ora va impostata come finestra predefinita del browser, per
			# poter essere usata per il login
			self.fb.bw = window
	
			# Sembra che facebook non accetti più login troppo veloci
			logger.info("Aspettando %d s prima del login", sleep_before_login)
			time.sleep(sleep_before_login)
			
			# HACK
			# Forziamo il login in questa finestra
			# XXX Bruttina questa operazione, non è un metodo pubblico...
			self.fb.my_profile._MyProfile_NoBase__login()
		
		else:
			logger.debug("Utilizzando la finestra già esistente")
			window = self.bw
			
		tab = window.tabs_manager.add_tab()


		# Scarichiamo le pagine con i profili
		while(True):
			# XXX usare args={} in session.get2(), non questo schifo...
			# la pagina da scaricare con i profili
			pag_url = "https://m.facebook.com/browse/group/members/?id=%s&start=%s" % (self.gid, str(start))

			# Scarica la pagina
			logger.debug("start = %d", start)
			pag = tab.bs_load(pag_url)

			# Cerca i profili
			profiles = pag.body.find("div", attrs={'id': "root", 'role': "main"}).findAll("table")

			# Nessun profilo nella pagina, pagine finite
			if len(profiles) == 0:
				logger.debug("Non ci sono profili in questa pagina")
				break

			# Altrimenti
			self.fb.human.do(5, 15, "Copiando i profili che sono in questa pagina")
			
			# Estrae le informazioni da ogni profilo
			for profile in profiles:
				try:
					info = profile.findAll("h3")[1].text
					name = profile.find("h3").find("a").text
					img = profile.find("img").get("src")
					table_id = profile.get("id")

					# [:-8] perché gli indirizzi finiscono con "?fref=pb"
					url = profile.find("h3").find("a").get("href")[:-8]
					url = "https://m.facebook.com" + url

					try:
						# ATTENZIONE!!! Questo link funziona solo se siamo loggati
						# con lo stesso profilo che si sta usando adesso
						add_friend = profile.findAll("a")[1].get("href")
						add_friend = "https://m.facebook.com" + add_friend
						
					except IndexError:
						# Non sempre c'è il link per aggiungere agli amici
						add_friend = ""

				except AttributeError:
					# 'NoneType' object has no attribute ...
					logger.error("Informazione non trovata")
					logger.debug(str(profilo))
					raise

				# In caso di modifiche a questo dizionario, aggiornare la docstring
				# di self.get_members()
				profile_info = {
								'image': img,
								'name': name,
								'info': info,
								'url':  url,
								'add_friend': add_friend,
								'table_id': table_id
								}

				if None in profile_info.values():
					const_name = profile_info.keys(profile_info.values().index(None))
					err = "Informazione sul profilo non trovata: %s" % const_name
					
					logger.error(err)
					logger.debug(str(profile))
					
					raise ConstError(err)

				# Invia il profilo al processo principale
				queue.put(profile_info)


			try:
				# Cerca il link alla prossima pagina
				# TODO Generalizzare, questo viene usato anche in self.get_members()
				# per trovare il valore di start_offset
				pag.find("div", attrs={'id': "m_more_item"}).a.get("href")
				
			except AttributeError:
				# AttributeError: 'NoneType' object has no attribute 'a'
				# il link non è stato trovato
				logger.debug("Il link alla pagina successiva non è stato trovato")
				break

			# Passiamo alla pagina successiva
			start += start_offset

		# Se non hai aperto una nuova finestra, allora l'hai a lasciar stare quella
		# che c'è, perché è usata di default da tutti i metodi e deve rimanere aperta
		if open_new_window:
			window.close()

	gid = property(get_id)
	name = property(get_name)
	members = property(get_members)


class Friends(GenericFbObj):
	"""Dovrebbe rappresentare la lista degli amici"""
	
	# TODO Finire di implementare
	
	def __init__(self, facebook_obj):
		"""
		Parametri:
		
			facebook_obj: fbwrapper.Facebook
				Oggetto Facebook utilizzato per recuperare i dati
		"""
		super(Friends, self).__init__(facebook_obj, url=None)
		

	def get_online(self):
		"""Restituisce una lista con il nome degli amici online"""
		# TODO Migliorare output, aggiungere più informazioni per ogni profilo
		
		pag = self.bw.bs_get("https://m.facebook.com/buddylist.php")
		
		table_div = pag.find("div", attrs={'id': "root"}).div.div
		profiles = table_div.findAll("table")
		ret = []
		
		for profile in profiles:
			ret.append(profile.a.text)
			
		return ret
			
	online = property(get_online)
		

