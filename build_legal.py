#!/usr/bin/env python3
"""
Gera as páginas legais do site da Nelis a partir dos rascunhos em markdown
que ficam em `Automação instagram/docs/legal/`.

Uso:
    python build_legal.py

Depois que a advogada revisar o .md, rode de novo — o .md continua sendo a fonte.
Texto entre colchetes ([RAZÃO SOCIAL], [E-MAIL]...) sai destacado em amarelo,
para ninguém publicar com buraco no documento.
"""

import html
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEGAL_DIR = Path.home() / "Automação instagram" / "docs" / "legal"

PAGES = [
    # (arquivo md, pasta de destino, título da página)
    ("POLITICA_DE_PRIVACIDADE.md", "privacidade", "Política de Privacidade"),
    ("TERMOS_DE_USO.md", "termos", "Termos de Uso"),
    ("TERMO_AUTORIZACAO_CONEXAO_INSTAGRAM.md", "conexao", "Autorização de Conexão"),
]

# Seções internas que NÃO podem ir para o ar
CUT_MARKERS = [
    "### Para o desenvolvimento",
    "### Pontos para a advogada revisar",
    # Blocos internos criados em 12/11/2026: guardam cláusulas ainda não decididas e
    # explicações de revisão. Nada disso pode ir para a página pública — campo em branco
    # publicado vira promessa vazia ou contrato incompleto.
    "### Pendências comerciais e jurídicas (não publicar)",
    "### Pendências técnicas e jurídicas (não publicar)",
]

TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Nelis</title>
<meta name="robots" content="{robots}">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#3B1B3F">
<link rel="stylesheet" href="../styles.css">
</head>
<body>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="../">
      <svg viewBox="0 0 40 40" aria-hidden="true">
        <rect width="40" height="40" rx="12" fill="#3B1B3F"/>
        <path d="M12.5 28.5V12l15 16.5V12" fill="none" stroke="#FBF6F1" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M31.5 6.5l1.15 2.85L35.5 10.5l-2.85 1.15L31.5 14.5l-1.15-2.85L27.5 10.5l2.85-1.15z" fill="#F0B79E"/>
      </svg>
      Nelis
    </a>
    <nav class="nav">
      <a class="opt" href="../#como-funciona">Como funciona</a>
      <a href="../#contato">Contato</a>
    </nav>
  </div>
</header>

<main class="wrap">
  <div class="draft-banner" style="margin-top:26px">
    <strong>Versão em revisão profissional.</strong> Este documento ainda não passou por revisão
    jurídica e não deve ser tratado como aprovado.
  </div>
  <article class="legal narrow">
{body}
  </article>
</main>

<footer class="site-footer">
  <div class="wrap">
    <div><strong style="color:var(--ink)">Nelis Assistente</strong><br>Bruna Rodrigues · CNPJ 38.275.381/0001-94</div>
    <nav>
      <a href="../privacidade/">Privacidade</a>
      <a href="../termos/">Termos</a>
      <a href="../conexao/">Autorização de Conexão</a>
      <a href="../exclusao-de-dados/">Exclusão de dados</a>
    </nav>
  </div>
</footer>

</body>
</html>
"""


def inline(text: str) -> str:
    """Converte markdown inline para HTML, protegendo o texto primeiro."""
    # guarda links antes de escapar
    links = []

    def keep_link(m):
        links.append((m.group(1), m.group(2)))
        return f"\x00LINK{len(links) - 1}\x00"

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", keep_link, text)

    # placeholders [ALGO ASSIM] -> destaque
    text = re.sub(
        r"\[([A-ZÁÂÃÉÊÍÓÔÕÚÇ0-9][^\]]{1,60})\]",
        lambda m: "\x00MARK" + m.group(1) + "\x00",
        text,
    )

    text = html.escape(text, quote=False)

    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)

    for i, (label, url) in enumerate(links):
        text = text.replace(
            f"\x00LINK{i}\x00",
            f'<a href="{html.escape(url)}">{html.escape(label)}</a>',
        )
    text = re.sub(r"\x00MARK([^\x00]+)\x00", r"<mark>\1</mark>", text)
    return text


def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out, i = [], 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # título
        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue

        # régua
        if re.fullmatch(r"-{3,}", stripped):
            out.append("<hr>")
            i += 1
            continue

        # tabela
        if stripped.startswith("|") and i + 1 < n and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
            header = [c.strip() for c in stripped.strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            parts = ["<table>", "<thead><tr>"]
            parts += [f"<th>{inline(c)}</th>" for c in header]
            parts.append("</tr></thead><tbody>")
            for r in rows:
                parts.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            parts.append("</tbody></table>")
            out.append("".join(parts))
            continue

        # citação
        if stripped.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append(f"<blockquote>{inline(' '.join(buf))}</blockquote>")
            continue

        # lista com marcador
        if re.match(r"^[-*]\s+", stripped):
            items = []
            while i < n and re.match(r"^[-*]\s+", lines[i].strip()):
                items.append(inline(re.sub(r"^[-*]\s+", "", lines[i].strip())))
                i += 1
            out.append("<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>")
            continue

        # lista numerada
        if re.match(r"^\d+[.)]\s+", stripped):
            items = []
            while i < n and re.match(r"^\d+[.)]\s+", lines[i].strip()):
                items.append(inline(re.sub(r"^\d+[.)]\s+", "", lines[i].strip())))
                i += 1
            out.append("<ol>" + "".join(f"<li>{x}</li>" for x in items) + "</ol>")
            continue

        # parágrafo
        buf = []
        while i < n:
            s = lines[i].strip()
            if not s or re.match(r"^(#{1,4}\s|\||>\s*[-*]\s|\d+[.)]\s)", s):
                break
            buf.append(s)
            i += 1
        if buf:
            out.append(f"<p>{inline(' '.join(buf))}</p>")

    return "\n".join(out)


def clean(md: str) -> str:
    # Anotações internas de revisão não vão para o público: são bilhetes para a
    # advogada e para a conferência técnica, não texto de contrato.
    md = re.sub(r"\s*\*\*\[CONFERIR[^\]]*\]\*\*", "", md)
    md = re.sub(r"\s*\*\[[CONFERIR[^\]]*\]\*", "", md)
    md = re.sub(r"\s*\*\*\[REVISAR COM ADVOGADA[^\]]*\]\*\*", "", md)
    md = re.sub(r"\s*\[REVISAR COM ADVOGADA[^\]]*\]", "", md)

    for marker in CUT_MARKERS:
        if marker in md:
            md = md.split(marker)[0]
    # o aviso de rascunho do próprio .md é redundante: o site já mostra um banner
    md = re.sub(
        r"(?m)^(?:>[^\n]*\n)+",
        lambda m: "" if "RASCUNHO" in m.group(0) else m.group(0),
        md,
        count=1,
    )
    return md.rstrip().rstrip("-").rstrip()


def main() -> None:
    for md_name, folder, title in PAGES:
        src = LEGAL_DIR / md_name
        if not src.exists():
            print(f"AVISO: não encontrei {src}")
            continue
        body = md_to_html(clean(src.read_text(encoding="utf-8")))
        dest_dir = HERE / folder
        dest_dir.mkdir(parents=True, exist_ok=True)
        (dest_dir / "index.html").write_text(
            TEMPLATE.format(title=title, body=body, robots="noindex,nofollow"),
            encoding="utf-8",
        )
        print(f"gerado: {folder}/index.html  ({len(body)} chars)")


if __name__ == "__main__":
    main()
