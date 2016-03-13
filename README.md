# Facebook wrapper #

Libreria per usare facebook in python

> Se lo puoi fare su facebook, lo puoi fare con questa libreria


## Caratteristiche ##
 
 * Nessun limite a ciò che si può fare: si basa sul normale sito html, non sulle
   api di facebook
 * Modalità di emulazione umana: lavora sul sito imitando il comportamento di un
   umano, per evitare che facebook ci riconosca come bot
 * Sistema di caching integrato, per migliorare le prestazioni ed evitare di 
   insospettire facebook recuperando dati troppo spesso
 * Modalità con più processi, per recuperare alcuni dati più velocemente


## Esempio ##

```python
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
```

## Requisiti ##

 * [Cachetools](https://pypi.python.org/pypi/cachetools/1.0.0)
 * [BeautifulSoup 4](http://www.crummy.com/software/BeautifulSoup/#Download)
 * [Lxml](http://lxml.de/installation.html)
 * Quelli della libreria [bot-virtualbrowser](https://github.com/matteoalessiocarrara/bot-virtualbrowser)


## Estendere la libreria ##

Ho scritto questa libreria non come progetto a se, ma come componente di alcuni
progetti più grandi. Quindi, contiene solo ciò che è necessario per far funzionare
questi progetti.  
Comunque la "base" è completa, e se fossero necessari altri oggetti/metodi possono
essere aggiunti facilmente.


## Altre informazioni ##

> This is the Unix philosophy: Write programs that do one thing and do it well.
Write programs to work together. Write programs to handle text streams, because
that is a universal interface.

Aggiornamenti: [GitHub](https://github.com/matteoalessiocarrara)  
Email: sw.matteoac@gmail.com
