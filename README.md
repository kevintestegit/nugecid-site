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
- `sistemas.html` — visão geral das plataformas e seus estados de implantação.
- `assets/fonts/` — fontes locais e respectivas licenças SIL OFL.
- `DESIGN.md` — identidade visual e mapeamento para os tokens do CSS.
- `tests/` — regressões de conteúdo, links e validação no navegador.
- `docs/superpowers/` — spec e plano de implementação.

## Design system

Identidade editorial: arquivo científico, perícia criminal e memória documental. O mockup
fornecido em 08/10/2026 orienta o papel marfim, os títulos serifados, os cartões de borda
fina e a faixa azul profunda. A imagem de ambientação combina registros abertos,
pastas e livros em luz quente; máscaras de composição preservam a leitura dos textos.
Sem glassmorphism ou estética de dashboard SaaS.

Tokens ficam no `:root` do `site.css`:

| Token | Uso |
| --- | --- |
| `--paper` / `--paper-2` / `--paper-3` | Marfim do papel, folha mais clara, tom alternado de seção |
| `--rule` / `--rule-2` | Fios e divisores |
| `--ink` / `--ink-2` | Texto corrido e texto secundário |
| `--navy` / `--navy-2` / `--on-navy` | Cabeçalho, rodapé, links |
| `--gold` / `--gold-2` / `--gold-3` | Botão principal, destaques e item ativo |
| `--stamp` / `--green` | Carimbo de status |
| `--serif` / `--sans` / `--mono` | Newsreader (títulos) · Archivo (interface e metadados) |

`--paper` é igual à cor de fundo das gravuras, então as ilustrações encostam no papel sem
costura visível.

Componentes compartilhados: `menu` (desktop inline / mobile em
`<details>`, sem JS), `pagehead` (banner + título), `hero`, `plate` (ilustração emoldurada
com legenda), `btn`, `ficha`, `keylist`, `steps`, `data-table`, `news-card`, `notice`,
`divider`, `site-footer`.

Foco visível com contorno de 2px, claro no azul-marinho e escuro no cabeçalho de papel.
A auditoria automática WCAG A/AA das nove páginas em desktop e mobile não encontrou
violações; isso não substitui uma avaliação manual completa de acessibilidade.

## Assets visuais

`arquivo-editorial.webp` é uma ilustração gerada de ambientação editorial, inspirada
no mockup; não é fotografia do acervo da instituição. A capa verdadeira em
`livro-capa.webp` e o brasão oficial foram preservados sem alteração.

As gravuras já existentes vêm de `NU_GECID_assets_mockup.zip`. Os arquivos entregues eram folhas de contato
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
python3 -m unittest discover -s tests -v
```

Exit code 0 = tudo certo. Verifica: links internos existem, cada página tem `lang="pt-BR"`,
`<title>`, um `<h1>` e `meta description`, e toda `<img>` tem `alt` e `loading="lazy"`.

Para servir localmente: `python3 -m http.server 8000` na raiz do repositório.
O site não precisa de build, Node ou instalação de dependências.

Para reproduzir as capturas e as verificações de navegador, com Playwright e Chromium instalados:

```bash
python3 tests/browser_smoke.py --output /tmp/nugecid-review
```

O teste verifica nove páginas em cinco larguras, imagens, fontes, navegação por teclado,
disclosures e ausência de rolagem horizontal. Para incluir axe-core, passe `--axe`
com o caminho do script de auditoria; sem essa opção, a auditoria axe não é executada.
Veja `docs/visual-review.md` para a comparação com o mockup e os resultados.

## Publicação

GitHub Pages, branch `main`, raiz do repositório. Sem build e sem Actions.

1. Criar o repositório `nugecid-site` na conta `kevintestegit`.
2. `git remote add origin git@github.com:kevintestegit/nugecid-site.git`
3. `git push -u origin main`
4. Settings → Pages → Source: "Deploy from a branch" → Branch: `main` / `/ (root)`.

## Pendências de conteúdo

Itens marcados com `<!-- CONFIRMAR: ... -->` no HTML: contato oficial, datas das notícias,
título do hero, prints dos sistemas e textos institucionais revisados.
