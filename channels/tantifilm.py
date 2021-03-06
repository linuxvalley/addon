# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Canale per Tantifilm
# ------------------------------------------------------------

import re

from core import scrapertools, httptools, support
from core.item import Item
from core.support import info
from platformcode import logger
from platformcode import config, unify


def findhost(url):
    permUrl = httptools.downloadpage(url).data
    host = scrapertools.find_single_match(permUrl, r'Nuovo indirizzo: <a href="([^"]+)')
    return host

host = config.get_channel_url(findhost)
headers = [['Referer', host]]

player_iframe = r'<iframe src="([^"]+)"[^>]+></iframe>\s?<div class="player'

@support.menu
def mainlist(item):
    info()

    top = [('Generi', ['', 'category'])]
    film = ['/film',
        ('Al Cinema', ['/watch-genre/al-cinema/']),
        ('HD', ['/watch-genre/altadefinizione/']),
        ('Sub-ITA', ['/watch-genre/sub-ita/'])

        ]

    tvshow = ['/serie-tv/',
        ('HD', ['/watch-genre/serie-altadefinizione/']),
        ('Miniserie', ['/watch-genre/miniserie-1/']),
        ('Programmi TV', ['/watch-genre/programmi-tv/']),
        #('LIVE', ['/watch-genre/live/'])
        ]

    anime = ['/watch-genre/anime/'
        ]

    search = ''
    return locals()

@support.scrape
def peliculas(item):
    if item.args == 'search':
        patron = r'<a href="(?P<url>[^"]+)" title="Permalink to\s*(?P<title>[^"]+) \((?P<year>[0-9]+)[^<]*\)[^"]*"[^>]+>\s*<img[^s]+src="(?P<thumb>[^"]+)".*?<div class="calitate">\s*<p>(?P<quality>[^<]+)<\/p>'
    else:
        patronNext = r'<a class="nextpostslink" rel="next" href="([^"]+)">'
        patron = r'<div class="mediaWrap mediaWrapAlt">\s*<a href="(?P<url>[^"]+)"(?:[^>]+)?>?\s*<img[^s]+src="([^"]+)"[^>]+>\s*<\/a>[^>]+>[^>]+>[^>]+>(?P<title>.+?)(?P<lang>[sSuUbB\-iItTaA]+)?(?:[ ]?\((?P<year>\d{4})-?(?:\d{4})?)\).[^<]+[^>]+><\/a>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>\s*(?P<quality>[a-zA-Z-0-9\.]+)'
        patronBlock = r'<div id="main_col">(?P<block>.*?)<!\-\- main_col \-\->'

    # if item.args != 'all' and item.args != 'search':
    #     action = 'findvideos' if item.extra == 'movie' else 'episodios'
    #     item.contentType = 'movie' if item.extra == 'movie' else 'tvshow'
    # debug = True
    return locals()


@support.scrape
def episodios(item):
    info()
    if not item.data:
        data_check = httptools.downloadpage(item.url, headers=headers).data
        data_check = re.sub('\n|\t', ' ', data_check)
        data_check = re.sub(r'>\s+<', '> <', data_check)
    else:
        data_check = item.data
    data = httptools.downloadpage(scrapertools.find_single_match(data_check, player_iframe), headers=headers).data
    data = data.replace("'", '"')
    data = re.sub('\n|\t', ' ', data)
    data = re.sub(r'>\s+<', '> <', data)

    patronBlock = r'Stagioni<\/a>.*?<ul class="nav navbar-nav">(?P<block>.*?)<\/ul>'
    patron = r'<a href="(?P<url>[^"]+)"\s*>\s*<i[^>]+><\/i>\s*(?P<episode>\d+)<\/a>'
    # debugBlock = True

    otherLinks = support.match(data_check, patronBlock='<div class="content-left-film">.*?Keywords', patron='([0-9]+)(?:×|x)([0-9]+(?:-[0-9]+)?)(.*?)(?:<br|$)').matches

    def itemlistHook(itemlist):
        retItemlist = []

        for item in itemlist:
            item.contentType = 'episode'

            season = unify.remove_format(item.title)
            season_data = httptools.downloadpage(item.url).data
            season_data = re.sub('\n|\t', ' ', season_data)
            season_data = re.sub(r'>\s+<', '> <', season_data)
            # block = scrapertools.find_single_match(season_data, 'Episodi.*?<ul class="nav navbar-nav">(.*?)</ul>')
            episodes = scrapertools.find_multiple_matches(season_data, '<a.*?href="(?P<url>[^"]+)"[^>]+>Episodio (?P<episode>[0-9]+)(?::\s*(?P<title2>[^<]+))?')
            for url, episode in episodes:
                i = item.clone()
                i.action = 'findvideos'
                i.url = url
                i.contentSeason = str(season)
                i.contentEpisodeNumber = str(episode)
                i.title = str(season) + 'x' + str(episode)
                for ep in otherLinks:
                    if int(ep[0]) == int(season) and int(ep[1].split('-')[-1]) == int(episode):
                        i.otherLinks = ep[2]
                        break
                retItemlist.append(i)
        retItemlist.sort(key=lambda e: (int(e.contentSeason), int(e.contentEpisodeNumber)))
        return retItemlist

    # debugBlock = True
    return locals()


