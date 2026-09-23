# Site NUGECID — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publicar o site institucional e vitrine de sistemas do NUGECID/ITEP-RN em HTML/CSS puro no GitHub Pages.

**Architecture:** 7 páginas HTML estáticas na raiz do repositório + 1 CSS compartilhado + 1 script Python de verificação (`check.py`). Zero JavaScript, zero build, zero dependências. Deploy direto da branch `main` pelo GitHub Pages.

**Tech Stack:** HTML5, CSS3 (custom properties), Python 3 stdlib (`check.py`), GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-09-23-nugecid-site-design.md`

---

## Estrutura de arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `check.py` | Verificação automática: links internos, metadados, imagens |
| `assets/css/site.css` | Único CSS: tokens, tipografia, componentes |
| `index.html` | Home: hero, o que o Núcleo faz, fichas dos sistemas, livro, notícias |
| `sgc.html` | Sistema de Gestão de Documentos e Desarquivamentos |
| `ojs.html` | Revista da Polícia Científica do RN (RPCIRN) |
| `dspace.html` | Repositório institucional |
| `sobre.html` | Sobre o Núcleo + contato |
| `noticias.html` | Lista de notícias |
| `noticia-lancamento-livro.html` | Post: lançamento do livro |
| `noticia-sistemas-implantacao.html` | Post: implantação dos sistemas |
| `.nojekyll` | Impede processamento Jekyll no Pages |
| `README.md` | Como rodar a verificação e publicar |

**Ordem das tarefas:** o `check.py` é escrito primeiro (Tarefa 1) e usado como critério de
aceite em todas as tarefas seguintes. Ele falhará com "link quebrado" enquanto as páginas
linkadas ainda não existirem — isso é esperado. A Tarefa 10 exige zero erros.

**Placeholders marcados:** todo conteúdo provisório (contato, datas, títulos, prints) fica
com um comentário HTML `<!-- CONFIRMAR: ... -->` na linha. Onde aparecer "CONTATO_A_DEFINIR",
substituir pelo dado oficial antes de publicar.

---

### Task 1: `check.py`

**Files:**
- Create: `check.py`

- [ ] **Step 1: Escrever o script**

```python
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
    return href.startswith(("http://", "https://", "//", "mailto:", "tel:", "#", "data:"))


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
```

- [ ] **Step 2: Rodar e confirmar que falha (sem páginas ainda)**

Run: `python3 check.py`
Expected: `ERRO: nenhuma pagina .html encontrada na raiz` e exit code 1.

- [ ] **Step 3: Commit**

```bash
git add check.py
git commit -m "chore: script de verificacao do site estatico"
```

---

### Task 2: `assets/css/site.css`

**Files:**
- Create: `assets/css/site.css`

- [ ] **Step 1: Escrever o CSS completo**

```css
/* Site NUGECID — identidade "Dossie manila" */
:root {
  --paper: #ece3cf;
  --paper-light: #f4ecdb;
  --kraft: #d9c9a3;
  --ink: #2a2620;
  --ink-soft: #5c5648;
  --archive: #5f5a4e;
  --stamp: #a33127;
  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);
  --radius: 3px;
  --key-w: 6.5rem;
  --wrap: 72rem;
}

*, *::before, *::after { box-sizing: border-box; }

html { -webkit-text-size-adjust: 100%; }

body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font: 400 1rem/1.6 Archivo, system-ui, sans-serif;
}

img { max-width: 100%; height: auto; display: block; }

a {
  color: var(--stamp);
  text-decoration-thickness: 1px;
  text-underline-offset: 2px;
  transition: color 160ms var(--ease-out);
}

h1, h2, h3 { line-height: 1.15; letter-spacing: -0.01em; margin: 0 0 0.6em; }
h1 { font-size: clamp(2rem, 5vw, 3rem); font-weight: 700; }
h2 { font-size: 1.6rem; font-weight: 700; }
h3 { font-size: 1.2rem; font-weight: 600; }

p { margin: 0 0 1em; max-width: 72ch; }

a:focus-visible, button:focus-visible {
  outline: 2px solid var(--stamp);
  outline-offset: 2px;
}
.site-header a:focus-visible, .site-footer a:focus-visible { outline-color: var(--kraft); }

.wrap { width: min(100% - 2.5rem, var(--wrap)); margin-inline: auto; }

.skip-link { position: absolute; left: -999px; }
.skip-link:focus {
  left: 1rem; top: 1rem; z-index: 10;
  background: var(--ink); color: var(--paper); padding: 0.5rem 0.75rem;
}
.visually-hidden {
  position: absolute; width: 1px; height: 1px;
  margin: -1px; padding: 0; overflow: hidden;
  clip: rect(0 0 0 0); white-space: nowrap; border: 0;
}

/* Cabecalho */
.site-header { background: var(--ink); color: var(--paper); }
.site-header .wrap {
  display: flex; flex-wrap: wrap; gap: 0.75rem 1.5rem;
  align-items: center; justify-content: space-between;
  padding-block: 0.9rem;
}
.brand { display: flex; align-items: baseline; gap: 0.6rem; color: var(--paper); text-decoration: none; }
.brand-mark {
  font: 600 0.72rem/1 "IBM Plex Mono", monospace;
  letter-spacing: 0.14em; text-transform: uppercase; color: var(--kraft);
}
.brand-name { font-weight: 700; font-size: 1.15rem; }
.site-nav { display: flex; flex-wrap: wrap; gap: 0.25rem 0.35rem; }
.site-nav a {
  color: var(--paper); text-decoration: none;
  font: 600 0.85rem/1 Archivo, sans-serif;
  padding: 0.45rem 0.6rem; border-radius: var(--radius);
  transition: background-color 160ms var(--ease-out), color 160ms var(--ease-out);
}
.site-nav a[aria-current="page"] { background: var(--kraft); color: var(--ink); }

