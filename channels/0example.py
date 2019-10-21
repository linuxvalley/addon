# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Canale per 'idcanale nel json'
# By: pincopallo!
# Eventuali crediti se vuoi aggiungerli
# ------------------------------------------------------------
# Rev: 0.2
# Update 12-10-2019
# fix:
# 1. aggiunto pagination e sistemate alcune voci
# 2. modificato problemi in eccezioni
# 3. aggiunta la def select
# 4. modifica alla legenda e altre aggiunte

# Questo vuole solo essere uno scheletro per velocizzare la scrittura di un canale.
# La maggior parte dei canali può essere scritta con il decoratore.
# I commenti sono più un promemoria... che una vera e propria spiegazione!
# Niente di più.
# Ulteriori informazioni sono reperibili nel wiki:
# https://github.com/kodiondemand/addon/wiki/decoratori
 
"""
    Questi sono commenti per i beta-tester.

    Su questo canale, nella categoria 'Ricerca Globale'
    non saranno presenti le voci 'Aggiungi alla Videoteca'
    e 'Scarica Film'/'Scarica Serie', dunque,
    la loro assenza, nel Test, NON dovrà essere segnalata come ERRORE.

    Novità. Indicare in quale/i sezione/i è presente il canale:
       - Nessuna, film, serie, anime...

    Avvisi:
        - Eventuali avvisi per i tester

    Ulteriori info:

"""
# CANCELLARE Ciò CHE NON SERVE per il canale, lascia il codice commentato ove occorre,
# ma fare PULIZIA quando si è finito di testarlo

# Qui gli import
#import re

# per l'uso dei decoratori, per i log, e funzioni per siti particolari
from core import support
# se non si fa uso di findhost()
from platformcode import config

# in caso di necessità
#from core import scrapertoolsV2, httptools, servertools, tmdb
from core.item import Item # per newest
#from lib import unshortenit

##### fine import

# impostazioni variabili o def findhost()

# se necessaria la variabile __channel__
# da cancellare se non utilizzata
__channel__ = "id nel json"
# da cancellare se si utilizza findhost()
host = config.get_channel_url('id nel json' OR __channel__) # <-- ATTENZIONE
headers = [['Referer', host]]

# Inizio findhost() - da cancellare se usato l'altro metodo
#impostati dinamicamente da findhost()
host = ""
headers = ""

def findhost():
    global host, headers
    # da adattare alla bisogna...
    permUrl = httptools.downloadpage('INSERIRE-URL-QUI', follow_redirects=False).headers
    host = 'https://www.'+permUrl['location'].replace('https://www.google.it/search?q=site:', '')
    # cancellare host non utilizzato
    host = scrapertoolsV2.find_single_match(permUrl, r'<div class="elementor-button-wrapper"> <a href="([^"]+)"')
    headers = [['Referer', host]]

findhost() # così le imposta una volta per tutte
### fine findhost

# server di esempio...
list_servers = ['supervideo', 'streamcherry','rapidvideo', 'streamango', 'openload']
# quality di esempio
list_quality = ['default', 'HD', '3D', '4K', 'DVD', 'SD']

### fine variabili

#### Inizio delle def principali ###

