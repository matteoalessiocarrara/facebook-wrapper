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

import virtualbrowser
import logging


logging.basicConfig(level=logging.WARNING)


# Apriamo un browser
browser = virtualbrowser.BotBrowser()

# Aprendo il browser, si apre una finestra del browser
window = browser.windows_manager.windows.values()[0]

# E in ogni finestra c'è sempre almeno una scheda
tab = window.tabs_manager.tabs.values()[0]


# Il nostro bot deve scaricare una pagina, usando una nuova scheda
# Come farebbe senza questa libreria:

newtab = window.tabs_manager.add_tab("https://python.org")
newtab.download_content()
pag = newtab.get_content()
newtab.close()

# Come può fare con la libreria

pag = window.get("https://python.org")


# C'è già una scheda aperta, il nostro bot vuole usarla per scaricare una pagina
# Come farebbe senza questa libreria:

tab.set_url("https://python.org")
tab.download_content()
pag = tab.get_content()

# Come può fare con la libreria

pag = tab.load("https://python.org")


window.close()



















