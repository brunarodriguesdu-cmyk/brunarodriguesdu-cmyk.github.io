# NELIS — atualização visual, 11/11/2026

Página principal atualizada a partir das cinco referências fornecidas pela usuária.

- `index.html`: nova faixa de benefícios, marca tipográfica, imagens atualizadas, link para pular ao conteúdo. Planos, preços, links de contato e rotas legais preservados.
- `home.css`: estilos exclusivos da página comercial. `styles.css` continua atendendo as páginas legais.
- `assets/wave-cream.svg`: transições curvas em SVG.
- `assets/nelis-transparente.webp` e `assets/nelis-aprovacao-transparente.webp`: mascotes com transparência; PNGs correspondentes preservados como fontes.
- `assets/recursos-3d.webp`: seis ilustrações em uma grade 3 × 2, exibidas individualmente por posições de fundo CSS.

## Imagens

Criadas com a ferramenta integrada ImageGen, usando as imagens existentes da mascote como referência. Versões sem transparência e tentativas descartadas não são utilizadas pelo site.

Prompts finais resumidos: remover completamente o fundo da mascote mantendo identidade, cores e pose; isolar a mascote segurando o tablet com o texto “Você revisa e aprova.” e botões “Editar” / “Aprovar”; criar uma grade 3 × 2 de ícones lilás tridimensionais (conteúdo, arte, relatórios, perfil, radar e grupo) em fundo branco uniforme. O fundo branco dos ícones é integrado ao creme com `mix-blend-mode: multiply`.

## Prévia local

Na pasta do projeto: `python -m http.server 8765 --bind 127.0.0.1`.
Abrir http://127.0.0.1:8765/. Não exige build ou instalação de dependências.

Os textos legais ainda contêm campos pendentes preexistentes. A atualização visual não preenche nem modifica esses documentos.
