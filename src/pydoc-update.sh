#!/bin/bash
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
#

# Aggiorna la documentazione autogenerata in ../doc

OUTFILE="../doc/pydoc.txt"

pydoc ./fbwrapper.py > $OUTFILE
pydoc ./fbobj.py >> $OUTFILE
pydoc ./human.py >> $OUTFILE
pydoc ./shared.py >> $OUTFILE
pydoc ./myexceptions.py >> $OUTFILE
pydoc ./version.py >> $OUTFILE

# Rimuove il percorso dei file dalla documentazione
# TODO È possibile lasciare solo il percorso relativo alla root del repo?

sed -i -e '/^FILE/,+2d' $OUTFILE

