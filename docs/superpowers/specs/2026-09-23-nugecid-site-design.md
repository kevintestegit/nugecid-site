# Site NUGECID — Design

Data: 2026-09-23
Status: aprovado (brainstorming) — pronto para plano de implementação

## Contexto

O NUGECID (Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória) do
ITEP-RN (Instituto Técnico-Científico de Perícia do Rio Grande do Norte) precisa de um
site institucional público que também sirva de vitrine dos seus três sistemas:

- **SGC** — Sistema de Gestão de Documentos e Desarquivamentos (uso interno, PCIRN).
- **OJS** — Revista da Polícia Científica do Rio Grande do Norte (RPCIRN), periódico
  científico mantido pelo Núcleo.
- **DSpace** — repositório digital institucional (portarias, acervo, publicações).

Fatos de referência (fontes: livro institucional *Do Vestígio à Prova*, 2024, ISBN
978-65-01-06618-9; README dos repositórios):

- NUGECID criado pela Portaria nº 127, de 29/03/2023, vinculado à Diretoria Geral do ITEP-RN.
- Atribuições: gestão documental, gestão da informação e do conhecimento, memória institucional.
- Estruturas que o Núcleo gere: Setor de Arquivo Geral (SAG, Portaria 588/2022),
  Comitê Permanente de Avaliação e Gestão Documental (CPAGED, Portaria 177/2023),
  Comissão Permanente de Gestão da Memória (CPGM, Portaria 126/2023).
- Projetos: repositório digital institucional (DSpace), periódico científico (OJS/RPCIRN),
  biblioteca especializada, livro *Do Vestígio à Prova* (v. 1, 2024).

## Objetivo e público

Site institucional + vitrine de sistemas. Público: gestão pública, comunidade acadêmica,
parceiros institucionais e servidores do ITEP-RN.

Sucesso = visitante entende em uma página o que o NUGECID faz, conhece os três sistemas e
acha o contato. Site leve, acessível e sem manutenção de infraestrutura.

## Escopo

### Páginas (arquivos na raiz, sem subpastas)

| Arquivo | Conteúdo |
| --- | --- |
| `index.html` | Hero institucional → o que o NUGECID faz (gestão documental · memória · repositório · periódico) → fichas dos 3 sistemas → faixa do livro → últimas notícias → rodapé |
| `sgc.html` | O que é, para quem (interno PCIRN), módulos (desarquivamentos, anexos, termos, dashboard, kanban, auditoria, usuários, backup), tabela de stack, prints, selo "uso interno" |
| `ojs.html` | Sobre a RPCIRN, seções, como submeter, equipe editorial, selo "em implantação" + slot único de URL |
| `dspace.html` | Sobre o repositório, o que deposita, comunidades, selo + slot de URL |
| `sobre.html` | Portaria 127/2023, atribuições, equipe, contato |
| `noticias.html` | Lista por data |
| `noticia-<slug>.html` | Posts estáticos (iniciais: lançamento do livro; sistemas em implantação) |
| `assets/css/site.css` | Único CSS do site |
| `assets/img/` | Logos, prints, capa do livro |
| `check.py` | Verificação de links internos e atributos obrigatórios (Python stdlib) |

Raiz plana: a mesma navegação relativa funciona em todas as páginas, sem `../`.

### Fora de escopo

- URLs públicas de OJS/DSpace (não existem ainda; deixar slot único por página para ligar depois).
- SGC público (é interno; sem link de acesso).
- VLibras, blog com CMS, busca interna, i18n, dark mode.

## Identidade visual — direção B "Dossiê manila"

Escolhida em mockup no companion visual (3 refinamentos apresentados; B aprovado).

### Tokens

| Token | Valor | Uso |
| --- | --- | --- |
| `--paper` | `#ece3cf` | fundo base (manila) |
| `--paper-light` | `#f4ecdb` | fichas, cartões |
| `--kraft` | `#d9c9a3` | bordas, faixas, hover |
| `--ink` | `#2a2620` | texto, header, footer |
| `--ink-soft` | `#5c5648` | texto secundário |
| `--archive` | `#6f6a5e` | metadados, labels |
| `--stamp` | `#a33127` | carimbo, links, destaque |

