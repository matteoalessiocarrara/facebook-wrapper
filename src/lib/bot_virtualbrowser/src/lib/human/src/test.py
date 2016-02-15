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
import version


logging.basicConfig(level=logging.WARNING)

# Apriamo il browser
browser = virtualbrowser.Browser()

# Aprendo il browser, si apre anche una finestra
window = browser.windows_manager.windows.values()[0]

# Ogni finestra contiene almeno una scheda
tab = window.tabs_manager.tabs.values()[0]

# Scriviamo l'url nella barra degli indirizzi
tab.url = "https://www.python.org/"

# Premiamo invio, e carichiamo la pagina
tab.download_content()

print "Il titolo della pagina nella scheda 1 è", tab.bs_content.title.text

# Ora vogliamo aprire una nuova scheda
tab2 = window.tabs_manager.add_tab("https://google.com")

# Ccarichiamo la pagina
tab2.download_content()

print "Il titolo della pagina nella scheda 2 è", tab2.bs_content.title.text

# Torniamo sulla scheda 1, è sempre aperta
print "Il titolo della pagina nella scheda 1 è", tab.bs_content.title.text

# Ora apriamo una nuova finestra
window2 = browser.windows_manager.add_window()

# Anche in questa, c'è già una scheda aperta
tab3 =  window2.tabs_manager.tabs.values()[0]

tab3.url = "https://m.facebook.com"
tab3.download_content()

# Dimostriamo che ci sono sempre tre schede aperte
print "Il titolo della pagina nella scheda 3 è", tab3.bs_content.title.text
print "Il titolo della pagina nella scheda 2 è", tab2.bs_content.title.text
print "Il titolo della pagina nella scheda 1 è", tab.bs_content.title.text

# Ora usciamo
window2.close()
window.close()



















