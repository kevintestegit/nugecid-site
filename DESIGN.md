---
version: alpha
colors:
  primary: "#101d2b"
  paper: "#f7f2e9"
  surface: "#fcf8f0"
  paperAlt: "#eee6d8"
  ink: "#071f34"
  inkSecondary: "#41515d"
  navy: "#101d2b"
  gold: "#d4b07a"
  border: "#d8ccba"
typography:
  display:
    fontFamily: "Newsreader, Georgia, serif"
  body:
    fontFamily: "Archivo, system-ui, sans-serif"
  metadata:
    fontFamily: "Archivo, system-ui, sans-serif"
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
border → --rule; primary → --navy; gold → --gold. As classes compartilhadas consomem essas variáveis diretamente.
Dourado (`--gold`, `--gold-2`) marca o botão principal e destaques sobre o azul;
`--gold-3` marca o item ativo da navegação e hovers sobre papel (contraste AA).
Verde identifica “Em uso”; âmbar identifica “Em implantação”, sempre com texto explícito.

## Typography

Newsreader para títulos e marca; Archivo para textos, navegação e metadados
(`--mono` aponta para a mesma família). Fontes locais licenciadas sob SIL OFL em `assets/fonts/`, com
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
Gravuras (`plate`) recebem duotone sépia por filtro CSS para harmonizar com o papel.

## Motion

Somente CSS, sem JS, em `site.css` (seções 17 e 18), tudo dentro de
`prefers-reduced-motion: no-preference` e de `@supports` para recursos de linha do tempo.
Sem suporte ou com movimento reduzido, a página fica estática e completa.
- Entrada: hero e `pagehead` sobem em sequência; destaque dourado do título com brilho único.
- Rolagem: cabeçalho fixo que se condensa; revelação de cartões e blocos com `view()`;
  parallax da imagem do hero; barra de progresso de leitura nas notícias.
- Interação: sublinhado dourado da navegação, elevação de cartões, brilho no botão dourado,
  disclosures com altura animada e menu mobile com ícone que vira X.
- Navegação entre páginas: View Transitions entre documentos (`main` desliza e esmaece).

## Shapes

Cartões com raio de 5px; botões com raio de 4px; ícones lineares simples em azul.
Sem botões de busca sem função, notícias fictícias, acesso público inventado ao SGC ou
links de implantação apresentados como serviços já disponíveis.

## Components

`site-header`: faixa marfim com brasão, NUGECID e nome completo; nav Início, Sobre, Sistemas,
Acervo, Notícias e Contato com sublinhado dourado no item ativo. Na home, recorte diagonal sob a marca.
`archive-hero`: abertura azul-marinho com imagem de arquivo, título em caixa alta com destaque dourado.
`capability`: faixa de quatro atribuições com ícone em círculo.
`system-card`: nome, status, link “Conhecer o sistema”, captura de tela (home) e ficha expansível.
`book-feature`: capa verdadeira, informação bibliográfica e link original ao PDF.
`news-mini` / `news-card`: últimas notícias na home e grade de cartões em Notícias.
`pagehead`: faixa azul-marinho das páginas internas, com breadcrumbs embutidos.
`site-footer`: marca, navegação e contatos sobre azul-marinho.
`related-news`: apenas artigos que existem no site.

## Do's and Don'ts

Preservar o conteúdo institucional e os links; não copiar fatos fictícios do mockup.
Manter foco visível, semântica nativa, contraste AA e redução de movimento.
Não transformar imagens geradas em suposta documentação oficial.
Não publicar na branch principal sem aprovação do usuário.