@media (hover: hover) and (pointer: fine) {
  a:hover { color: var(--ink); }
  .brand:hover { color: var(--kraft); }
  .site-nav a:hover { background: var(--kraft); color: var(--ink); }
  .btn:hover { background: var(--stamp); border-color: var(--stamp); color: #fff; }
  .btn--ghost:hover { background: var(--ink); border-color: var(--ink); color: var(--paper); }
  .news-list a:hover { color: var(--stamp); text-decoration: underline; }
  .site-footer a:hover { color: var(--kraft); }
}

/* Hero */
.hero { padding: clamp(2.5rem, 6vw, 5rem) 0 clamp(2rem, 4vw, 3.5rem); }
.kicker {
  display: block; margin-bottom: 0.9rem;
  font: 600 0.75rem/1 "IBM Plex Mono", monospace;
  letter-spacing: 0.18em; text-transform: uppercase; color: var(--stamp);
}
.lead { font-size: 1.15rem; color: var(--ink-soft); max-width: 60ch; }

/* Botoes */
.actions { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 1.5rem; }
.btn {
  display: inline-block;
  font: 600 0.9rem/1 Archivo, sans-serif;
  padding: 0.75rem 1.1rem;
  border: 2px solid var(--ink); border-radius: var(--radius);
  background: var(--ink); color: var(--paper); text-decoration: none;
  transition: transform 160ms var(--ease-out), background-color 160ms var(--ease-out),
    border-color 160ms var(--ease-out), color 160ms var(--ease-out);
}
.btn:active { transform: scale(0.97); }
.btn--ghost { background: transparent; color: var(--ink); }
.btn[aria-disabled="true"] {
  background: transparent; color: var(--archive); border-color: var(--archive);
  cursor: not-allowed;
}

/* Secoes */
.section { padding-block: clamp(2rem, 4vw, 3.5rem); }
.section--alt { background: var(--paper-light); }
.section h2 { margin-bottom: 1rem; }

.grid-2, .grid-3 { display: grid; gap: 1.25rem; grid-template-columns: 1fr; }
@media (min-width: 640px) { .grid-2, .grid-3 { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 960px) { .grid-3 { grid-template-columns: repeat(3, 1fr); } }

/* Ficha catalografica */
.ficha {
  display: flex; flex-direction: column; gap: 0.75rem;
  background: var(--paper-light); border: 1px solid var(--kraft);
  border-radius: var(--radius); padding: 1.25rem;
}
.ficha h3 { margin: 0; }
.ficha dl { margin: 0; font: 400 0.82rem/1.7 "IBM Plex Mono", monospace; }
.ficha dt { float: left; clear: left; width: var(--key-w); color: var(--archive); }
.ficha dd {
  margin: 0 0 0.35rem; padding-left: var(--key-w); padding-bottom: 0.35rem;
  border-bottom: 1px dotted var(--kraft);
}
.ficha dd:last-of-type { border-bottom: 0; }
.ficha .stamp { align-self: flex-start; }
.ficha .ficha-link { margin-top: auto; font-weight: 600; }

/* Carimbo */
.stamp {
  display: inline-block;
  border: 2px solid currentColor; border-radius: var(--radius);
  padding: 0.3rem 0.6rem;
  font: 700 0.68rem/1 "IBM Plex Mono", monospace;
  letter-spacing: 0.14em; text-transform: uppercase;
  transform: rotate(-3deg); color: var(--stamp);
}

/* Prosa */
.prose ul { padding-left: 1.2rem; max-width: 72ch; }
.prose li { margin-bottom: 0.4rem; }

/* Tabela de stack */
.table-wrap { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: 0.9rem; }
th, td { text-align: left; padding: 0.55rem 0.7rem; border-bottom: 1px solid var(--kraft); }
th {
  font: 600 0.75rem/1.4 "IBM Plex Mono", monospace;
  letter-spacing: 0.08em; text-transform: uppercase; color: var(--archive);
}

/* Noticias */
.news-list { list-style: none; margin: 0; padding: 0; max-width: 72ch; }
.news-list li { border-bottom: 1px dotted var(--kraft); padding: 1rem 0; }
.news-list time {
  display: block; margin-bottom: 0.25rem;
  font: 400 0.78rem/1.4 "IBM Plex Mono", monospace; color: var(--archive);
}
.news-list a { font-weight: 600; color: var(--ink); text-decoration: none; }

/* Rodape */
.site-footer { background: var(--ink); color: var(--kraft); margin-top: 3rem; }
.site-footer .wrap { padding-block: 2rem; }
.site-footer p { font-size: 0.85rem; margin: 0 0 0.35rem; max-width: 72ch; }
.site-footer a { color: var(--paper); }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add assets/css/site.css
git commit -m "feat: CSS do site com identidade dossie manila"
```

---

### Task 3: `index.html`

**Files:**
- Create: `index.html`

- [ ] **Step 1: Escrever a página**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NUGECID — Memória, informação e conhecimento do ITEP-RN</title>
<meta name="description" content="Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória do ITEP-RN: gestão documental, memória institucional, repositório digital e periódico científico.">
<meta property="og:title" content="NUGECID — Memória, informação e conhecimento do ITEP-RN">
<meta property="og:description" content="Gestão documental, memória institucional, repositório digital e periódico científico do ITEP-RN.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://kevintestegit.github.io/nugecid-site/">
<meta property="og:locale" content="pt_BR">
<link rel="canonical" href="https://kevintestegit.github.io/nugecid-site/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">
      <span class="brand-mark">ITEP-RN</span>
      <span class="brand-name">NUGECID</span>
    </a>
    <nav class="site-nav" aria-label="Principal">
      <a href="index.html" aria-current="page">Início</a>
      <a href="sgc.html">SGC</a>
      <a href="ojs.html">OJS</a>
      <a href="dspace.html">DSpace</a>
      <a href="sobre.html">Sobre</a>
      <a href="noticias.html">Notícias</a>
    </nav>
  </div>
</header>

<main id="conteudo">

  <section class="hero">
    <div class="wrap">
      <span class="kicker">Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória</span>
      <!-- CONFIRMAR: titulo oficial do hero -->
      <h1>Memória, informação e conhecimento da perícia criminal do Rio Grande do Norte</h1>
      <p class="lead">O NUGECID cuida do acervo documental, da memória institucional e da produção
      científica do Instituto Técnico-Científico de Perícia do Rio Grande do Norte.</p>
      <div class="actions">
        <a class="btn" href="#sistemas">Conhecer os sistemas</a>
        <a class="btn btn--ghost" href="sobre.html">Sobre o Núcleo</a>
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="wrap">
      <h2>O que o Núcleo faz</h2>
      <div class="grid-2">
        <div>
          <h3>Gestão documental</h3>
          <p>Coordena o Setor de Arquivo Geral e o Comitê Permanente de Avaliação e Gestão
          Documental, garantindo classificação, avaliação e destinação correta dos documentos.</p>
        </div>
        <div>
          <h3>Memória institucional</h3>
          <p>Pesquisa, preserva e dá acesso à história do ITEP-RN, com a Comissão Permanente de
          Gestão da Memória e o livro <em>Do Vestígio à Prova</em>.</p>
        </div>
        <div>
          <h3>Repositório digital</h3>
          <p>Implanta o repositório institucional em DSpace para reunir portarias, publicações e
          o acervo de memória em um só lugar, com acesso aberto.</p>
        </div>
        <div>
          <h3>Periódico científico</h3>
          <p>Mantém a Revista da Polícia Científica do Rio Grande do Norte, publicada em Open
          Journal Systems, com submissão e avaliação por pares.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="sistemas">
    <div class="wrap">
      <h2>Sistemas</h2>
      <div class="grid-3">

        <article class="ficha">
          <span class="stamp">Uso interno</span>
          <h3>SGC</h3>
          <dl>
            <dt>Nome</dt><dd>Sistema de Gestão de Documentos e Desarquivamentos</dd>
            <dt>Função</dt><dd>Desarquivamentos, anexos, termos e relatórios</dd>
            <dt>Stack</dt><dd>NestJS · React · PostgreSQL · Redis</dd>
            <dt>Situação</dt><dd>Em uso na PCIRN/ITEP-RN</dd>
          </dl>
          <a class="ficha-link" href="sgc.html">Ver detalhes</a>
        </article>

        <article class="ficha">
          <span class="stamp">Em implantação</span>
          <h3>OJS · RPCIRN</h3>
          <dl>
            <dt>Nome</dt><dd>Revista da Polícia Científica do Rio Grande do Norte</dd>
            <dt>Função</dt><dd>Periódico científico em acesso aberto</dd>
            <dt>Plataforma</dt><dd>Open Journal Systems</dd>
            <dt>Situação</dt><dd>Em implantação</dd>
          </dl>
          <a class="ficha-link" href="ojs.html">Ver detalhes</a>
        </article>

        <article class="ficha">
          <span class="stamp">Em implantação</span>
          <h3>DSpace</h3>
          <dl>
            <dt>Nome</dt><dd>Repositório Institucional do ITEP-RN</dd>
            <dt>Função</dt><dd>Portarias, publicações e acervo de memória</dd>
            <dt>Plataforma</dt><dd>DSpace</dd>
            <dt>Situação</dt><dd>Em implantação</dd>
          </dl>
          <a class="ficha-link" href="dspace.html">Ver detalhes</a>
        </article>

      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="wrap">
      <span class="kicker">Publicação institucional</span>
      <h2>Do Vestígio à Prova</h2>
      <p>A trajetória da perícia criminal no Rio Grande do Norte, em pesquisa conduzida pela
      Comissão Permanente de Gestão da Memória. Volume 1, 2024, ISBN 978-65-01-06618-9.</p>
      <div class="actions">
        <a class="btn" href="noticia-lancamento-livro.html">Sobre a publicação</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <h2>Últimas notícias</h2>
      <ul class="news-list">
        <!-- CONFIRMAR: data -->
        <li>
          <time datetime="2026">2026</time>
          <a href="noticia-sistemas-implantacao.html">NUGECID implanta repositório digital e periódico científico</a>
        </li>
        <!-- CONFIRMAR: data -->
        <li>
          <time datetime="2024">2024</time>
          <a href="noticia-lancamento-livro.html">ITEP-RN lança livro sobre a trajetória da perícia criminal</a>
        </li>
      </ul>
    </div>
  </section>

</main>

<footer class="site-footer">
  <div class="wrap">
    <p><strong>NUGECID</strong> — Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória</p>
    <p>Instituto Técnico-Científico de Perícia do Rio Grande do Norte — ITEP-RN</p>
    <!-- CONFIRMAR: e-mail e telefone oficiais -->
    <p>Contato: CONTATO_A_DEFINIR · <a href="sobre.html">Sobre e contato</a></p>
  </div>
</footer>

</body>
</html>
```

- [ ] **Step 2: Rodar verificação (falhas esperadas: páginas ainda não criadas)**

Run: `python3 check.py`
Expected: exit 1, erros do tipo `index.html: link quebrado -> sgc.html` (as demais páginas ainda não existem). Nenhum erro de metadado, `h1` ou imagem.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: home institucional do NUGECID"
```

---

### Task 4: `sgc.html`

**Files:**
- Create: `sgc.html`

- [ ] **Step 1: Escrever a página**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SGC — Sistema de Gestão de Documentos e Desarquivamentos | NUGECID</title>
<meta name="description" content="SGC é o sistema interno de gestão de documentos e desarquivamentos da Polícia Científica do Rio Grande do Norte, desenvolvido em NestJS e React.">
<meta property="og:title" content="SGC — Sistema de Gestão de Documentos e Desarquivamentos">
<meta property="og:description" content="Sistema interno de gestão de documentos e desarquivamentos da PCIRN/ITEP-RN.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://kevintestegit.github.io/nugecid-site/sgc.html">
<meta property="og:locale" content="pt_BR">
<link rel="canonical" href="https://kevintestegit.github.io/nugecid-site/sgc.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">
      <span class="brand-mark">ITEP-RN</span>
      <span class="brand-name">NUGECID</span>
    </a>
    <nav class="site-nav" aria-label="Principal">
      <a href="index.html">Início</a>
      <a href="sgc.html" aria-current="page">SGC</a>
      <a href="ojs.html">OJS</a>
      <a href="dspace.html">DSpace</a>
      <a href="sobre.html">Sobre</a>
      <a href="noticias.html">Notícias</a>
    </nav>
  </div>
</header>

<main id="conteudo">

  <section class="hero">
    <div class="wrap">
      <span class="stamp">Uso interno</span>
      <h1>SGC — Sistema de Gestão de Documentos e Desarquivamentos</h1>
      <p class="lead">Sistema que organiza os fluxos de desarquivamento, os documentos e os
      relatórios operacionais da Polícia Científica do Rio Grande do Norte.</p>
    </div>
  </section>

  <section class="section section--alt">
    <div class="wrap prose">
      <h2>O que o sistema faz</h2>
      <ul>
        <li>Gestão de desarquivamentos, anexos, termos e relatórios.</li>
        <li>Dashboard com estatísticas operacionais.</li>
        <li>Kanban de tarefas, projetos, checklists e comentários.</li>
        <li>Gestão de usuários, perfis de acesso e auditoria.</li>
        <li>Backup, restauração e verificações de saúde da aplicação.</li>
        <li>Notificações, busca unificada e integrações de apoio.</li>
      </ul>
      <p>O acesso é restrito à rede institucional da PCIRN/ITEP-RN, por se tratar de sistema
      com dados administrativos e documentais internos.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <h2>Stack técnica</h2>
      <div class="table-wrap">
        <table>
          <caption class="visually-hidden">Tecnologias usadas no SGC</caption>
          <thead>
            <tr><th scope="col">Camada</th><th scope="col">Tecnologia</th></tr>
          </thead>
          <tbody>
            <tr><th scope="row">Backend</th><td>NestJS, TypeScript, TypeORM</td></tr>
            <tr><th scope="row">Frontend</th><td>React, Vite, TypeScript, TailwindCSS</td></tr>
            <tr><th scope="row">Banco de dados</th><td>PostgreSQL</td></tr>
            <tr><th scope="row">Cache e sessões</th><td>Redis</td></tr>
            <tr><th scope="row">Infraestrutura</th><td>Docker Compose, Nginx</td></tr>
            <tr><th scope="row">Testes</th><td>Jest, Vitest, Testing Library, Playwright</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="wrap">
      <h2>Telas do sistema</h2>
      <!-- CONFIRMAR: substituir por prints reais (assets/img/sgc-*.webp), com width, height, alt e loading="lazy" -->
      <p>Imagens do sistema serão publicadas aqui após revisão institucional.</p>
      <div class="actions">
        <a class="btn btn--ghost" href="index.html#sistemas">Voltar aos sistemas</a>
      </div>
    </div>
  </section>

</main>

<footer class="site-footer">
  <div class="wrap">
    <p><strong>NUGECID</strong> — Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória</p>
    <p>Instituto Técnico-Científico de Perícia do Rio Grande do Norte — ITEP-RN</p>
    <!-- CONFIRMAR: e-mail e telefone oficiais -->
    <p>Contato: CONTATO_A_DEFINIR · <a href="sobre.html">Sobre e contato</a></p>
  </div>
</footer>

</body>
</html>
```

Nota: a classe `visually-hidden` usada no `<caption>` já está definida em `site.css` (Tarefa 2).

- [ ] **Step 2: Rodar verificação**

Run: `python3 check.py`
Expected: exit 1, apenas erros de link quebrado para páginas ainda não criadas (`ojs.html`,
`dspace.html`, `sobre.html`, `noticias.html`, posts). Nenhum erro de metadado.

- [ ] **Step 3: Commit**

```bash
git add sgc.html
git commit -m "feat: pagina do SGC com stack e funcionalidades"
```

---

### Task 5: `ojs.html`

**Files:**
- Create: `ojs.html`

- [ ] **Step 1: Escrever a página**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RPCIRN — Revista da Polícia Científica do Rio Grande do Norte | NUGECID</title>
<meta name="description" content="Revista da Polícia Científica do Rio Grande do Norte: periódico científico em acesso aberto mantido pelo NUGECID, publicado em Open Journal Systems.">
<meta property="og:title" content="RPCIRN — Revista da Polícia Científica do Rio Grande do Norte">
<meta property="og:description" content="Periódico científico em acesso aberto mantido pelo NUGECID/ITEP-RN.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://kevintestegit.github.io/nugecid-site/ojs.html">
<meta property="og:locale" content="pt_BR">
<link rel="canonical" href="https://kevintestegit.github.io/nugecid-site/ojs.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">
      <span class="brand-mark">ITEP-RN</span>
      <span class="brand-name">NUGECID</span>
    </a>
    <nav class="site-nav" aria-label="Principal">
      <a href="index.html">Início</a>
      <a href="sgc.html">SGC</a>
      <a href="ojs.html" aria-current="page">OJS</a>
      <a href="dspace.html">DSpace</a>
      <a href="sobre.html">Sobre</a>
      <a href="noticias.html">Notícias</a>
    </nav>
  </div>
</header>

<main id="conteudo">

  <section class="hero">
    <div class="wrap">
      <span class="stamp">Em implantação</span>
      <h1>Revista da Polícia Científica do Rio Grande do Norte</h1>
      <p class="lead">Periódico científico do ITEP-RN, mantido pelo NUGECID e publicado em
      Open Journal Systems, com submissão e avaliação por pares.</p>
    </div>
  </section>

  <section class="section section--alt">
    <div class="wrap prose">
      <h2>Sobre a revista</h2>
      <p>A RPCIRN reúne produção científica nas áreas de criminalística, medicina legal,
      identificação civil e temas afins da perícia oficial, aproximando o conhecimento técnico
      produzido no estado da comunidade acadêmica e da sociedade.</p>
      <!-- CONFIRMAR: secoes, periodicidade, ISSN e politica de acesso com a equipe editorial -->
      <ul>
        <li>Submissão de artigos pelo sistema OJS.</li>
        <li>Avaliação por pares.</li>
        <li>Acesso aberto ao conteúdo publicado.</li>
      </ul>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <h2>Acesso</h2>
      <!-- SLOT DE URL: quando a revista estiver publicada, trocar o botao abaixo por
           <a class="btn" href="https://URL-DA-REVISTA">Acessar revista</a> -->
      <p>A revista está em processo de implantação. O endereço de acesso será publicado aqui
      assim que o portal entrar no ar.</p>
      <p><span class="btn" aria-disabled="true">Acessar revista — em breve</span></p>
      <div class="actions">
        <a class="btn btn--ghost" href="index.html#sistemas">Voltar aos sistemas</a>
      </div>
    </div>
  </section>

</main>

<footer class="site-footer">
  <div class="wrap">
    <p><strong>NUGECID</strong> — Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória</p>
    <p>Instituto Técnico-Científico de Perícia do Rio Grande do Norte — ITEP-RN</p>
    <!-- CONFIRMAR: e-mail e telefone oficiais -->
    <p>Contato: CONTATO_A_DEFINIR · <a href="sobre.html">Sobre e contato</a></p>
  </div>
</footer>

</body>
</html>
```

- [ ] **Step 2: Rodar verificação**

Run: `python3 check.py`
Expected: exit 1, apenas links quebrados de páginas ainda não criadas.

- [ ] **Step 3: Commit**

```bash
git add ojs.html
git commit -m "feat: pagina da revista RPCIRN (OJS)"
```

---

### Task 6: `dspace.html`

**Files:**
- Create: `dspace.html`

- [ ] **Step 1: Escrever a página**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Repositório Institucional — DSpace | NUGECID</title>
<meta name="description" content="Repositório institucional do ITEP-RN em DSpace: portarias, publicações institucionais, acervo de memória e produção científica, mantido pelo NUGECID.">
<meta property="og:title" content="Repositório Institucional do ITEP-RN — DSpace">
<meta property="og:description" content="Portarias, publicações e acervo de memória do ITEP-RN em acesso aberto.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://kevintestegit.github.io/nugecid-site/dspace.html">
<meta property="og:locale" content="pt_BR">
<link rel="canonical" href="https://kevintestegit.github.io/nugecid-site/dspace.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">
      <span class="brand-mark">ITEP-RN</span>
      <span class="brand-name">NUGECID</span>
    </a>
    <nav class="site-nav" aria-label="Principal">
      <a href="index.html">Início</a>
      <a href="sgc.html">SGC</a>
      <a href="ojs.html">OJS</a>
      <a href="dspace.html" aria-current="page">DSpace</a>
      <a href="sobre.html">Sobre</a>
      <a href="noticias.html">Notícias</a>
    </nav>
  </div>
</header>

<main id="conteudo">

  <section class="hero">
    <div class="wrap">
      <span class="stamp">Em implantação</span>
      <h1>Repositório Institucional do ITEP-RN</h1>
      <p class="lead">Memória, documentos e produção científica do Instituto em um acervo
      digital de acesso aberto, construído em DSpace.</p>
    </div>
  </section>

  <section class="section section--alt">
    <div class="wrap prose">
      <h2>O que o repositório reúne</h2>
      <ul>
        <li>Portarias e atos normativos do ITEP-RN.</li>
        <li>Publicações institucionais, como o livro <em>Do Vestígio à Prova</em>.</li>
        <li>Documentos e fotografias do acervo de memória institucional.</li>
        <li>Produção técnica e científica da perícia oficial.</li>
      </ul>
      <!-- CONFIRMAR: nomes das comunidades e colecoes com a equipe do NUGECID -->
      <p>O material é organizado em comunidades e coleções, com metadados padronizados que
      facilitam a busca e a citação.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap prose">
      <h2>Como depositar</h2>
      <p>Servidores e setores do ITEP-RN podem encaminhar documentos e acervos ao NUGECID para
      avaliação e depósito no repositório. A equipe do Núcleo orienta sobre formatos, metadados
      e direitos de publicação.</p>
      <!-- SLOT DE URL: quando o repositorio estiver publicado, trocar o botao abaixo por
           <a class="btn" href="https://URL-DO-REPOSITORIO">Acessar repositório</a> -->
      <p>O repositório está em processo de implantação. O endereço de acesso será publicado
      aqui assim que o portal entrar no ar.</p>
      <p><span class="btn" aria-disabled="true">Acessar repositório — em breve</span></p>
      <div class="actions">
        <a class="btn btn--ghost" href="index.html#sistemas">Voltar aos sistemas</a>
      </div>
    </div>
  </section>

</main>

<footer class="site-footer">
  <div class="wrap">
    <p><strong>NUGECID</strong> — Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória</p>
    <p>Instituto Técnico-Científico de Perícia do Rio Grande do Norte — ITEP-RN</p>
    <!-- CONFIRMAR: e-mail e telefone oficiais -->
    <p>Contato: CONTATO_A_DEFINIR · <a href="sobre.html">Sobre e contato</a></p>
  </div>
</footer>

</body>
</html>
```

- [ ] **Step 2: Rodar verificação**

Run: `python3 check.py`
Expected: exit 1, apenas links quebrados de páginas ainda não criadas.

- [ ] **Step 3: Commit**

```bash
git add dspace.html
git commit -m "feat: pagina do repositorio institucional (DSpace)"
```

---

### Task 7: `sobre.html`

**Files:**
- Create: `sobre.html`

- [ ] **Step 1: Escrever a página**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sobre o NUGECID — Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória</title>
<meta name="description" content="Conheça o NUGECID do ITEP-RN: criação pela Portaria 127/2023, atribuições de gestão documental e memória institucional, equipe e contato.">
<meta property="og:title" content="Sobre o NUGECID — ITEP-RN">
<meta property="og:description" content="Gestão documental, memória institucional e informação no ITEP-RN.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://kevintestegit.github.io/nugecid-site/sobre.html">
<meta property="og:locale" content="pt_BR">
<link rel="canonical" href="https://kevintestegit.github.io/nugecid-site/sobre.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">
      <span class="brand-mark">ITEP-RN</span>
      <span class="brand-name">NUGECID</span>
    </a>
    <nav class="site-nav" aria-label="Principal">
      <a href="index.html">Início</a>
      <a href="sgc.html">SGC</a>
      <a href="ojs.html">OJS</a>
      <a href="dspace.html">DSpace</a>
      <a href="sobre.html" aria-current="page">Sobre</a>
      <a href="noticias.html">Notícias</a>
    </nav>
  </div>
</header>

<main id="conteudo">

  <section class="hero">
    <div class="wrap">
      <span class="kicker">Portaria nº 127, de 29 de março de 2023</span>
      <h1>Sobre o NUGECID</h1>
      <p class="lead">O Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória é
      vinculado à Diretoria Geral do ITEP-RN e responde pela gestão documental, pela informação
      e pela memória institucional do órgão.</p>
    </div>
  </section>

  <section class="section section--alt">
    <div class="wrap prose">
      <h2>Atribuições</h2>
      <ul>
        <li>Assessorar a gestão documental produzida e acumulada pelo ITEP-RN.</li>
        <li>Coordenar o Setor de Arquivo Geral (SAG).</li>
        <li>Secretariar o Comitê Permanente de Avaliação e Gestão Documental (CPAGED).</li>
        <li>Promover a gestão da memória institucional, da informação e do conhecimento.</li>
        <li>Desenvolver o repositório digital institucional e o periódico científico.</li>
      </ul>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <h2>Estruturas e comissões</h2>
      <div class="grid-3">
        <article class="ficha">
          <h3>SAG</h3>
          <dl>
            <dt>Nome</dt><dd>Setor de Arquivo Geral</dd>
            <dt>Criação</dt><dd>Portaria nº 588, de 23/12/2022</dd>
          </dl>
        </article>
        <article class="ficha">
          <h3>CPAGED</h3>
          <dl>
            <dt>Nome</dt><dd>Comitê Permanente de Avaliação e Gestão Documental</dd>
            <dt>Criação</dt><dd>Portaria nº 177, de 10/05/2023</dd>
          </dl>
        </article>
        <article class="ficha">
          <h3>CPGM</h3>
          <dl>
            <dt>Nome</dt><dd>Comissão Permanente de Gestão da Memória</dd>
            <dt>Criação</dt><dd>Portaria nº 126, de 29/03/2023</dd>
          </dl>
        </article>
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="wrap prose">
      <h2>Equipe</h2>
      <p>O Núcleo conta com equipe multidisciplinar de biblioteconomia, história, arquivologia e
      tecnologia da informação.</p>
      <!-- CONFIRMAR: incluir nomes e funcoes da equipe, se autorizado -->
    </div>
  </section>

  <section class="section">
    <div class="wrap prose">
      <h2>Contato</h2>
      <!-- CONFIRMAR: e-mail, telefone, endereco e horario oficiais -->
      <p>E-mail: CONTATO_A_DEFINIR<br>
      Telefone: CONTATO_A_DEFINIR<br>
      Endereço: CONTATO_A_DEFINIR</p>
      <p>Para solicitações de pesquisa no acervo, depósito de documentos e demais demandas,
      entre em contato pelo canal institucional.</p>
    </div>
  </section>

</main>

<footer class="site-footer">
  <div class="wrap">
    <p><strong>NUGECID</strong> — Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória</p>
    <p>Instituto Técnico-Científico de Perícia do Rio Grande do Norte — ITEP-RN</p>
    <p>Contato: CONTATO_A_DEFINIR</p>
  </div>
</footer>

</body>
</html>
```

- [ ] **Step 2: Rodar verificação**

Run: `python3 check.py`
Expected: exit 1, apenas links quebrados de páginas ainda não criadas (`noticias.html` e posts).

- [ ] **Step 3: Commit**

```bash
git add sobre.html
git commit -m "feat: pagina sobre o Nucleo e contato"
```

---

### Task 8: Notícias (lista + 2 posts)

**Files:**
- Create: `noticias.html`
- Create: `noticia-lancamento-livro.html`
- Create: `noticia-sistemas-implantacao.html`

- [ ] **Step 1: Escrever `noticias.html`**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Notícias | NUGECID — ITEP-RN</title>
<meta name="description" content="Notícias do Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória do ITEP-RN.">
<meta property="og:title" content="Notícias | NUGECID — ITEP-RN">
<meta property="og:description" content="Publicações e novidades do NUGECID/ITEP-RN.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://kevintestegit.github.io/nugecid-site/noticias.html">
<meta property="og:locale" content="pt_BR">
<link rel="canonical" href="https://kevintestegit.github.io/nugecid-site/noticias.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">
      <span class="brand-mark">ITEP-RN</span>
      <span class="brand-name">NUGECID</span>
    </a>
    <nav class="site-nav" aria-label="Principal">
      <a href="index.html">Início</a>
      <a href="sgc.html">SGC</a>
      <a href="ojs.html">OJS</a>
      <a href="dspace.html">DSpace</a>
      <a href="sobre.html">Sobre</a>
      <a href="noticias.html" aria-current="page">Notícias</a>
    </nav>
  </div>
</header>

<main id="conteudo">

  <section class="hero">
    <div class="wrap">
      <h1>Notícias</h1>
      <p class="lead">Publicações, sistemas e novidades do NUGECID.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <ul class="news-list">
        <!-- CONFIRMAR: data -->
        <li>
          <time datetime="2026">2026</time>
          <a href="noticia-sistemas-implantacao.html">NUGECID implanta repositório digital e periódico científico</a>
        </li>
        <!-- CONFIRMAR: data -->
        <li>
          <time datetime="2024">2024</time>
          <a href="noticia-lancamento-livro.html">ITEP-RN lança livro sobre a trajetória da perícia criminal</a>
        </li>
      </ul>
    </div>
  </section>

</main>

<footer class="site-footer">
  <div class="wrap">
    <p><strong>NUGECID</strong> — Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória</p>
    <p>Instituto Técnico-Científico de Perícia do Rio Grande do Norte — ITEP-RN</p>
    <p>Contato: CONTATO_A_DEFINIR · <a href="sobre.html">Sobre e contato</a></p>
  </div>
</footer>

</body>
</html>
```

- [ ] **Step 2: Escrever `noticia-lancamento-livro.html`**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ITEP-RN lança livro sobre a trajetória da perícia criminal | NUGECID</title>
<meta name="description" content="O livro Do Vestígio à Prova: A Trajetória da Perícia Criminal no Rio Grande do Norte reúne pesquisa da Comissão Permanente de Gestão da Memória do ITEP-RN.">
<meta property="og:title" content="ITEP-RN lança livro sobre a trajetória da perícia criminal">
<meta property="og:description" content="Pesquisa da CPGM resgata a memória institucional do ITEP-RN.">
<meta property="og:type" content="article">
<meta property="og:url" content="https://kevintestegit.github.io/nugecid-site/noticia-lancamento-livro.html">
<meta property="og:locale" content="pt_BR">
<link rel="canonical" href="https://kevintestegit.github.io/nugecid-site/noticia-lancamento-livro.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">
      <span class="brand-mark">ITEP-RN</span>
      <span class="brand-name">NUGECID</span>
    </a>
    <nav class="site-nav" aria-label="Principal">
      <a href="index.html">Início</a>
      <a href="sgc.html">SGC</a>
      <a href="ojs.html">OJS</a>
      <a href="dspace.html">DSpace</a>
      <a href="sobre.html">Sobre</a>
      <a href="noticias.html" aria-current="true">Notícias</a>
    </nav>
  </div>
</header>

<main id="conteudo">

  <article class="section">
    <div class="wrap prose">
      <!-- CONFIRMAR: data exata de lancamento -->
      <p><time datetime="2024">2024</time></p>
      <h1>ITEP-RN lança livro sobre a trajetória da perícia criminal</h1>
      <p>O Instituto Técnico-Científico de Perícia do Rio Grande do Norte publicou o livro
      <em>Do Vestígio à Prova: A Trajetória da Perícia Criminal no Rio Grande do Norte</em>,
      volume 1, resultado de pesquisa conduzida pela Comissão Permanente de Gestão da Memória
      (CPGM) com o Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória
      (NUGECID).</p>
      <p>A obra resgata marcos legais, personagens e inovações que moldaram a perícia oficial
      no estado, a partir de documentos históricos, acervo do Diário Oficial, entrevistas com
      servidores e fotografias das unidades do Instituto.</p>
      <p>O livro tem 158 páginas, ISBN 978-65-01-06618-9 e integra o projeto de memória
      institucional do NUGECID. A versão digital será disponibilizada no repositório
      institucional em implantação.</p>
      <div class="actions">
        <a class="btn btn--ghost" href="noticias.html">Voltar às notícias</a>
      </div>
    </div>
  </article>

</main>

<footer class="site-footer">
  <div class="wrap">
    <p><strong>NUGECID</strong> — Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória</p>
    <p>Instituto Técnico-Científico de Perícia do Rio Grande do Norte — ITEP-RN</p>
    <p>Contato: CONTATO_A_DEFINIR · <a href="sobre.html">Sobre e contato</a></p>
  </div>
</footer>

</body>
</html>
```

- [ ] **Step 3: Escrever `noticia-sistemas-implantacao.html`**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NUGECID implanta repositório digital e periódico científico | NUGECID</title>
<meta name="description" content="O NUGECID avança na implantação do repositório institucional em DSpace e da Revista da Polícia Científica do RN em Open Journal Systems.">
<meta property="og:title" content="NUGECID implanta repositório digital e periódico científico">
<meta property="og:description" content="Repositório em DSpace e revista em OJS ampliam o acesso à informação do ITEP-RN.">
<meta property="og:type" content="article">
<meta property="og:url" content="https://kevintestegit.github.io/nugecid-site/noticia-sistemas-implantacao.html">
<meta property="og:locale" content="pt_BR">
<link rel="canonical" href="https://kevintestegit.github.io/nugecid-site/noticia-sistemas-implantacao.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">
      <span class="brand-mark">ITEP-RN</span>
      <span class="brand-name">NUGECID</span>
    </a>
    <nav class="site-nav" aria-label="Principal">
      <a href="index.html">Início</a>
      <a href="sgc.html">SGC</a>
      <a href="ojs.html">OJS</a>
      <a href="dspace.html">DSpace</a>
      <a href="sobre.html">Sobre</a>
      <a href="noticias.html" aria-current="true">Notícias</a>
    </nav>
  </div>
</header>

<main id="conteudo">

  <article class="section">
    <div class="wrap prose">
      <!-- CONFIRMAR: data -->
      <p><time datetime="2026">2026</time></p>
      <h1>NUGECID implanta repositório digital e periódico científico</h1>
      <p>O Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória trabalha na
      implantação de dois sistemas que ampliam o acesso à informação do ITEP-RN: o repositório
      institucional, em DSpace, e a Revista da Polícia Científica do Rio Grande do Norte, em
      Open Journal Systems.</p>
      <p>O repositório vai reunir portarias, publicações institucionais e o acervo de memória
      em um ambiente de acesso aberto, com metadados padronizados para busca e citação. Já a
      revista dará fluxo editorial completo à produção científica da perícia oficial, com
      submissão e avaliação por pares.</p>
      <p>Além dos dois sistemas, o Núcleo mantém o SGC — Sistema de Gestão de Documentos e
      Desarquivamentos — em operação interna na Polícia Científica do Rio Grande do Norte.</p>
      <div class="actions">
        <a class="btn btn--ghost" href="noticias.html">Voltar às notícias</a>
      </div>
    </div>
  </article>

</main>

<footer class="site-footer">
  <div class="wrap">
    <p><strong>NUGECID</strong> — Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória</p>
    <p>Instituto Técnico-Científico de Perícia do Rio Grande do Norte — ITEP-RN</p>
    <p>Contato: CONTATO_A_DEFINIR · <a href="sobre.html">Sobre e contato</a></p>
  </div>
</footer>

</body>
</html>
```

- [ ] **Step 4: Rodar verificação (deve passar)**

Run: `python3 check.py`
Expected: `OK: 8 paginas, 0 erro(s)`, exit code 0.

- [ ] **Step 5: Commit**

```bash
git add noticias.html noticia-lancamento-livro.html noticia-sistemas-implantacao.html
git commit -m "feat: secao de noticias com dois posts iniciais"
```

---

### Task 9: `.nojekyll` e `README.md`

**Files:**
- Create: `.nojekyll`
- Create: `README.md`

- [ ] **Step 1: Criar `.nojekyll` (arquivo vazio)**

```bash
touch .nojekyll
```

- [ ] **Step 2: Escrever `README.md`**

```markdown
# Site NUGECID

Site institucional e vitrine de sistemas do NUGECID — Núcleo de Gestão do Conhecimento,
Informação, Documentação e Memória do ITEP-RN.

Publicado em: https://kevintestegit.github.io/nugecid-site/

## Estrutura

- Páginas HTML na raiz (`index.html`, `sgc.html`, `ojs.html`, `dspace.html`, `sobre.html`,
  `noticias.html` e posts).
- `assets/css/site.css` — único CSS, identidade "dossiê manila".
- `check.py` — verificação de links internos, metadados e imagens.
- `docs/superpowers/` — spec e plano de implementação.

## Verificação

```bash
python3 check.py
```

Exit code 0 = tudo certo. Verifica: links internos existem, cada página tem `lang="pt-BR"`,
`<title>`, um `<h1>` e `meta description`, e toda `<img>` tem `alt` e `loading="lazy"`.

## Publicação

GitHub Pages, branch `main`, raiz do repositório. Sem build e sem Actions.

1. Criar o repositório `nugecid-site` na conta `kevintestegit`.
2. `git remote add origin git@github.com:kevintestegit/nugecid-site.git`
3. `git push -u origin main`
4. Settings → Pages → Source: "Deploy from a branch" → Branch: `main` / `/ (root)`.

## Pendências de conteúdo

Itens marcados com `<!-- CONFIRMAR: ... -->` no HTML: contato oficial, datas das notícias,
título do hero, prints dos sistemas e textos institucionais revisados.
```

- [ ] **Step 3: Commit**

```bash
git add .nojekyll README.md
git commit -m "docs: README e .nojekyll para o GitHub Pages"
```

---

### Task 10: Verificação final e publicação

**Files:**
- Nenhum arquivo novo (apenas verificação e deploy).

- [ ] **Step 1: Rodar a verificação final**

Run: `python3 check.py`
Expected: `OK: 8 paginas, 0 erro(s)`.

- [ ] **Step 2: Revisar acessibilidade no navegador (manual, 5 minutos)**

Abrir `index.html` no navegador e conferir:

- Navegação por `Tab` alcança skip-link, marca, todos os itens do menu e o conteúdo.
- Foco visível (contorno vermelho) em todos os elementos interativos.
- Zoom em 200% sem quebra de layout.
- Larguras de 360px, 768px e 1280px sem rolagem horizontal.
- Com `prefers-reduced-motion` ativado no sistema, não há transições perceptíveis.

- [ ] **Step 3: Publicar**

```bash
git remote add origin git@github.com:kevintestegit/nugecid-site.git
git push -u origin main
```

Se o repositório ainda não existir no GitHub, criar antes (web ou
`gh repo create kevintestegit/nugecid-site --public --source=. --push`).
Depois: Settings → Pages → Source "Deploy from a branch" → `main` / `/ (root)`.

Expected: site disponível em `https://kevintestegit.github.io/nugecid-site/` após 1–2 minutos.

- [ ] **Step 4: Conferir o site publicado**

Abrir a URL publicada e repetir: todas as páginas carregam, fontes carregam, menu funciona
em todas as páginas, selos e fichas aparecem corretos.

---

### Task 11: Renomeação do órgão (LC 795/2025) e fix do `aria-current`

**Contexto:** A Lei Complementar nº 795, de 08/10/2025 (DOE 09/10/2025) renomeou o
"Instituto Técnico-Científico de Perícia do Rio Grande do Norte (ITEP/RN)" para
**Polícia Científica do Rio Grande do Norte**. Decisão aprovada: usar só o nome novo,
com nota histórica onde o texto citar fatos de 2023–2024. Esta tarefa substitui os
nomes nas tarefas anteriores.

**Files:**
- Modify: `index.html`, `sgc.html`, `ojs.html`, `dspace.html`, `sobre.html`,
  `noticias.html`, `noticia-lancamento-livro.html`, `noticia-sistemas-implantacao.html`
- Modify: `assets/css/site.css`

- [ ] **Step 1: Marca do header (8 páginas)**

Em cada um dos 8 arquivos HTML, substituir:

```html
<span class="brand-mark">ITEP-RN</span>
```

por:

```html
<span class="brand-mark">PCIRN</span>
```

- [ ] **Step 2: Rodapé (8 páginas)**

Em cada um dos 8 arquivos HTML, substituir:

```html
<p>Instituto Técnico-Científico de Perícia do Rio Grande do Norte — ITEP-RN</p>
```

por:

```html
<p>Polícia Científica do Rio Grande do Norte</p>
```

- [ ] **Step 3: `index.html`**

```text
<title>NUGECID — Memória, informação e conhecimento do ITEP-RN</title>
→ <title>NUGECID — Memória, informação e conhecimento da Polícia Científica do RN</title>

content="Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória do ITEP-RN: gestão documental, memória institucional, repositório digital e periódico científico."
→ content="Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória da Polícia Científica do RN: gestão documental, memória institucional, repositório digital e periódico científico."

content="NUGECID — Memória, informação e conhecimento do ITEP-RN"
→ content="NUGECID — Memória, informação e conhecimento da Polícia Científica do RN"

content="Gestão documental, memória institucional, repositório digital e periódico científico do ITEP-RN."
→ content="Gestão documental, memória institucional, repositório digital e periódico científico da Polícia Científica do RN."

científica do Instituto Técnico-Científico de Perícia do Rio Grande do Norte.
→ científica da Polícia Científica do Rio Grande do Norte.

<p>Pesquisa, preserva e dá acesso à história do ITEP-RN, com a Comissão Permanente de
→ <p>Pesquisa, preserva e dá acesso à história da instituição, com a Comissão Permanente de

<dt>Situação</dt><dd>Em uso na PCIRN/ITEP-RN</dd>
→ <dt>Situação</dt><dd>Em uso na PCIRN</dd>

<dt>Nome</dt><dd>Repositório Institucional do ITEP-RN</dd>
→ <dt>Nome</dt><dd>Repositório Institucional da Polícia Científica do RN</dd>

<a href="noticia-lancamento-livro.html">ITEP-RN lança livro sobre a trajetória da perícia criminal</a>
→ <a href="noticia-lancamento-livro.html">Polícia Científica do RN lança livro sobre a trajetória da perícia criminal</a>
```

E na seção do livro, após o parágrafo que termina em "ISBN 978-65-01-06618-9.", acrescentar:

```html
      <p>O livro foi publicado em 2024, quando o órgão ainda se chamava Instituto
      Técnico-Científico de Perícia do Rio Grande do Norte (ITEP-RN), renomeado pela
      Lei Complementar nº 795, de 8 de outubro de 2025.</p>
```

- [ ] **Step 4: `sgc.html`**

```text
content="Sistema interno de gestão de documentos e desarquivamentos da PCIRN/ITEP-RN."
→ content="Sistema interno de gestão de documentos e desarquivamentos da PCIRN."

<p>O acesso é restrito à rede institucional da PCIRN/ITEP-RN, por se tratar de sistema
→ <p>O acesso é restrito à rede institucional da PCIRN, por se tratar de sistema
```

- [ ] **Step 5: `ojs.html`**

```text
content="Periódico científico em acesso aberto mantido pelo NUGECID/ITEP-RN."
→ content="Periódico científico em acesso aberto mantido pelo NUGECID."

<p class="lead">Periódico científico do ITEP-RN, mantido pelo NUGECID e publicado em
→ <p class="lead">Periódico científico da Polícia Científica do RN, mantido pelo NUGECID e publicado em
```

- [ ] **Step 6: `dspace.html`**

```text
content="Repositório institucional do ITEP-RN em DSpace: portarias, publicações institucionais, acervo de memória e produção científica, mantido pelo NUGECID."
→ content="Repositório institucional da Polícia Científica do RN em DSpace: portarias, publicações institucionais, acervo de memória e produção científica, mantido pelo NUGECID."

content="Repositório Institucional do ITEP-RN — DSpace"
→ content="Repositório Institucional da Polícia Científica do RN — DSpace"

content="Portarias, publicações e acervo de memória do ITEP-RN em acesso aberto."
→ content="Portarias, publicações e acervo de memória da Polícia Científica do RN em acesso aberto."

<h1>Repositório Institucional do ITEP-RN</h1>
→ <h1>Repositório Institucional da Polícia Científica do RN</h1>

<li>Portarias e atos normativos do ITEP-RN.</li>
→ <li>Portarias e atos normativos da Polícia Científica do RN.</li>

<p>Servidores e setores do ITEP-RN podem encaminhar documentos e acervos ao NUGECID para
→ <p>Servidores e setores da Polícia Científica do RN podem encaminhar documentos e acervos ao NUGECID para
```

- [ ] **Step 7: `sobre.html`**

```text
content="Conheça o NUGECID do ITEP-RN: criação pela Portaria 127/2023, atribuições de gestão documental e memória institucional, equipe e contato."
→ content="Conheça o NUGECID da Polícia Científica do RN: criação pela Portaria 127/2023, atribuições de gestão documental e memória institucional, equipe e contato."

content="Sobre o NUGECID — ITEP-RN"
→ content="Sobre o NUGECID — Polícia Científica do RN"

content="Gestão documental, memória institucional e informação no ITEP-RN."
→ content="Gestão documental, memória institucional e informação na Polícia Científica do RN."

vinculado à Diretoria Geral do ITEP-RN e responde pela gestão documental, pela informação
→ vinculado à Diretoria Geral da Polícia Científica do Rio Grande do Norte (à época da
criação, ITEP-RN) e responde pela gestão documental, pela informação

<li>Assessorar a gestão documental produzida e acumulada pelo ITEP-RN.</li>
→ <li>Assessorar a gestão documental produzida e acumulada pela Polícia Científica do RN.</li>
```

- [ ] **Step 8: `noticias.html`**

```text
<title>Notícias | NUGECID — ITEP-RN</title>
→ <title>Notícias | NUGECID — Polícia Científica do RN</title>

content="Notícias do Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória do ITEP-RN."
→ content="Notícias do Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória da Polícia Científica do RN."

content="Notícias | NUGECID — ITEP-RN"
→ content="Notícias | NUGECID — Polícia Científica do RN"

content="Publicações e novidades do NUGECID/ITEP-RN."
→ content="Publicações e novidades do NUGECID."

<a href="noticia-lancamento-livro.html">ITEP-RN lança livro sobre a trajetória da perícia criminal</a>
→ <a href="noticia-lancamento-livro.html">Polícia Científica do RN lança livro sobre a trajetória da perícia criminal</a>
```

- [ ] **Step 9: `noticia-lancamento-livro.html`**

```text
<title>ITEP-RN lança livro sobre a trajetória da perícia criminal | NUGECID</title>
→ <title>Polícia Científica do RN lança livro sobre a trajetória da perícia criminal | NUGECID</title>

content="O livro Do Vestígio à Prova: A Trajetória da Perícia Criminal no Rio Grande do Norte reúne pesquisa da Comissão Permanente de Gestão da Memória do ITEP-RN."
→ content="O livro Do Vestígio à Prova: A Trajetória da Perícia Criminal no Rio Grande do Norte reúne pesquisa da Comissão Permanente de Gestão da Memória (à época, ITEP-RN)."

content="ITEP-RN lança livro sobre a trajetória da perícia criminal"
→ content="Polícia Científica do RN lança livro sobre a trajetória da perícia criminal"

content="Pesquisa da CPGM resgata a memória institucional do ITEP-RN."
→ content="Pesquisa da CPGM resgata a memória institucional da Polícia Científica do RN."

<h1>ITEP-RN lança livro sobre a trajetória da perícia criminal</h1>
→ <h1>Polícia Científica do RN lança livro sobre a trajetória da perícia criminal</h1>

<p>O Instituto Técnico-Científico de Perícia do Rio Grande do Norte publicou o livro
→ <p>A Polícia Científica do Rio Grande do Norte publicou o livro
```

E no fim do último parágrafo do post (o que termina em "repositório institucional em
implantação."), acrescentar a frase:

```text
 O livro foi publicado em 2024, quando o órgão ainda se chamava ITEP-RN, renomeado
 pela Lei Complementar nº 795, de 8 de outubro de 2025.
```

- [ ] **Step 10: `noticia-sistemas-implantacao.html`**

```text
content="Repositório em DSpace e revista em OJS ampliam o acesso à informação do ITEP-RN."
→ content="Repositório em DSpace e revista em OJS ampliam o acesso à informação da Polícia Científica do RN."

implantação de dois sistemas que ampliam o acesso à informação do ITEP-RN: o repositório
→ implantação de dois sistemas que ampliam o acesso à informação da Polícia Científica
do RN: o repositório
```

- [ ] **Step 11: `assets/css/site.css`**

O estado ativo do menu deve valer para `aria-current="page"` (páginas) e
`aria-current="true"` (posts). Substituir:

```css
.site-nav a[aria-current="page"] { background: var(--kraft); color: var(--ink); }
```

por:

```css
.site-nav a[aria-current] { background: var(--kraft); color: var(--ink); }
```

- [ ] **Step 12: Verificar**

Run: `python3 check.py`
Expected: `OK: 8 paginas, 0 erro(s)`.

Run: `grep -rn "ITEP" *.html | grep -v "à época" | grep -v "renomeado pela" | grep -v "renomeado" | grep -v "Lei Complementar"` (ou inspeção manual)
Expected: nenhuma ocorrência de ITEP fora das notas históricas.

- [ ] **Step 13: Commit**

```bash
git add index.html sgc.html ojs.html dspace.html sobre.html noticias.html \
  noticia-lancamento-livro.html noticia-sistemas-implantacao.html assets/css/site.css
git commit -m "feat: adota nome Policia Cientifica do RN (LC 795/2025) e fixa aria-current"
```

---

### Task 12: Contato oficial e prints dos sistemas

**Files:**
- Modify: `index.html`, `sgc.html`, `ojs.html`, `dspace.html`, `noticias.html`,
  `noticia-lancamento-livro.html`, `noticia-sistemas-implantacao.html`, `sobre.html`
- Modify: `assets/css/site.css`
- Assets já presentes: `assets/img/sgc-dashboard.webp` (1280x651),
  `assets/img/sgc-desarquivamentos.webp` (1280x651), `assets/img/ojs-home.webp` (1280x647),
  `assets/img/dspace-home.webp` (1280x800), `assets/img/dspace-comunidades.webp` (1280x800),
  `assets/img/dspace-item.webp` (1280x800)

- [ ] **Step 1: Rodapé com contato (7 páginas: index, sgc, ojs, dspace, noticias e os 2 posts)**

Substituir:

```html
    <p>Contato: CONTATO_A_DEFINIR · <a href="sobre.html">Sobre e contato</a></p>
```

por:

```html
    <p>Contato: <a href="mailto:arquivogeral@pci.rn.gov.br">arquivogeral@pci.rn.gov.br</a> ·
    <a href="tel:+558432326928">(84) 3232-6928</a> ·
    <a href="sobre.html">Sobre e contato</a></p>
```

E remover a linha de comentário, quando existir (index, sgc, ojs, dspace):

```html
    <!-- CONFIRMAR: e-mail e telefone oficiais -->
```

- [ ] **Step 2: `sobre.html` — seção Contato e rodapé**

Substituir:

```html
      <!-- CONFIRMAR: e-mail, telefone, endereco e horario oficiais -->
      <p>E-mail: CONTATO_A_DEFINIR<br>
      Telefone: CONTATO_A_DEFINIR<br>
      Endereço: CONTATO_A_DEFINIR</p>
```

por:

```html
      <!-- CONFIRMAR: endereco e horario oficiais -->
      <p>E-mail: <a href="mailto:arquivogeral@pci.rn.gov.br">arquivogeral@pci.rn.gov.br</a><br>
      Telefone: <a href="tel:+558432326928">(84) 3232-6928</a><br>
      Endereço: CONTATO_A_DEFINIR</p>
```

E no rodapé do `sobre.html`, substituir:

```html
    <p>Contato: CONTATO_A_DEFINIR</p>
```

por:

```html
    <p>Contato: <a href="mailto:arquivogeral@pci.rn.gov.br">arquivogeral@pci.rn.gov.br</a> ·
    <a href="tel:+558432326928">(84) 3232-6928</a></p>
```

- [ ] **Step 3: `assets/css/site.css` — estilo dos prints**

Adicionar após o bloco `/* Ficha catalografica */` (antes de `/* Carimbo */`):

```css
/* Prints dos sistemas */
.print { margin: 0 0 1.5rem; }
.print img { border: 1px solid var(--kraft); border-radius: var(--radius); }
.print figcaption {
  margin-top: 0.5rem;
  font: 400 0.8rem/1.4 "IBM Plex Mono", monospace;
  color: var(--archive);
}
```

- [ ] **Step 4: `sgc.html` — substituir o placeholder pelos prints**

Substituir:

```html
      <!-- CONFIRMAR: substituir por prints reais (assets/img/sgc-*.webp), com width, height, alt e loading="lazy" -->
      <p>Imagens do sistema serão publicadas aqui após revisão institucional.</p>
```

por:

```html
      <div class="grid-2">
        <figure class="print">
          <img src="assets/img/sgc-dashboard.webp" width="1280" height="651" loading="lazy"
            alt="Dashboard do SGC com cartões de indicadores e gráficos de desarquivamentos">
          <figcaption>Dashboard com estatísticas operacionais</figcaption>
        </figure>
        <figure class="print">
          <img src="assets/img/sgc-desarquivamentos.webp" width="1280" height="651" loading="lazy"
            alt="Tela de desarquivamentos do SGC com lista de processos e filtros">
          <figcaption>Gestão de desarquivamentos</figcaption>
        </figure>
      </div>
```

- [ ] **Step 5: `ojs.html` — print da página inicial**

Substituir:

```html
        <li>Acesso aberto ao conteúdo publicado.</li>
      </ul>
```

por:

```html
        <li>Acesso aberto ao conteúdo publicado.</li>
      </ul>
      <figure class="print">
        <img src="assets/img/ojs-home.webp" width="1280" height="647" loading="lazy"
          alt="Página inicial da Revista da Polícia Científica do RN no Open Journal Systems">
        <figcaption>Página inicial da revista</figcaption>
      </figure>
```

- [ ] **Step 6: `dspace.html` — prints do repositório**

Substituir:

```html
      <p>O material é organizado em comunidades e coleções, com metadados padronizados que
      facilitam a busca e a citação.</p>
```

por:

```html
      <p>O material é organizado em comunidades e coleções, com metadados padronizados que
      facilitam a busca e a citação.</p>
      <div class="grid-2">
        <figure class="print">
          <img src="assets/img/dspace-home.webp" width="1280" height="800" loading="lazy"
            alt="Página inicial do Repositório Institucional com busca e últimas publicações">
          <figcaption>Página inicial do repositório</figcaption>
        </figure>
        <figure class="print">
          <img src="assets/img/dspace-comunidades.webp" width="1280" height="800" loading="lazy"
            alt="Lista de comunidades do repositório institucional">
          <figcaption>Comunidades do acervo</figcaption>
        </figure>
        <figure class="print">
          <img src="assets/img/dspace-item.webp" width="1280" height="800" loading="lazy"
            alt="Página de um documento no repositório, com metadados e arquivo para download">
          <figcaption>Página de um documento depositado</figcaption>
        </figure>
      </div>
```

- [ ] **Step 7: Verificar**

Run: `python3 check.py`
Expected: `OK: 8 paginas, 0 erro(s)`.

- [ ] **Step 8: Commit**

```bash
git add index.html sgc.html ojs.html dspace.html sobre.html noticias.html \
  noticia-lancamento-livro.html noticia-sistemas-implantacao.html \
  assets/css/site.css assets/img
git commit -m "feat: contato oficial e prints dos sistemas"
```

---

### Task 13: Home com capa do livro + SGC detalhado com 6 prints

**Files:**
- Modify: `index.html`, `sgc.html`, `assets/css/site.css`
- Add: `assets/img/sgc-custodia-etiquetas.webp` (1280x653), `assets/img/sgc-relatorios.webp`
  (1280x653), `assets/img/sgc-arquivo-prateleiras.webp` (1280x653), `assets/img/sgc-usuarios.webp`
  (1280x653), `assets/img/livro-capa.webp` (700x1154)
  (já convertidos no diretório; os existentes `sgc-dashboard.webp` e `sgc-desarquivamentos.webp`
  foram regerados em 1280x653)

- [ ] **Step 1: `assets/css/site.css` — grid do livro**

Adicionar após o bloco `/* Prints dos sistemas */`:

```css
/* Livro em destaque */
.livro { display: grid; gap: 1.5rem; }
.livro-capa { margin-bottom: 0; }
@media (min-width: 760px) {
  .livro { grid-template-columns: 260px 1fr; align-items: start; }
}
```

- [ ] **Step 2: `index.html` — capa na seção do livro**

Substituir:

```html
  <section class="section section--alt">
    <div class="wrap">
      <span class="kicker">Publicação institucional</span>
      <h2>Do Vestígio à Prova</h2>
```

por:

```html
  <section class="section section--alt">
    <div class="wrap livro">
      <figure class="print livro-capa">
        <img src="assets/img/livro-capa.webp" width="700" height="1154" loading="lazy"
          alt="Capa do livro Do Vestígio à Prova: A Trajetória da Perícia Criminal no Rio Grande do Norte">
      </figure>
      <div>
      <span class="kicker">Publicação institucional</span>
      <h2>Do Vestígio à Prova</h2>
```

E, no fim da mesma seção, substituir:

```html
      <div class="actions">
        <a class="btn" href="noticia-lancamento-livro.html">Sobre a publicação</a>
      </div>
    </div>
  </section>
```

por:

```html
      <div class="actions">
        <a class="btn" href="noticia-lancamento-livro.html">Sobre a publicação</a>
      </div>
      </div>
    </div>
  </section>
```

- [ ] **Step 3: `sgc.html` — funcionalidades detalhadas**

Substituir o bloco de lista atual:

```html
      <h2>O que o sistema faz</h2>
      <ul>
        <li>Gestão de desarquivamentos, anexos, termos e relatórios.</li>
        <li>Dashboard com estatísticas operacionais.</li>
        <li>Kanban de tarefas, projetos, checklists e comentários.</li>
        <li>Gestão de usuários, perfis de acesso e auditoria.</li>
        <li>Backup, restauração e verificações de saúde da aplicação.</li>
        <li>Notificações, busca unificada e integrações de apoio.</li>
      </ul>
```

por:

```html
      <h2>O que o sistema faz</h2>
      <ul>
        <li><strong>Desarquivamentos</strong> — cadastro, acompanhamento, importação em lote
        (XLSX/CSV), exportação, emissão de termos em PDF/DOCX, comentários, anexos, lixeira e
        códigos de barras.</li>
        <li><strong>Dashboard operacional</strong> — estatísticas em tempo real, gráficos e
        relatórios mensais em PDF.</li>
        <li><strong>Tarefas e projetos (Kanban)</strong> — colunas com limite de trabalho em
        andamento, prioridades, prazos, tags, checklists, subtarefas e comentários.</li>
        <li><strong>Vestígios e custódia</strong> — catalogação, busca por código SCV e
        estatísticas.</li>
        <li><strong>Arquivos e pastas</strong> — upload, download, visualização de imagens e
        organização com tags.</li>
        <li><strong>Planilhas de controle</strong> — upload e download das planilhas de
        desarquivamento.</li>
        <li><strong>Usuários e perfis</strong> — quatro níveis de acesso, preferências, avatar e
        bloqueio automático.</li>
        <li><strong>Notificações</strong> — no sistema, push no navegador e preferências por
        canal e tipo.</li>
        <li><strong>Busca unificada</strong> — busca em texto completo em todo o acervo do
        sistema.</li>
        <li><strong>Auditoria e backup</strong> — trilha de auditoria das ações e rotina de
        backup do banco de dados.</li>
      </ul>
```

- [ ] **Step 4: `sgc.html` — nova seção de integrações**

Inserir antes de `<h2>Telas do sistema</h2>` uma seção própria (a seção de Telas passa de
`section--alt` para `section`, mantendo a alternância de fundos):

```html
  <section class="section section--alt">
    <div class="wrap prose">
      <h2>Integrações e recursos</h2>
      <ul>
        <li><strong>SEI</strong> — captura de processos do sistema eletrônico de informações.</li>
        <li><strong>Escavador SEIRN</strong> — recebimento de publicações por webhook.</li>
        <li><strong>Metabase</strong> — painéis de business intelligence.</li>
        <li><strong>OCR</strong> — reconhecimento de texto em documentos digitalizados.</li>
      </ul>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <h2>Telas do sistema</h2>
```

A seção que hoje contém "Telas do sistema" deve terminar logo após o `</ul>` das
integrações, e a seção de telas começa em `<section class="section">`.

- [ ] **Step 5: `sgc.html` — seis prints**

Substituir o `grid-2` atual (com 2 figures) por:

```html
      <div class="grid-2">
        <figure class="print">
          <img src="assets/img/sgc-dashboard.webp" width="1280" height="653" loading="lazy"
            alt="Dashboard do SGC com cartões de indicadores e gráficos de desarquivamentos">
          <figcaption>Dashboard com estatísticas operacionais</figcaption>
        </figure>
        <figure class="print">
          <img src="assets/img/sgc-desarquivamentos.webp" width="1280" height="653" loading="lazy"
            alt="Tela de desarquivamentos do SGC com lista de processos e filtros">
          <figcaption>Gestão de desarquivamentos</figcaption>
        </figure>
        <figure class="print">
          <img src="assets/img/sgc-custodia-etiquetas.webp" width="1280" height="653" loading="lazy"
            alt="Tela de custódia de vestígios com geração de etiquetas">
          <figcaption>Custódia de vestígios e etiquetas</figcaption>
        </figure>
        <figure class="print">
          <img src="assets/img/sgc-relatorios.webp" width="1280" height="653" loading="lazy"
            alt="Tela de relatórios do SGC com filtros e exportação">
          <figcaption>Relatórios operacionais</figcaption>
        </figure>
        <figure class="print">
          <img src="assets/img/sgc-arquivo-prateleiras.webp" width="1280" height="653" loading="lazy"
            alt="Tela do arquivo com organização das prateleiras e caixas">
          <figcaption>Organização do arquivo</figcaption>
        </figure>
        <figure class="print">
          <img src="assets/img/sgc-usuarios.webp" width="1280" height="653" loading="lazy"
            alt="Tela de gestão de usuários com perfis de acesso">
          <figcaption>Usuários e perfis de acesso</figcaption>
        </figure>
      </div>
```

- [ ] **Step 6: Verificar**

Run: `python3 check.py`
Expected: `OK: 8 paginas, 0 erro(s)`.

- [ ] **Step 7: Commit**

```bash
git add index.html sgc.html assets/css/site.css assets/img
git commit -m "feat: capa do livro na home e pagina do SGC detalhada com 6 prints"
```

---

### Task 14: OJS e DSpace detalhados com mais prints

**Files:**
- Modify: `ojs.html`, `dspace.html`
- Add: `assets/img/ojs-logo.webp` (900x149), `assets/img/dspace-comunidade-nugecid.webp`
  (1280x800), `assets/img/dspace-colecao.webp` (1280x800), `assets/img/dspace-busca.webp`
  (1280x800)

- [ ] **Step 1: `ojs.html` — logo e escopo da revista**

Substituir:

```html
      <h2>Sobre a revista</h2>
      <p>A RPCIRN reúne produção científica nas áreas de criminalística, medicina legal,
      identificação civil e temas afins da perícia oficial, aproximando o conhecimento técnico
      produzido no estado da comunidade acadêmica e da sociedade.</p>
```

por:

```html
      <h2>Sobre a revista</h2>
      <figure class="print">
        <img src="assets/img/ojs-logo.webp" width="900" height="149" loading="lazy"
          alt="Logotipo da Revista da Polícia Científica do Rio Grande do Norte">
      </figure>
      <p>A RPCIRN reúne produção científica nas áreas de criminalística, medicina legal,
      identificação civil e criminal e temas afins da perícia oficial, aproximando o
      conhecimento técnico produzido no estado da comunidade acadêmica e da sociedade.</p>
      <p>O periódico adota o fluxo editorial completo do Open Journal Systems: submissão
      online, avaliação por pares, editoração e publicação em acesso aberto.</p>
```

- [ ] **Step 2: `ojs.html` — nova seção "Como submeter"**

Substituir:

```html
  <section class="section">
    <div class="wrap">
      <h2>Como submeter</h2>
```

por (a seção usa `prose` para listas e largura de linha consistentes):

```html
  <section class="section">
    <div class="wrap prose">
      <h2>Como submeter</h2>
```

Se a seção ainda não existir, inserir antes de `<h2>Acesso</h2>`:

```html
      <h2>Como submeter</h2>
      <ol>
        <li>Criar cadastro no sistema, como autor.</li>
        <li>Enviar o manuscrito e preencher os metadados: autoria, resumo e palavras-chave.</li>
        <li>Acompanhar a avaliação por pares pelo painel do autor.</li>
        <li>Após aprovação, o artigo entra na edição em preparação.</li>
      </ol>
      <!-- CONFIRMAR: diretrizes para autores, secoes e periodicidade com a equipe editorial -->
```

- [ ] **Step 2b: `assets/css/site.css` — listas ordenadas**

Substituir:

```css
.prose ul { padding-left: 1.2rem; max-width: 72ch; }
```

por:

```css
.prose ul, .prose ol { padding-left: 1.2rem; max-width: 72ch; }
```

- [ ] **Step 2c: `dspace.html` — remover comentário obsoleto**

Remover a linha (os nomes de comunidades e coleções já foram confirmados no repositório):

```html
      <!-- CONFIRMAR: nomes das comunidades e colecoes com a equipe do NUGECID -->
```

- [ ] **Step 3: `dspace.html` — o que o repositório reúne, detalhado**

Substituir:

```html
      <h2>O que o repositório reúne</h2>
      <ul>
        <li>Portarias e atos normativos da Polícia Científica do RN.</li>
        <li>Publicações institucionais, como o livro <em>Do Vestígio à Prova</em>.</li>
        <li>Documentos e fotografias do acervo de memória institucional.</li>
        <li>Produção técnica e científica da perícia oficial.</li>
      </ul>
```

por:

```html
      <h2>O que o repositório reúne</h2>
      <ul>
        <li>Portarias, leis e demais atos normativos da Polícia Científica do RN.</li>
        <li>Notas técnicas, relatórios, manuais e procedimentos operacionais.</li>
        <li>Publicações institucionais, como o livro <em>Do Vestígio à Prova</em>.</li>
        <li>Documentos e fotografias do acervo de memória institucional.</li>
        <li>Produção técnica e científica da perícia oficial.</li>
      </ul>
      <p>Cada documento recebe metadados padronizados (Dublin Core) e identificador persistente
      (handle), o que garante busca precisa, citação estável e preservação digital de longo
      prazo.</p>
```

- [ ] **Step 4: `dspace.html` — nova seção "Comunidades"**

Inserir antes de `<h2>Como depositar</h2>`:

```html
      <h2>Comunidades</h2>
      <p>O acervo é organizado em cinco comunidades, espelhando a estrutura do órgão:</p>
      <ul>
        <li><strong>Gestão Estratégica e Administrativa (DG)</strong> — documentos da Direção
        Geral e da gestão institucional.</li>
        <li><strong>Instituto de Criminalística (IC)</strong> — procedimentos, guias e relatórios.</li>
        <li><strong>Instituto de Identificação (II)</strong> — procedimentos e diretrizes.</li>
        <li><strong>Instituto de Medicina Legal (IML)</strong> — procedimentos, protocolos e notas
        técnicas.</li>
        <li><strong>NUGECID</strong> — memória institucional, publicações e acervo do Núcleo.</li>
      </ul>
      <p>Dentro das comunidades, as coleções reúnem tipos específicos de documento, como
      portarias, notas técnicas, relatórios e manuais.</p>
```

- [ ] **Step 5: `dspace.html` — fluxo de depósito**

Substituir:

```html
      <h2>Como depositar</h2>
      <p>Servidores e setores da Polícia Científica do RN podem encaminhar documentos e acervos ao NUGECID para
      avaliação e depósito no repositório. A equipe do Núcleo orienta sobre formatos, metadados
      e direitos de publicação.</p>
```

por:

```html
      <h2>Como depositar</h2>
      <ol>
        <li>O setor encaminha o documento ou acervo ao NUGECID.</li>
        <li>A equipe avalia o material e define a comunidade e a coleção de destino.</li>
        <li>Os metadados são descritos conforme o padrão Dublin Core.</li>
        <li>O documento é depositado e recebe um identificador persistente (handle).</li>
        <li>O item fica disponível para consulta pública no repositório.</li>
      </ol>
```

- [ ] **Step 6: `dspace.html` — seis prints**

Substituir o `grid-2` atual (3 figures) por:

```html
      <div class="grid-2">
        <figure class="print">
          <img src="assets/img/dspace-home.webp" width="1280" height="800" loading="lazy"
            alt="Página inicial do Repositório Institucional com busca e últimas publicações">
          <figcaption>Página inicial do repositório</figcaption>
        </figure>
        <figure class="print">
          <img src="assets/img/dspace-comunidades.webp" width="1280" height="800" loading="lazy"
            alt="Lista das cinco comunidades do repositório institucional">
          <figcaption>Comunidades do acervo</figcaption>
        </figure>
        <figure class="print">
          <img src="assets/img/dspace-comunidade-nugecid.webp" width="1280" height="800" loading="lazy"
            alt="Página da comunidade do NUGECID no repositório">
          <figcaption>Comunidade do NUGECID</figcaption>
        </figure>
        <figure class="print">
          <img src="assets/img/dspace-colecao.webp" width="1280" height="800" loading="lazy"
            alt="Página de uma coleção do repositório, com a lista de documentos">
          <figcaption>Coleção de documentos</figcaption>
        </figure>
        <figure class="print">
          <img src="assets/img/dspace-busca.webp" width="1280" height="800" loading="lazy"
            alt="Resultados de busca no repositório institucional">
          <figcaption>Busca no acervo</figcaption>
        </figure>
        <figure class="print">
          <img src="assets/img/dspace-item.webp" width="1280" height="800" loading="lazy"
            alt="Página de um documento no repositório, com metadados e arquivo para download">
          <figcaption>Página de um documento depositado</figcaption>
        </figure>
      </div>
```

- [ ] **Step 7: Verificar**

Run: `python3 check.py`
Expected: `OK: 8 paginas, 0 erro(s)`.

- [ ] **Step 8: Commit**

```bash
git add ojs.html dspace.html assets/img
git commit -m "feat: paginas do OJS e do DSpace detalhadas com mais prints"
```

---

## Pendências que não bloqueiam a implementação

Conteúdo provisório marcado com `<!-- CONFIRMAR -->`: contato oficial, datas das notícias,
título do hero, nomes da equipe, prints dos sistemas, seções/ISSN da revista, comunidades do
repositório e logo do órgão (ainda não usado no layout — o header usa texto).

