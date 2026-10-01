# NUGECID — Sistema de Design Institucional

Documento de referência estética e arquitetura visual para o portal do **NUGECID** (Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória) da **Polícia Científica do Rio Grande do Norte (PCIRN)**.

---

## 1. Princípios de Design & Anti-Slop / Avoid AI Design

Este sistema de design foi concebido com diretrizes estritas contra clichês de geração automática de inteligência artificial (*AI slop*):

1. **Rejeição do Clichê Manila/Dossiê Sujo (SD1):** Eliminação de fundos bege-amarelados/kraft (`#ece3cf`), carimbos tortos com `-3deg` e falso aspecto envelhecido. O portal representa um órgão de ponta em ciência forense e inteligência pericial.
2. **Rejeição de Gradientes SaaS Clichê (C1):** Proibição total de gradientes lilás/roxo para ciano (`indigo-to-purple`), botões genéricos de template SaaS ou cartões flutuantes sem ancoragem.
3. **Rejeição de Monospace Indiscriminado (SD4):** A fonte com largura fixa (`IBM Plex Mono`) é estritamente restrita a identificadores técnicos (ISBN, números de portaria, código de barras SCV, termos de custódia e stacks). Headings, kickers e corpo utilizam tipografia proporcional com leitura refinada.
4. **Composição e Hierarquia Claras (60-30-10):**
   - **60% Superfície:** Branco e ardósia sutil (`#f8fafc`, `#ffffff`, `#f1f5f9`), conferindo clareza, limpeza técnica e laboratorial.
   - **30% Estrutura Institucional:** Azul meia-noite pericial (`#09111e`, `#0e1c2f`), garantindo autoridade, contraste superior a 12:1 e peso solene de segurança pública.
   - **10% Acentos com Função:** Ouro/Latão pericial (`#c29329`) para insígnias, badges e destaque; esmeralda (`#059669`) e âmbar (`#d97706`) com anéis de pulso para status operacionais reais.
5. **Movimento com Propósito Físico (*Snappy & Tactile*):**
   - Animações escalonadas com curva física de mola (`cubic-bezier(0.16, 1, 0.3, 1)`).
   - Efeito de perspectiva 3D na capa da publicação institucional.
   - Lightbox modal interativo para exploração de telas de sistemas em alta definição.
   - Suporte nativo à preferência de redução de movimento (`@media (prefers-reduced-motion: reduce)`).

---

## 2. Paleta de Cores e Tokens

| Token | Hex | Função e Aplicação |
|---|---|---|
| `--navy-deep` | `#09111e` | Cabeçalho, Hero principal, Rodapé institucional |
| `--navy-dark` | `#0e1c2f` | Superfícies escuras elevadas e modais |
| `--navy-border` | `#1e3553` | Divisores e bordas em temas escuros |
| `--bg-page` | `#f8fafc` | Fundo principal da página (claro e legível) |
| `--bg-surface` | `#ffffff` | Cartões, fichas e blocos de conteúdo |
| `--bg-surface-elevated` | `#f1f5f9` | Destaques sutis, tabelas e chips |
| `--ink-primary` | `#0f172a` | Texto de alta prioridade (títulos, corpo principal) |
| `--ink-secondary` | `#334155` | Texto descritivo e listas |
| `--ink-muted` | `#64748b` | Metadados e legendas |
| `--gold-accent` | `#c29329` | Insígnia da PCIRN, destaques e números-chave |
| `--blue-primary` | `#003566` | Botões de ação primária e links com foco |
| `--status-live-dot` | `#10b981` | Pulso de status: sistemas em uso na instituição |
| `--status-dev-dot` | `#f59e0b` | Pulso de status: sistemas em fase de implantação |

---

## 3. Tipografia

- **Títulos & Display:** `Plus Jakarta Sans` (pesos 600, 700, 800) — Tipografia geométrica contemporânea, austera e de alta precisão.
- **Corpo & Leitura:** `Plus Jakarta Sans` / `Archivo` (pesos 400, 500) — Entrelinhamento de 1.65, contraste superior aos critérios WCAG AAA.
- **Dados Técnicos & Códigos:** `IBM Plex Mono` (pesos 400, 600) — Estritamente para ISBNs, tabelas de stack e identificadores.

---

## 4. Componentes Chave

1. **Insígnia Institucional SVG:** Escudo pericial com mira de precisão, representando segurança, veracidade das provas e salvaguarda documental.
2. **Badges de Status (`.stamp`):**
   - `.stamp--internal`: Uso interno na PCIRN.
   - `.stamp--dev`: Em implantação (OJS e DSpace), com animação de pulso contínuo (`@keyframes pulse-dot`).
   - `.stamp--live`: Operacional.
3. **Showcase do Livro Institucional:**
   - Apresentação em perspectiva 3D com rotação sutil e profundidade de sombra dinâmica.
   - Botão interativo de cópia de ISBN com feedback instantâneo.
4. **Visualizador Interativo de Telas (Lightbox Modal):**
   - Permite inspecionar as interfaces do SGC, OJS e DSpace em tela cheia com fechamento por teclado (Esc), backdrop blur e acessibilidade completa.
5. **Menu Responsivo Móvel:**
   - Navegação otimizada para smartphones e tablets com alternador animado.
6. **Barra de Acessibilidade Governamental (Padrão e-MAG / Gov.br):**
   - Atalhos semânticos de teclado (`accesskey="1"`, `accesskey="2"`, `accesskey="3"`).
   - Alternador de Alto Contraste com persistência em `localStorage`.
   - Redimensionador de fonte tipográfica (A- / A / A+).
7. **Breadcrumbs (Trilha de Navegação):**
   - Navegação hierárquica acessível em todas as subpáginas.
8. **Linha do Tempo Histórica e Normativa:**
   - Componente sequencial narrativo em `sobre.html` com marcos legais (2022 a 2026).
9. **Filtro Rápido e Busca Instantânea de Notícias:**
   - Busca em tempo real e filtros por categoria (`Todos`, `Sistemas`, `Memória`) sem recarregamento.
10. **Caixa de Citação Científica (ABNT & BibTeX):**
    - Facilidade para citação acadêmica da obra institucional com cópia em um clique.
11. **FAQ em Acordeão Semântico:**
    - Elementos `<details>` e `<summary>` acessíveis nativamente para esclarecimento de dúvidas frequentes.
12. **Favicon SVG Vetorial Dinâmico:**
    - Ícone com o escudo pericial e mira de precisão forense no formato SVG leve.

