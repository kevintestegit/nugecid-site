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
