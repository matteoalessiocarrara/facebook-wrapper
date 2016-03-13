# Bot virtualbrowser #

Browser headless veloce ed intuitivo, con interfaccia simile a quella dei browser gui - 
libreria in python


Questa è in realtà un estensione della libreria [human-virtualbrowser](https://github.com/matteoalessiocarrara/human-virtualbrowser), 
che contiene un "oggetto" browser senza interfaccia grafica ma strutturato in modo 
da averne le stesse caratteristiche.

Dal readme di human-virtualbrowser:

> L'obbiettivo è scrivere un "oggetto" browser che abbia le stesse azioni (metodi)
  e caratteristiche (attributi) della gui di un normale browser, come firefox.  
  Per esempio, un oggetto browser avrà un attributo "gestore delle schede", e questo
  avrà a sua volta un attributo "schede aperte". Un oggetto "scheda", avrà un metodo
  "chiudi", "ricarica" ecc.
  

## Esempio ##

```python
import virtualbrowser
import logging

logging.basicConfig(level=logging.DEBUG)

# Apriamo un browser
browser = virtualbrowser.BotBrowser()

# Aprendo il browser, si apre una finestra del browser
window = browser.windows_manager.windows.values()[0]

# E in ogni finestra c'è sempre almeno una scheda
tab = window.tabs_manager.tabs.values()[0]


# Il nostro bot deve scaricare una pagina, usando una nuova scheda.
# Come farebbe senza questa libreria:

newtab = window.tabs_manager.add_tab("https://www.python.org")
newtab.download_content()
pag = newtab.get_content()
newtab.close()

# Come può fare con la libreria

pag = window.get("https://www.python.org")


# C'è già una scheda aperta, il nostro bot la vuole usare per scaricare una pagina
# Come farebbe senza questa libreria:

tab.set_url("https://www.python.org")
tab.download_content()
pag = tab.get_content()

# Come può fare con la libreria

pag = tab.load("https://www.python.org")
```


## Perché dovrei usare questo browser headless? ##

È basato su un browser simile a quelli con gui, ma senza gui. Il risultato dovrebbe 
essere un browser headless veloce e intuitivo.


## Caratteristiche ##

 * Gestione interna di più finestre
 * Gestione di più schede per finestra
 * Basato sulla libreria requests per la parte della rete 
 * Parsing (opzionale) del contenuto delle schede con la libreria BeautifulSoup


## Requisiti ##

Vedere il readme di [human-virtualbrowser](https://github.com/matteoalessiocarrara/human-virtualbrowser)
, su cui si basa.  


## Documentazione ##

Questa libreria è solo un estensione di human-virtualbrowser, la documentazione
è quindi divisa fra i due repo.


## Altre informazioni ##

> This is the Unix philosophy: Write programs that do one thing and do it well.
  Write programs to work together. Write programs to handle text streams, because
  that is a universal interface.

Aggiornamenti: [GitHub](https://github.com/matteoalessiocarrara)  
Email: sw.matteoac@gmail.com
