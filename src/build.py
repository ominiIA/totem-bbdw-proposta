#!/usr/bin/env python3
"""Build do deck BBDW.

../index.html     -> Vercel (raiz do repo): <video> aponta para media/*.mp4
deck-bbdw.html    -> versão sem vídeo (pôster no lugar), para hospedagem com limite
Imagens e fontes vão embutidas como data URI nas duas.
"""
import base64, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

def data_uri(path):
    mime = 'image/png' if path.lower().endswith('.png') else 'image/jpeg'
    return 'data:%s;base64,%s' % (mime, b64(path))

IMAGES = {
    '__IMG_LOGO_WHITE__':     'img/out/logo-cria-white.png',
    '__IMG_LOGO_INK__':       'img/out/logo-cria-ink.png',
    '__IMG_TOTEM_EVENTO__':   'img/out/totem-evento.jpg',
    '__IMG_BASE_SOLO__':      'img/out/base-solo.jpg',
    '__IMG_BASE_DUPLA__':     'img/out/base-dupla.jpg',
    '__IMG_BASE_GRUPO__':     'img/out/base-grupo.jpg',
    '__IMG_BASE_SENIOR__':    'img/out/base-senior.jpg',
    '__IMG_BASE_JOVEM__':     'img/out/base-jovem.jpg',
    '__IMG_PAL_DUPLA__':      'img/out/feat-palestrante.jpg',
    '__IMG_PAL_SENIOR__':     'img/out/palestrante-senior.jpg',
    '__IMG_PAL_GRUPO__':      'img/out/palestrante-grupo.jpg',
    '__IMG_FUT_SOLO__':       'img/out/feat-futuro.jpg',
    '__IMG_FUT_GRUPO__':      'img/out/futuro-grupo.jpg',
    '__IMG_FUT_JOVEM__':      'img/out/futuro-jovem.jpg',
    '__IMG_JOR_SOLO__':       'img/out/feat-jornal.jpg',
    '__IMG_JOR_SENIOR__':     'img/out/jornal-senior.jpg',
    '__IMG_MOLDURA_BBDW__':   'img/out/moldura-bbdw.jpg',
    '__IMG_WRAP_BBDW__':      'img/out/wrap-bbdw.jpg',
    '__IMG_MOLDURA_JUNINA__': 'img/out/moldura-junina.jpg',
    '__IMG_MOLDURA_INVERNO__':'img/out/moldura-inverno.jpg',
    '__POSTER_FILA__':        'vid/festival-fila-poster.jpg',
    '__POSTER_ACESS__':       'vid/acessibilidade-poster.jpg',
}
VIDEOS = {
    '__VID_FILA__':  '../media/festival-fila.mp4',
    '__VID_ACESS__': '../media/acessibilidade.mp4',
}

for p in list(IMAGES.values()) + list(VIDEOS.values()):
    if not os.path.exists(p):
        sys.exit('ERRO: asset ausente -> ' + p)

base = open('deck.src.html').read()
base = base.replace('__FONT_NORMAL__', b64('fonts/archivo-normal.woff2'))
base = base.replace('__FONT_EXP__',    b64('fonts/archivo-exp.woff2'))
for token, path in IMAGES.items():
    base = base.replace(token, data_uri(path))

# ---------- Vercel build ----------
web = base
for token, path in VIDEOS.items():
    web = web.replace(token, 'media/' + os.path.basename(path))
web = web.replace('<video muted loop', '<video autoplay muted loop')

marker = '<div class="deck" id="deck">'
head_part, body_part = web.split(marker, 1)
body_part = marker + body_part

DESC = ('Totem de IA da CRIA Incubator para o BB Digital Week 2026 — '
        'o participante no palco, no futuro e na capa do jornal.')
web_doc = (
    '<!doctype html>\n<html lang="pt-BR">\n<head>\n'
    '<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    '<meta name="description" content="%s">\n'
    '<meta name="robots" content="noindex, nofollow">\n'
    '<meta property="og:type" content="website">\n'
    '<meta property="og:title" content="Totem CRIA · BB Digital Week 2026">\n'
    '<meta property="og:description" content="%s">\n'
    '<meta property="og:image" content="og.jpg">\n'
    '<link rel="icon" type="image/png" href="%s">\n'
    '%s</head>\n<body>\n%s\n</body>\n</html>\n'
) % (DESC, DESC, data_uri('img/out/logo-cria-icon.png'), head_part, body_part)

shutil.copy('img/out/feat-palestrante.jpg', '../og.jpg')
open('../index.html', 'w').write(web_doc)

# ---------- versão sem vídeo ----------
art = re.sub(r'<video\b.*?</video>\s*', '', base, flags=re.S)
art = art.replace('.vwrap .poster-img{display:none;', '.vwrap .poster-img{display:block;')
for token in VIDEOS:
    art = art.replace(token, '')
open('deck-bbdw.html', 'w').write(art)

# ---------- report ----------
def mb(n): return '%.2f MB' % (n / 1024 / 1024)
leftovers = re.findall(r'__[A-Z_]+__', web) + re.findall(r'__[A-Z_]+__', art)
if leftovers:
    sys.exit('ERRO: tokens nao substituidos -> ' + ', '.join(sorted(set(leftovers))))

media_total = sum(os.path.getsize(p) for p in VIDEOS.values())
print('../index.html   ', mb(os.path.getsize('../index.html')))
print('../media/       ', mb(media_total))
print('deck-bbdw.html  ', mb(os.path.getsize('deck-bbdw.html')))
