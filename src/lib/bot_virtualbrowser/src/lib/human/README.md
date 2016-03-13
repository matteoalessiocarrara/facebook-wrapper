# Human Virtualbrowser #

Browser headless scritto in python, ispirato ai browser con gui - libreria


## Esempio ##

```python
import virtualbrowser
import logging

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
```


## Obbiettivo ##

L'obbiettivo è scrivere un "oggetto" browser che abbia le stesse azioni (metodi)
e caratteristiche (attributi) della gui di un normale browser, come firefox.  
Per esempio, un oggetto browser avrà un attributo "gestore delle schede", e questo
avrà a sua volta un attributo "schede aperte". Un oggetto "scheda", avrà un metodo
"chiudi", "ricarica" ecc.

Il browser gui preso come riferimento è firefox, ma si ispira al funzionamento dei
browser con gui in generale.

Essendo ispirato ai browser gui visti "dall'esterno", dovrebbe essere molto semplice
e intuitivo. Purtroppo però, il fatto di essere ispirato a browser con gui e non 
avere una gui lo rende scomodo per un utilizzo reale.
Quindi ho scritto un wrapper ottimizzato per l'utilizzo in script, lo trovate 
[qui](https://github.com/matteoalessiocarrara/bot-virtualbrowser).


## A cosa serve? ##

Da solo, a poco. Infatti è solo un componente di un [progetto più grande](https://github.com/matteoalessiocarrara/bot-virtualbrowser).  
L'idea iniziale era scrivere un browser headless con funzioni simili a quelle dei
browser gui. Io preferisco, quando possibile, scomporre i progetti in progetti più
piccoli, indipendenti e riutilizzabili.
Quindi questo è il browser-gui-senza-gui, nell'altro repo ci sono delle ottimizzazioni
per renderlo un browser headless comodo.


## Perché quel nome? ##

Il browser dovrebbe rendere disponibili azioni (metodi) per esseri umani, quindi
non semplificazioni per bot come apri-scheda/scarica-contenuto/chiudi-scheda.
Queste sono contenute [in un repo separato](https://github.com/matteoalessiocarrara/bot-virtualbrowser).


## Requisiti ##

 * Python 2
 * [BeautifulSoup 4](http://www.crummy.com/software/BeautifulSoup/#Download)
 * [Requests](http://docs.python-requests.org/en/master/user/install/#install)


## Codice ##

La sintassi delle docstring è ispirata a quella usata in [NumPy](https://github.com/numpy/numpy/)


## Branch ##

### master ###

Sul branch master c'è l'ultima versione stable, le mie librerie sono incluse
come semplici sorgenti

### beta-* ###

Questo branch non esiste sempre, viene creato solo quando si decide di creare
una nuova versione stable.  
Su questo branch si ripulisce e si documenta il codice, eventualmente si sitemano
i bug che ci sono.  
Le librerie sono incluse come submodule.

### dev ###

Versione alpha: tutte le nuove funzioni sono qui, ma potrebbero essere da ricontrollare
o scrivere meglio.  
Le librerie sono incluse come submodule.

### altri ###

Gli altri branch sono per nuove funzioni ancora non incluse in dev, probabilmente 
perché incomplete


## Altre informazioni ##

> This is the Unix philosophy: Write programs that do one thing and do it well.
  Write programs to work together. Write programs to handle text streams, because
  that is a universal interface.

Aggiornamenti: [GitHub](https://github.com/matteoalessiocarrara/human-virtualbrowser)  
Email: sw.matteoac@gmail.com
