# Totem CRIA · BB Digital Week 2026

Deck de proposta do Totem CRIA para o BB Digital Week 2026 (27 a 29 de outubro,
Ulysses Centro de Convenções, Brasília). Site estático, sem build step no deploy
e sem dependências em runtime. Mesma estrutura do deck da Hasbro.

## Deploy na Vercel

**Pela interface:** importe o repositório em vercel.com/new. *Framework Preset*
`Other`, *Build Command* vazio, *Output Directory* vazio (raiz).

**Pela CLI:**

```bash
vercel deploy --prod
```

`vercel.json` define cache longo para `/media` e `X-Robots-Tag: noindex` — o deck
não deve ser indexado.

## Estrutura

```
index.html                 deck completo; CSS, fontes e imagens embutidos
media/*.mp4                vídeos reais do totem em operação (servidos como arquivo)
og.jpg                     preview para compartilhamento do link
Totem-CRIA-BBDW-2026.pdf   versão impressa, 11 páginas em paisagem
vercel.json                headers de cache e noindex
src/deck.src.html          fonte do deck (marcadores __IMG_*__, __VID_*__, __FONT_*__)
src/build.py               gera ../index.html e src/deck-bbdw.html (sem vídeo)
src/gen_images.py          gera as imagens de exemplo com o Gemini do totem
src/make_moldura.py        monta o conceito de moldura 10×15 do BBDW
src/img/out/               imagens finais usadas no deck
src/img/gen/               PNGs brutos do Gemini (fora do git)
```

## Editando

```bash
cd src && python3 build.py
```

## Gerando o PDF

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer --window-size=1600,900 \
  --print-to-pdf="Totem-CRIA-BBDW-2026.pdf" --virtual-time-budget=8000 \
  "file://$PWD/index.html"
```

A janela de 1600×900 é obrigatória: sem ela o Chrome usa o layout de tela pequena.

## Imagens de exemplo

Geradas com `src/gen_images.py` (usa `GEMINI_KEY` de `../fabricadesoftware/.env`,
com o venv de lá). Os visitantes são **fictícios**: primeiro é gerada a "foto no
totem" (`base-*`), depois cada experiência usa essa foto como entrada, igual ao
fluxo real. Nos prompts, as cores vão por nome — com código hex a IA escreve o
código como texto na imagem.

## Conteúdo

Investimento: R$ 48.000 (software 20 mil + hardware 20 mil + logística 8 mil),
mesmo valor da proposta do Porão do Rock. Moldura e envelopamento são conceitos;
a arte final segue o manual de marca do BBDW. O deck não usa o logo oficial do BB.