@support.menu
def mainlist(item):
    support.log(item)

    # Ordine delle voci
    # Voce FILM, puoi solo impostare l'url
    film = ['', # url per la voce FILM, se possibile la pagina principale con le ultime novità
        #Voce Menu,['url','action','args',contentType]
        ('Al Cinema', ['', 'peliculas', '']),
        ('Generi', ['', 'genres', 'genres']),
        ('Per Lettera', ['', 'genres', 'letters']),
        ('Anni', ['', 'genres', 'years']),
        ('Qualità', ['', 'genres', 'quality']),
        ('Mi sento fortunato', ['', 'genres', 'lucky']),
        ('Popolari', ['', 'peliculas', '']),
        ('Sub-ITA', ['', 'peliculas', ''])
        ]

    # Voce SERIE, puoi solo impostare l'url
    tvshow = ['', # url per la voce Serie, se possibile la pagina con titoli di serie
        #Voce Menu,['url','action','args',contentType]
        ('Novità', ['', '', '']),
        ('Per Lettera', ['', 'genres', 'letters']),
        ('Per Genere', ['', 'genres', 'genres']),
        ('Per anno', ['', 'genres', 'years'])
        ]
    # Voce ANIME, puoi solo impostare l'url
    anime = ['', # url per la voce Anime, se possibile la pagina con titoli di anime
        #Voce Menu,['url','action','args',contentType]
        ('Novità', ['', '', '']),
        ('In Corso',['', '', '', '']),
        ('Ultimi Episodi',['', '', '', '']),
        ('Ultime Serie',['', '', '', ''])
        ]

    """
        Eventuali Menu per voci non contemplate!
    """

    # se questa voce non è presente il menu genera una voce
    # search per ogni voce del menu. Es. Cerca Film...
    search = '' # se alla funzione search non serve altro

    # VOCE CHE APPARIRA' come prima voce nel menu di KOD!
    # [Voce Menu,['url','action','args',contentType]
    top = [ '' ['', '', '', ''])

    # Se vuoi creare un menu personalizzato o perchè gli altri non
    # ti soddisfano
    # [Voce Menu,['url','action','args',contentType]
    nome = [( '' ['', '', '', ''])
    return locals()

    # Legenda known_keys per i groups nei patron
    # known_keys = ['url', 'title', 'title2', 'season', 'episode', 'thumb', 'quality',
    #                'year', 'plot', 'duration', 'genere', 'rating', 'type', 'lang']
    # url = link relativo o assoluto alla pagina titolo film/serie
    # title = titolo Film/Serie/Anime/Altro
    # title2 = titolo dell'episodio Serie/Anime/Altro
    # season = stagione in formato numerico
    # episode = numero episodio, in formato numerico.
    # thumb = linkrealtivo o assoluto alla locandina Film/Serie/Anime/Altro
    # quality = qualità indicata del video
    # year = anno in formato numerico (4 cifre)
    # duration = durata del Film/Serie/Anime/Altro
    # genere = genere del Film/Serie/Anime/Altro. Es: avventura, commedia
    # rating = punteggio/voto in formato numerico
    # type = tipo del video. Es. movie per film o tvshow per le serie. Di solito sono discrimanti usati dal sito
    # lang = lingua del video. Es: ITA, Sub-ITA, Sub, SUB ITA.
    # AVVERTENZE: Se il titolo è trovato nella ricerca TMDB/TVDB/Altro allora le locandine e altre info non saranno quelle recuperate nel sito.!!!!


@support.scrape
def peliculas(item):
    support.log(item)
    #support.dbg() # decommentare per attivare web_pdb

    action = ''
    blacklist = ['']
    patron = r''
    patronBlock = r''
    patronNext = ''
    pagination = ''

    #debug = True  # True per testare le regex sul sito
    return locals()

@support.scrape
def episodios(item):
    support.log(item)
    #support.dbg()

    action = ''
    blacklist = ['']
    patron = r''
    patronBlock = r''
    patronNext = ''
    pagination = ''

    #debug = True
    return locals()

# Questa def è utilizzata per generare i menu del canale
# per genere, per anno, per lettera, per qualità ecc ecc
@support.scrape
def genres(item):
    support.log(item)
    #support.dbg()

    action = ''
    blacklist = ['']
    patron = r''
    patronBlock = r''
    patronNext = ''
    pagination = ''

    #debug = True
    return locals()

############## Fine ordine obbligato
## Def ulteriori

# per quei casi dove il sito non differenzia film e/o serie e/o anime
# e la ricerca porta i titoli mischiati senza poterli distinguere tra loro
# andranno modificate anche le def peliculas e episodios ove occorre
def select(item):
    support.log('select --->', item)
    #support.dbg()
    data = httptools.downloadpage(item.url, headers=headers).data
    # pulizia di data, in caso commentare le prossime 2 righe
    data = re.sub('\n|\t', ' ', data)
    data = re.sub(r'>\s+<', '> <', data)
    block = scrapertoolsV2.find_single_match(data, r'')
    if re.findall('', data, re.IGNORECASE):
        support.log('select = ### è una serie ###')
        return episodios(Item(channel=item.channel,
                              title=item.title,
                              fulltitle=item.fulltitle,
                              url=item.url,
                              args='serie',
                              contentType='tvshow',
                              #data1 = data decommentando portiamo data nella def senza doverla riscaricare
                            ))

############## Fondo Pagina
# da adattare al canale
def search(item, text):
    support.log('search', item)
    itemlist = []
    text = text.replace(' ', '+')
    item.url = host + '/index.php?do=search&story=%s&subaction=search' % (text)
    # bisogna inserire item.contentType per la ricerca globale
    # se il canale è solo film, si può omettere, altrimenti bisgona aggiungerlo e discriminare.
    item.contentType = item.contentType
    try:
        return peliculas(item)
    # Se captura la excepcion, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            log('search log:', line)
        return []


# da adattare al canale
# inserire newest solo se il sito ha la pagina con le ultime novità/aggiunte
# altrimenti NON inserirlo
def newest(categoria):
    support.log('newest ->', categoria)
    itemlist = []
    item = Item()
    try:
        if categoria == 'peliculas':
            item.url = host
            item.action = 'peliculas'
            itemlist = peliculas(item)

            if itemlist[-1].action == 'peliculas':
                itemlist.pop()
    # Continua la ricerca in caso di errore
    except:
        import sys
        for line in sys.exc_info():
            support.log('newest log: ', {0}.format(line))
        return []

    return itemlist

# da adattare...
# consultare il wiki sia per support.server che ha vari parametri,
# sia per i siti con hdpass
#support.server(item, data='', itemlist=[], headers='', AutoPlay=True, CheckLinks=True)
def findvideos(item):
    support.log('findvideos ->', item)
    return support.server(item, headers=headers)
