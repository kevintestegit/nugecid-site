# Site NUGECID

Site institucional e vitrine de sistemas do NUGECID — Núcleo de Gestão do Conhecimento,
Informação, Documentação e Memória do ITEP-RN.

Publicado em: https://kevintestegit.github.io/nugecid-site/

## Estrutura

- Páginas HTML na raiz (`index.html`, `sgc.html`, `ojs.html`, `dspace.html`, `sobre.html`,
  `noticias.html` e posts).
- `assets/css/site.css` — único CSS, o design system completo (tokens → base → tipografia →
  layout → componentes).
- `assets/img/` — brasão oficial, prints reais dos sistemas e as gravuras/ícones do mockup.
- `check.py` — verificação de links internos, metadados e imagens.
- `docs/superpowers/` — spec e plano de implementação.

## Design system

Identidade editorial: arquivo científico, perícia criminal e memória documental. Marfim e
azul-marinho, gravuras em estilo blueprint, bordas finas e muito respiro. Sem gradientes,
glassmorphism nem estética de dashboard SaaS.

Tokens ficam no `:root` do `site.css`:

| Token | Uso |
| --- | --- |
| `--paper` / `--paper-2` / `--paper-3` | Marfim do papel, folha mais clara, tom alternado de seção |
| `--rule` / `--rule-2` | Fios e divisores |
| `--ink` / `--ink-2` | Texto corrido e texto secundário |
| `--navy` / `--navy-2` / `--on-navy` | Cabeçalho, rodapé, links |
| `--stamp` / `--green` | Carimbo de status |
| `--serif` / `--sans` / `--mono` | Newsreader (títulos) · Archivo (interface) · IBM Plex Mono (metadados) |

`--paper` é igual à cor de fundo das gravuras, então as ilustrações encostam no papel sem
costura visível.

Componentes compartilhados: `barra-institucional`, `menu` (desktop inline / mobile em
`<details>`, sem JS), `pagehead` (banner + título), `hero`, `plate` (ilustração emoldurada
com legenda), `btn`, `ficha`, `keylist`, `steps`, `data-table`, `news-list`, `notice`,
`divider`, `site-footer`.

Todas as combinações de cor passam em WCAG AA (mínimo 5,5:1 para texto corrido). Foco visível
com contorno de 2px, claro no azul-marinho e carimbo no papel.

## Assets visuais

As gravuras vêm de `NU_GECID_assets_mockup.zip`. Os arquivos entregues eram folhas de contato
com fundo opaco e vários elementos por imagem, então foram fatiados e convertidos para WebP
(alpha nas bordas, 3× com alpha suavizado nos ícones de ~30px):

- `hero-pericia`, `banner-{sgc,ojs,dspace,sobre,noticias}`, `footer-paisagem`,
  `separador-h` — ilustrações completas, usadas como estão.
- `textura-papel` — tile 3×3 espelhado (sem emenda) a 14% de opacidade no `body`.
- `pattern-azul` — malha de contours a 22% no cabeçalho, 14% no rodapé.
- `icones/*.webp` — 12 ícones de linha extraídos da folha de funcionalidades.
- `ilustracao-*.webp` — elementos de apoio (maleta, lupa, mapa, perito, ponte, documentos,
  placas de prova).

O brasão real do projeto (`brasao-pcirn.webp`) prevalece sobre o logotipo e o carimbo gerados
por IA no mockup — esses dois não foram usados. O selo que aparecia no canto da gravura do
hero foi removido por patch, e a faixa de texto cortada do banner do DSpace foi aparada.

Textos dentro das imagens são só linguagem visual; todo o conteúdo real está em HTML.

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
