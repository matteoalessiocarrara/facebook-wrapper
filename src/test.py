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

import logging

import fbwrapper
import shared

logging.basicConfig(level=logging.WARNING)

username = raw_input("Username: ")
password = raw_input("Password: ")

# Login
fb = fbwrapper.Facebook(username, password)

# Imposta la cache
fb.caching_level = shared.caching_levels['safe']

# Operazioni sui profili
print "Tu sei", fb.my_profile.gender
print "La lingua del tuo profilo è", fb.my_profile.lang
print "La tua immagine del profilo è", fb.my_profile.profile_picture_medium

# Operazioni sui gruppi
group_url = raw_input("Inserisci l'url di un gruppo: ")
group = fb.get_group(group_url)

print "Il nome del gruppo è", group.name

# Altro
print "Questi amici sono online:"

for friend in fb.friends.online:
	print friend



