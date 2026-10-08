---
version: alpha
colors:
  primary: "#031c2b"
  paper: "#f7f2e9"
  surface: "#fcf8f0"
  paperAlt: "#eee6d8"
  ink: "#071f34"
  inkSecondary: "#41515d"
  navy: "#031c2b"
  border: "#d8ccba"
typography:
  display:
    fontFamily: "Newsreader, Georgia, serif"
  body:
    fontFamily: "Archivo, system-ui, sans-serif"
  metadata:
    fontFamily: "IBM Plex Mono, monospace"
rounded:
  card: "5px"
  button: "4px"
omitted:
  - section: spacing
    reason: "Responsive geometry is owned by assets/css/site.css, with named component rules."
  - section: components
    reason: "This static content site has no component framework; shared HTML classes are documented below."
---

## Overview

Site público institucional em português brasileiro, para servidores, pesquisadores e sociedade.
Referência: mockup editorial fornecido pelo usuário em 08/10/2026, com papel claro,
livros e pastas de arquivo em luz quente e faixa azul profunda. O Arquivo Geral faz parte
das atribuições do NUGECID. A assinatura visual é a passagem do documento em papel à memória
institucional: abertura clara, registro aberto e faixa escura de conhecimento.

Esta direção substitui a composição em gravuras da versão anterior. Não altera normas,
nomes oficiais, contatos, estados de implantação ou informações históricas.

## Colors

Fonte canônica de implementação: `:root` em `assets/css/site.css`.
O frontmatter documenta a mesma paleta: paper → --paper; surface → --paper-2;
paperAlt → --paper-3; ink → --ink; inkSecondary → --ink-2; navy → --navy;
border → --rule; primary → --navy. As classes compartilhadas consomem essas variáveis diretamente.
Verde identifica “Em uso”; âmbar identifica “Em implantação”, sempre com texto explícito.

## Typography

Newsreader para títulos e marca; Archivo para textos e navegação; IBM Plex Mono para
metadados técnicos. Fontes locais licenciadas sob SIL OFL em `assets/fonts/`, com
fallbacks completos. Itálico reservado às frases editoriais e títulos de obras.

## Layout

Conteúdo em largura máxima de 84rem. Home: abertura editorial → atribuições / sistemas /
livro → memória institucional e plataformas → notícias e acesso rápido → rodapé.
No celular, atribuições em duas colunas, sistemas em uma coluna e navegação em disclosure nativo.
Desktop a partir de 70rem usa navegação explícita, independente do disclosure mobile.
Cada página de sistema mantém suas telas reais, recursos e avisos de acesso existentes.

## Elevation & Depth

Papel, bordas finas e profundidade nas imagens de ambientação. Sombra contida somente na capa.
A imagem `arquivo-editorial.webp` é ilustração gerada de ambientação: não é registro do acervo real.
A capa `livro-capa.webp` e o brasão oficial são mantidos byte a byte.

## Shapes

Cartões com raio de 5px; botões com raio de 4px; ícones lineares simples em azul.
Sem botões de busca sem função, notícias fictícias, acesso público inventado ao SGC ou
links de implantação apresentados como serviços já disponíveis.

## Components

`archive-hero`: abertura editorial clara com imagem à direita.
`capability`: resumo e atribuição oficial completa em disclosure.
`system-card`: nome, status, página de detalhes e ficha completa expansível.
`book-feature`: capa verdadeira, informação bibliográfica e link original ao PDF.
`archive-feature`: faixa de memória institucional em azul profundo.
`pagehead`: abertura compartilhada das páginas internas; variante clara para Sobre.
`related-news`: apenas artigos que existem no site.

## Do's and Don'ts

Preservar o conteúdo institucional e os links; não copiar fatos fictícios do mockup.
Manter foco visível, semântica nativa, contraste AA e redução de movimento.
Não transformar imagens geradas em suposta documentação oficial.
Não publicar na branch principal sem aprovação do usuário.
