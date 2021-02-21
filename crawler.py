# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import requests
import re
import os

from constantes import Constantes

from bs4 import BeautifulSoup

def retira_tag_xml(html):
    return re.sub('<[^<]+>', '', html)

def formata_lastmod(data):
    return re.sub('T.+', '', data)

def extrair_image(tag):
    """Extrai image URL de image:loc"""
    return re.sub(
        '<[^<]+>', '',
        re.search(
            '<image:loc>.+<\/image:loc>',
            tag
        ).group()
    )

def criar_xml(nome_arq, noticias):
    path = os.path.dirname(os.path.abspath(__file__))
    path += '/xml/'
    arq = open(path + nome_arq, 'w+')
    arq.close()

    with open(path + nome_arq, 'ab') as f:
        for n in noticias:
            xml = """<titulo>{}</titulo><url>{}</url><lastmod>{}</lastmod><img>{}</img>""".format(
                n['titulo'].encode('utf-8'),
                n['url'],
                n['lastmod'],
                n['image']
            )
            f.writelines(xml)

        f.close()

def pco(qtd_noticias=20, noticias_recentes=True):
    """Busca noticias do site do PCO."""
    r = requests.get(url=Constantes.SITEMAP_PCO)
    if r.status_code == 200:
        
        html_soup = BeautifulSoup(r.text, 'html.parser')
        sitemaps = html_soup.findAll('sitemap')
        l_sm = []
        for s in sitemaps:
            if re.search('post-sitemap', s.loc.get_text()):
                l_sm.append({
                    'url': s.loc.get_text(),
                    'lastmod': formata_lastmod(s.lastmod.get_text())
                })

        if l_sm:
            l_sm = sorted(
                l_sm,
                key=lambda k: k['lastmod'],
                reverse=True)

            from random import randint, shuffle

            if noticias_recentes:
                # pega sitemapset mais recente.
                url_sitemap = l_sm[0]['url']
            else:
                # pega randomico.
                url_sitemap = l_sm[randint(0, len(l_sm) - 1)]
                url_sitemap = retira_tag_xml(str(url))

            j = requests.get(url=url_sitemap)

            l_noticias = []
            html_soup = BeautifulSoup(j.text, 'lxml')
            
            for noticias in html_soup.findAll('url'):
                if re.search('<image:loc>.+<\/image:loc>', str(noticias)):
                    l_noticias.append({
                        'url': noticias.loc.get_text(),
                        'image': extrair_image(str(noticias)),
                        'lastmod': formata_lastmod(noticias.lastmod.get_text())
                    })
                else:
                    continue

            shuffle(l_noticias)
            if len(l_noticias) <= qtd_noticias:
                qtd_noticias = len(l_noticias)

            noticias_fmt = []
            for n in l_noticias[:qtd_noticias]:

                req_noticia = requests.get(url=n['url'])
                html_noticia = BeautifulSoup(req_noticia.text, 'html.parser')

                n['titulo'] = html_noticia.find(
                    "h1",
                    {"class": "elementor-heading-title elementor-size-default"}
                ).text

                noticias_fmt.append(n)

            print 'Iniciando geracao arquivo PCO.'
            criar_xml("noticias_pco.xml", noticias_fmt)


def tercalivre(qtd_noticias=20, noticias_recentes=True):
    """Busca noticias do site do TercaLivre."""
    r = requests.get(url=Constantes.SITEMAP_TERCALIVRE)
    if r.status_code == 200:
        
        html_soup = BeautifulSoup(r.text, 'html.parser')
        sitemaps = html_soup.findAll('sitemap')
        l_sm = []
        for s in sitemaps:
            if re.search('post-sitemap', s.loc.get_text()):
                l_sm.append({
                    'url': s.loc.get_text(),
                    'lastmod': formata_lastmod(s.lastmod.get_text())
                })

        if l_sm:
            l_sm = sorted(
                l_sm,
                key=lambda k: k['lastmod'],
                reverse=True)

            from random import randint, shuffle

            if noticias_recentes:
                # pega sitemapset mais recente.
                url_sitemap = l_sm[0]['url']
            else:
                # pega randomico.
                url_sitemap = l_sm[randint(0, len(l_sm) - 1)]
                url_sitemap = retira_tag_xml(str(url))

            j = requests.get(url=url_sitemap)

            l_noticias = []
            html_soup = BeautifulSoup(j.text, 'lxml')
            
            for noticias in html_soup.findAll('url'):
                if re.search('<image:loc>.+<\/image:loc>', str(noticias)):
                    l_noticias.append({
                        'url': noticias.loc.get_text(),
                        'image': extrair_image(str(noticias)),
                        'lastmod': formata_lastmod(noticias.lastmod.get_text())
                    })
                else:
                    continue


            shuffle(l_noticias)
            if len(l_noticias) <= qtd_noticias:
                qtd_noticias = len(l_noticias)

            noticias_fmt = []
            for n in l_noticias[:qtd_noticias]:

                req_noticia = requests.get(url=n['url'])
                html_noticia = BeautifulSoup(req_noticia.text, 'html.parser')

                n['titulo'] = html_noticia.find(
                    "h1",
                    {"class": "entry-title h1"}
                ).text

                noticias_fmt.append(n)

            print 'Iniciando geracao arquivo Terca-Livre.'
            criar_xml("noticias_tercalivre.xml", noticias_fmt)

def gerar_xml_sites():
    """Gera XML dos dois sites."""
    print 'Gerando XML do PCO...'
    pco()

    print '\n\n'

    print 'Gerando XML do Terca-Livre...'
    tercalivre()

gerar_xml_sites()