Contraste mínimo AA em todas as combinações texto/fundo.

### Tipografia

- **Archivo** (400/600/700) — display, títulos e corpo. Títulos com peso 700 e tracking levemente negativo.
- **IBM Plex Mono** (400/600) — metadados, selos, fichas, labels.
- Escala: h1 `clamp(2rem, 5vw, 3rem)`, h2 `1.6rem`, h3 `1.2rem`, corpo `1rem/1.6`, mono `0.8rem`.
- Largura de linha ≤ 72ch. Google Fonts via `<link>`; self-host é opção futura (LGPD).

### Elementos-assinatura

- **Carimbo**: selo rotacionado `-3deg`, borda 2px, mono uppercase com tracking — marca status
  ("USO INTERNO", "EM IMPLANTAÇÃO", "ACERVO DIGITAL"). É o elemento memorável; resto fica quieto.
- **Ficha catalográfica**: bloco com linhas pontilhadas, chave em mono (`Sistema`, `Stack`, `Situação`).
  Usado para apresentar os sistemas.
- **Header/footer institucionais** em `--ink` com texto em `--paper`.
- Sem gradientes, sem sombras difusas, sem cards arredondados genéricos. Raio máximo 3px.

### Motion

- Mínimo e discreto: hover/focus em links e botões com `ease-out` custom
  (`cubic-bezier(0.23, 1, 0.32, 1)`), 150–200ms.
- `:active` com `transform: scale(0.97)` em botões.
- Hover só sob `@media (hover: hover) and (pointer: fine)`.
- `prefers-reduced-motion: reduce` remove movimento.
- Proibido: fade-in por seção, stagger decorativo, animação em ação de teclado.

## Estrutura técnica

- HTML5 semântico (`header`, `nav`, `main`, `section`, `footer`), um `<h1>` por página.
- **Zero JavaScript.** Nav com `flex-wrap` (sem hamburger, sem checkbox hack).
- CSS único com custom properties; mobile-first; breakpoints em 640px e 960px.
- Imagens WebP com `width`/`height`, `loading="lazy"` e `alt` descritivo.
- Meta: `lang="pt-BR"`, `<title>` único por página, `meta description`, Open Graph básico.
- Canonical/OG apontando para `https://kevintestegit.github.io/nugecid-site/`.

### Deploy

- Repositório `kevintestegit/nugecid-site`, branch `main`.
- GitHub Pages servindo da raiz da branch (Settings → Pages → Deploy from branch). Sem Actions.
- `.nojekyll` na raiz.
- `.gitignore` com `.superpowers/`.
- Slot de URL de OJS/DSpace: o CTA fica como "em breve" (sem link) e um comentário HTML
  único marca o ponto de troca, para virar link em uma linha quando a URL existir.

### Verificação (`check.py`)

Script Python (stdlib apenas) que:

1. Varre os `.html` da raiz e valida que todo `href`/`src` relativo (ignorando âncoras
   `#` e URLs externas) existe no disco.
2. Confirma que cada página tem `lang`, `<title>`, um `<h1>` e `meta description`.
3. Confirma que toda `<img>` tem `alt` e `loading="lazy"`.

Roda local (`python3 check.py`) antes de cada push. Falha = exit code 1.

## Conteúdo: pendências do cliente

- Logo/brasão do ITEP-RN em SVG ou PNG de alta resolução.
- Prints das telas do SGC, OJS e DSpace (ou autorização para capturar localmente).
- Textos institucionais prontos (missão, histórico) para incorporar/revisar.
- E-mail e telefone oficiais de contato.
- Confirmação do título do hero da home ("memória, informação e conhecimento do ITEP-RN"
  é proposta, não texto oficial).

Sem esses itens o site é construído com placeholders claramente marcados e substituíveis.

## Decisões adiadas

- Domínio próprio (paths relativos funcionam quando existir).
- VLibras e self-host de fontes.
- URLs públicas de OJS/DSpace.
