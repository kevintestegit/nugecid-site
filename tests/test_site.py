"""Regressões de conteúdo, navegação e recursos do site estático (stdlib)."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import unittest
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.links, self.ids, self.assets, self.data = [], set(), [], []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.add(a['id'])
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])
        if tag in ('img', 'script') and a.get('src'):
            self.assets.append(a['src'])

    def handle_data(self, data):
        self.data.append(data)

    @property
    def text(self):
        return ' '.join(' '.join(self.data).split())


class SiteRegression(unittest.TestCase):
    def test_internal_links_and_fragments(self):
        for path in ROOT.glob('*.html'):
            for link in Page(path).links:
                url = urlsplit(link)
                if url.scheme or url.netloc:
                    continue
                target = ROOT / unquote(url.path) if url.path else path
                with self.subTest(page=path.name, link=link):
                    self.assertTrue(target.is_file())
                    if url.fragment:
                        self.assertIn(unquote(url.fragment), Page(target).ids)

    def test_contacts_and_navigation_on_every_page(self):
        for path in ROOT.glob('*.html'):
            page = Page(path)
            with self.subTest(page=path.name):
                for href in ['mailto:arquivogeral@pci.rn.gov.br', 'tel:+558432326928',
                             'index.html', 'sgc.html', 'ojs.html', 'dspace.html',
                             'sistemas.html', 'sobre.html', 'noticias.html']:
                    self.assertIn(href, page.links)

    def test_original_book_cover_and_pdf(self):
        original_hash = '0f2f03333632ca0ab980e1bf2412c0341ecda507aa63e4ff5ceb11cedaee3d01'
        self.assertEqual(hashlib.sha256((ROOT/'assets/img/livro-capa.webp').read_bytes()).hexdigest(), original_hash)
        for name in ['index.html', 'noticia-lancamento-livro.html']:
            page = Page(ROOT/name)
            self.assertIn('https://drive.google.com/file/d/1_Sdru5ukTgvIwmae3blHcrNwCr5tB6G5/view', page.links)
            self.assertIn('978-65-01-06618-9', page.text)

    def test_original_institutional_information(self):
        page = Page(ROOT/'sobre.html')
        for fact in ['Setor de Arquivo Geral', 'CPAGED', 'CPGM', '588', '177', '126', '127']:
            self.assertIn(fact, page.text)
        home = Page(ROOT/'index.html')
        for fact in ['NestJS', 'React', 'PostgreSQL', 'Redis', '2024', '795', 'Em implantação']:
            self.assertIn(fact, home.text)

    def test_no_external_font_dependency(self):
        for path in ROOT.glob('*.html'):
            self.assertNotIn('fonts.googleapis.com', path.read_text())
        for name in ['newsreader.ttf', 'newsreader-italic.ttf', 'archivo.ttf', 'ibm-plex-mono.ttf']:
            self.assertTrue((ROOT/'assets/fonts'/name).is_file())


if __name__ == '__main__':
    unittest.main()