@support.scrape
def category(item):
    blacklist = ['Serie TV Altadefinizione', 'HD AltaDefinizione', 'Al Cinema', 'Serie TV', 'Miniserie', 'Programmi Tv', 'Live', 'Trailers', 'Serie TV Aggiornate', 'Aggiornamenti', 'Featured']
    patron = '<li><a href="(?P<url>[^"]+)"><span></span>(?P<title>[^<]+)</a></li>'
    patron_block = '<ul class="table-list">(.*?)</ul>'
    action = 'peliculas'

    return locals()


def search(item, texto):
    info(texto)


    item.url = host + "/?s=" + texto
    try:
        item.args = 'search'
        return peliculas(item)

    # Continua la ricerca in caso di errore
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


@support.scrape
def newest(categoria):
    if categoria == 'series':
        item = Item(url=host + '/aggiornamenti-giornalieri-serie-tv-2')
        data = support.match(item).data.replace('<u>','').replace('</u>','')
        item.contentType = 'episode'
        patronBlock = r'Aggiornamenti Giornalieri Serie TV.*?<div class="sp-body folded">(?P<block>.*?)</div>'
        patron = r'<p>(?P<title>.*?)\((?P<year>[0-9]{4})[^\)]*\)[^<]+<a href="(?P<url>[^"]+)">(?P<episode>[^ ]+) (?P<lang>[Ss][Uu][Bb].[Ii][Tt][Aa])?(?P<title2>[^<]+)?'

    return locals()


@support.scrape
def hdpass(item):
    patronBlock = r'<ul class="nav navbar-nav">(?P<block>.*?)</ul>'
    patron = r'<a.*?href="(?P<url>[^"]+)">'

    def itemHook(item):
        url = support.match(item.url, patron='<iframe.*?src="([^"]+)').match
        return Item(url=url)

    return locals()


def findvideos(item):
    info()
    support.info("ITEMLIST: ", item)
    data = support.match(item.url, headers=headers).data
    check = support.match(data, patron=r'<div class="category-film">(.*?)</div>').match
    if 'sub' in check.lower():
        item.contentLanguage = 'Sub-ITA'
    support.info("CHECK : ", check)
    if 'anime' in check.lower():
        item.contentType = 'tvshow'
        item.data = data
        support.info('select = ### è una anime ###')
        try:
            return episodios(item)
        except:
            pass
    elif 'serie' in check.lower():
        item.contentType = 'tvshow'
        item.data = data
        return episodios(item)

    # if 'protectlink' in data:
    #     urls = scrapertools.find_multiple_matches(data, r'<iframe src="[^=]+=(.*?)"')
    #     support.info("SONO QUI: ", urls)
    #     for url in urls:
    #         url = url.decode('base64')
    #         # tiro via l'ultimo carattere perchè non c'entra
    #         url, c = unshorten_only(url)
    #         if 'nodmca' in url:
    #             page = httptools.downloadpage(url, headers=headers).data
    #             url = '\t' + scrapertools.find_single_match(page, '<meta name="og:url" content="([^=]+)">')
    #         if url:
    #             listurl.add(url)
    # data += '\n'.join(listurl)
    info(data)
    itemlist = []
    # support.dbg()

    if '/serietv/series/names' in item.url:
        itemlist.extend(support.server(item, itemlist=hdpass(Item(url=item.url))))
    else:
        urls = support.match(data, patron=player_iframe).matches
        # support.dbg()
        if item.otherLinks:
            urls += support.match(item.otherLinks, patron=r'href="([^"]+)').matches

        info('URLS', urls)
        for u in urls:
            if 'hdplayer.casa/series/' in u:
                urls.remove(u)
                itemlist.extend(support.server(item, itemlist=hdpass(Item(url=u))))
                break
        else:
            itemlist.extend(support.server(item, urls))
        support.addQualityTag(item, itemlist, data, 'Keywords:\s*(?:<span>)?([^<]+)')
    return itemlist
