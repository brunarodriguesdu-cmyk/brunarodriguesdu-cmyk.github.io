# Site da Nelis — v1

Site institucional estático. **Sem build, sem dependências, sem cookies, sem analytics.**
É só HTML/CSS: funciona em qualquer hospedagem de arquivo estático.

## Identidade visual

Baseada nas imagens da marca em `Pictures\Nelis` (monograma em degradê lilás, retrato da mascote, tabela de valores).

| Token | Cor | Uso |
|---|---|---|
| `--plum` | `#3B1B3F` | títulos, header, seção escura, botão primário |
| `--lilac-2` | `#8D66E4` | links, destaques, botão lilás |
| `--lilac-wash` | `#EFE4FB` | fundos suaves, ícones, tabelas |
| `--peach` | `#F0B79E` | acento quente (sparkle, filetes) |
| `--cream` | `#FBF6F1` | fundo geral |

Tipografia: **Montserrat** (variável, auto-hospedada em `fonts/`). O arquivo cobre todos os pesos,
então um só `@font-face` serve título e texto. Se quiser site mais leve, vale instalar `fonttools`
e gerar um subset latino (~40 KB em vez de 727 KB).

Imagens da mascote em `assets/` já otimizadas em WebP:
`nelis-corpo-inteiro.webp` (55 KB — hero, corpo inteiro em pose de boas-vindas),
`nelis-hero.webp` (26 KB — retrato, usado no avatar do cartão de conversa),
`nelis-aprovacao.webp` (49 KB — tablet "Você revisa e aprova"). Os PNGs originais ficaram na pasta
para reuso em material impresso — não são referenciados pelo site.

**Como a mascote se integra ao fundo escuro:** a arte original tem fundo preto. Em vez de recortar
(que perderia o brilho lilás), ela é colocada dentro de `.hero-stage` — um painel arredondado com
gradiente ameixa — e usa `mix-blend-mode: screen`. O preto do fundo se funde ao painel e o brilho
da arte vira parte da composição. **Se um dia houver um PNG com fundo transparente, remova o
`mix-blend-mode: screen` do `.hero-mascot`** — com transparência real ele lava a imagem.

## Estrutura
```
index.html                    → página inicial (produto)
styles.css                    → estilos de todas as páginas
favicon.svg                   → ícone da aba
404.html                      → página de erro
robots.txt / sitemap.xml      → indexação (legais ficam fora do índice)
_headers                      → cabeçalhos de segurança (Cloudflare Pages / Netlify)
netlify.toml                  → 404 do Netlify
assets/og-image.png           → imagem de compartilhamento (1200×630)
privacidade/index.html        → Política de Privacidade      (gerado)
termos/index.html             → Termos de Uso                (gerado)
conexao/index.html            → Termo de Autorização Instagram (gerado)
exclusao-de-dados/index.html  → Instruções de exclusão de dados (Meta exige)
build_legal.py                → reconstrói as 3 páginas legais a partir dos .md
tools/make_og.py              → regera assets/og-image.png
```

## Pré-visualizar localmente

```bash
cd Documents/Nelis-site
python -m http.server 8765
# abra http://127.0.0.1:8765
```

As páginas legais **não são editadas aqui**: elas são geradas a partir dos rascunhos em
`~\Automação instagram\docs\legal\*.md`. Quando a advogada revisar o markdown, rode:

```bash
python build_legal.py
```

## Antes de publicar — preencher

Todos os campos pendentes aparecem destacados em amarelo (`<mark>`) nas páginas legais.
Procure por `[` em todos os arquivos:

| Campo | Onde |
|---|---|
| `[RAZÃO SOCIAL]` | rodapé de todas as páginas |
| `[E-MAIL DE PRIVACIDADE]` | privacidade, exclusão de dados |
| `[ENDEREÇO]` | privacidade, termos |
| `[DOMINIO]` | index (link de e-mail) |
| Número do WhatsApp | `index.html` — dois links `wa.me/5522996119580` |
| CNPJ, se diferente | rodapés |

Se o site não usar cookies nem analytics (é o caso hoje), o item 11 da Política de Privacidade
pode ser fechado com: *"Este site não usa cookies de rastreamento."*

## Publicar (escolha um — todos têm plano gratuito)

**Cloudflare Pages** (recomendado: mesma conta que você já usa para o R2)
1. Cloudflare → Workers & Pages → Create → Pages → Upload assets
2. Arraste a pasta `Nelis-site` inteira
3. Aponte o domínio em Custom domains

**Netlify** — arraste a pasta em app.netlify.com/drop. É o mais rápido para testar.

**Vercel** — `npx vercel` na pasta, escolha "Other" como framework.

**No mesmo VPS da Nelis** — o Caddy que já vai servir o OAuth também serve o site:
```
nelis.seudominio.com.br {
    root * /var/www/nelis-site
    file_server
}
```

## Por que este site importa para as aprovações

- **Meta / App Review** exige uma **URL pública de Política de Privacidade** e
  instruções de exclusão de dados → `/[dominio]/privacidade/` e `/[dominio]/exclusao-de-dados/`.
- **Google / Business Profile API** exige um **site representando o negócio** listado
  no Perfil da Empresa. Para a API do Google, o site que conta é o da clínica
  (o do Método EVA serve) — não o do produto.

## Depois

- Registrar domínio (sugestão: `.com.br` via Registro.br, ~R$40/ano).
- Trocar o e-mail `contato@[DOMINIO]` por um endereço real que você acesse.
- Formulário de contato: hoje é WhatsApp + `mailto:`. Se quiser formulário,
  use um serviço sem cookie (ex.: Formspree) e atualize o item 11 da privacidade.
