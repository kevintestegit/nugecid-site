#!/usr/bin/env python3
"""Valida o site estatico: links internos, metadados e imagens."""

import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGES = sorted(ROOT.glob("*.html"))
REQUIRED_META = ("description",)


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.title = ""
        self._in_title = False
        self.h1 = 0
        self.metas = {}
        self.links = []
        self.styles = []
        self.imgs = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "h1":
            self.h1 += 1
        elif tag == "meta":
            name = a.get("name")
            if name:
                self.metas[name.lower()] = a.get("content", "")
        elif tag == "a":
            self.links.append(a.get("href", ""))
        elif tag == "link" and a.get("rel") == "stylesheet":
            self.styles.append(a.get("href", ""))
        elif tag == "img":
            self.imgs.append((a.get("src", ""), a.get("alt"), a.get("loading")))

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def is_external(href):
    return href.startswith(
        ("http://", "https://", "//", "mailto:", "tel:", "#", "data:")
    )


def local_target(href):
    return (ROOT / href.split("#")[0].split("?")[0].lstrip("/")).resolve()


def check():
    errors = []
    if not PAGES:
        errors.append("nenhuma pagina .html encontrada na raiz")
    for page in PAGES:
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        rel = page.name
        if parser.lang != "pt-BR":
            errors.append(f"{rel}: lang deve ser pt-BR (achei {parser.lang!r})")
        if not parser.title.strip():
            errors.append(f"{rel}: <title> vazio")
        if parser.h1 != 1:
            errors.append(f"{rel}: esperado exatamente 1 <h1>, achei {parser.h1}")
        for meta in REQUIRED_META:
            if not parser.metas.get(meta):
                errors.append(f"{rel}: meta {meta} ausente ou vazia")
        for href in parser.links:
            if not href or is_external(href):
                continue
            if not local_target(href).exists():
                errors.append(f"{rel}: link quebrado -> {href}")
        for href in parser.styles:
            if not href or is_external(href):
                continue
            if not local_target(href).exists():
                errors.append(f"{rel}: folha de estilo ausente -> {href}")
        for src, alt, loading in parser.imgs:
            if not is_external(src) and not local_target(src).exists():
                errors.append(f"{rel}: imagem ausente -> {src}")
            if alt is None:
                errors.append(f"{rel}: <img src={src}> sem alt")
            if loading != "lazy":
                errors.append(f"{rel}: <img src={src}> sem loading=lazy")
    return errors


if __name__ == "__main__":
    errs = check()
    for err in errs:
        print(f"ERRO: {err}")
    print(f"{'FALHOU' if errs else 'OK'}: {len(PAGES)} paginas, {len(errs)} erro(s)")
    sys.exit(1 if errs else 0)
