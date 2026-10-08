# Revisão visual — identidade NUGECID

Referência: mockup anexado à solicitação de 08/10/2026.
Branch: `feat/nova-identidade-nugecid`.

## Comparação com a referência

| Área | Implementação e decisão |
| --- | --- |
| Abertura desktop | Título serifado com trecho em itálico, papel marfim, botões azul e claro, registro aberto à direita. |
| Atribuições | Quatro cartões com ícones lineares; textos oficiais completos disponíveis por “Saiba mais”. |
| Sistemas | Três plataformas, status verde/âmbar e fichas completas; página de visão geral adicionada. |
| Livro | Capa verdadeira mantida byte a byte, ISBN e link original ao PDF preservados. A capa fictícia do mockup não foi usada. |
| Faixa escura | Arquivo iluminado em tons quentes, título “Conhecimento de hoje…” e plataformas em painel lateral. |
| Notícias e atalhos | Cartões com as duas notícias reais existentes, sem copiar notícias ou datas fictícias da referência. |
| Sobre | Abertura clara com imagem à direita e navegação por âncoras para atribuições, estruturas, equipe e contato. |
| Artigo | Conteúdo original, imagem de ambientação identificada como ilustrativa e notícias relacionadas existentes. |
| Mobile | Menu nativo acessível, atribuições em 2 colunas, sistemas e notícias empilhados, capa inteira. |

A reprodução é visual, não uma comparação automática pixel a pixel: o mockup foi
fornecido como imagem composta, sem os arquivos originais de suas cenas.
A ambientação foi gerada a partir da referência e é identificada como ilustração.
O brasão oficial prevalece sobre a marca de impressão digital presente na referência.

## Capturas finais

As capturas foram geradas em Chromium, com todas as fontes e imagens locais carregadas.

- [Home desktop, 1440px](visual-review/index-1440.png)
- [Home mobile, 390px](visual-review/index-390.png)
- [Sistemas desktop](visual-review/sistemas-1440.png)
- [Sobre desktop](visual-review/sobre-1440.png)
- [Artigo desktop](visual-review/noticia-sistemas-implantacao-1440.png)
- [Menu mobile aberto](visual-review/menu-mobile-open.png)
- [Resultados completos do navegador](visual-review/browser-results.json)

## Verificações executadas

- `python3 check.py`: 9 páginas, zero erros.
- `python3 -m unittest discover -s tests -v`: 5 testes aprovados.
- `python3 tests/browser_smoke.py --output /workspace/nugecid-review --axe /tmp/axe-nugecid.min.js`:
  45 combinações de página/largura aprovadas em 320, 390, 768, 1024 e 1440px;
  menu por teclado, disclosures, imagens e salto ao conteúdo aprovados.
- axe-core 4.10.3: zero violações nos critérios automatizados WCAG A/AA das nove páginas
  em 390 e 1440px. Não equivale a certificação completa de acessibilidade.
- `designmd lint DESIGN.md`: zero erros e zero avisos.
- `git diff --check`: aprovado.
- Comparação com o commit original `b75226e`: nenhum destino de link removido das oito
  páginas originais; parágrafos institucionais e definições preservados, incluindo
  atribuições completas, metadados técnicos e informações bibliográficas.
- `livro-capa.webp` e `brasao-pcirn.webp`: conteúdo binário igual ao commit original.

## Limites preservados

O SGC continua interno; OJS e DSpace continuam em implantação. Datas e endereço ainda
pendentes de confirmação permanecem conforme o conteúdo original. Não foi inventado
acesso público, notícia, formulário ou mecanismo de busca para preencher o mockup.
O site permanece estático, sem build ou JavaScript de aplicação.
Nenhuma publicação ou alteração da branch principal faz parte desta entrega.
