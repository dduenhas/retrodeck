# Gera os ícones do RETRODECK (cassete emblemático) — PIL via uv
# Saídas: icons/icon-192.png, icon-512.png, icon-maskable-512.png,
#         apple-touch-icon.png, favicon.ico
from PIL import Image, ImageDraw
import os

HERE = os.path.dirname(os.path.abspath(__file__))       # .../mimo-proj/icons
ROOT = os.path.dirname(HERE)                            # .../mimo-proj
OUT = HERE
os.makedirs(OUT, exist_ok=True)

BG      = (17, 18, 20)        # #111214 fundo
SHELL   = (63, 67, 75)        # corpo da K7
SHELL_L = (139, 144, 153)     # contorno
LABEL   = (245, 241, 228)     # label creme
RED     = (200, 16, 46)       # #c8102e
BLUE    = (26, 63, 143)       # #1a3f8f
WINDOW  = (11, 12, 14)        # janela dos carretéis
HUB     = (233, 234, 238)     # carretel
HUB_IN  = (90, 95, 104)
SCREW   = (154, 160, 170)


def draw_cassette(d, S, ox, oy, s):
    """Desenha a K7 em escala s, canto superior-esquerdo (ox,oy), lado s*S."""
    def R(x, y, w, h, r, fill, outline=None, width=0):
        d.rounded_rectangle([ox+x*s, oy+y*s, ox+(x+w)*s, oy+(y+h)*s],
                            radius=r*s, fill=fill, outline=outline, width=max(1, int(width*s)))
    # corpo
    R(4, 12, 56, 40, 6, SHELL, SHELL_L, 1.4)
    # label creme
    R(8, 15.5, 48, 14, 2, LABEL)
    # faixas vermelha e azul (mesma linguagem da fita do deck)
    d.rectangle([ox+8*s, oy+15.5*s, ox+56*s, oy+20*s], fill=RED)
    d.rectangle([ox+8*s, oy+26.5*s, ox+56*s, oy+29.5*s], fill=BLUE)
    # janela dos carretéis
    R(12, 32, 40, 16, 3, WINDOW)
    # carretéis
    for cx in (23, 41):
        c = [ox+(cx-6.2)*s, oy+40*s, ox+(cx+6.2)*s, oy+40*s]
        d.ellipse([ox+(cx-6.2)*s, oy+33.8*s, ox+(cx+6.2)*s, oy+46.2*s], fill=HUB)
        d.ellipse([ox+(cx-2.3)*s, oy+37.7*s, ox+(cx+2.3)*s, oy+42.3*s], fill=HUB_IN)
    # parafusos
    for sx, sy in ((7.5, 47.5), (56.5, 47.5)):
        d.ellipse([ox+(sx-1.4)*s, oy+(sy-1.4)*s, ox+(sx+1.4)*s, oy+(sy+1.4)*s], fill=SCREW)


def render(size, scale_art, path, rounded=None):
    """scale_art: lado do ícone 64-units dentro do canvas; rounded: raio do bg (None = full-bleed)."""
    img = Image.new('RGBA', (size, size), BG + (255,))
    if rounded:
        mask = Image.new('L', (size, size), 0)
        md = ImageDraw.Draw(mask)
        md.rounded_rectangle([0, 0, size-1, size-1], radius=rounded, fill=255)
        bg = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        bg.paste(img, (0, 0), mask)
        img = bg
    d = ImageDraw.Draw(img)
    art = scale_art * size
    s = art / 64.0
    ox = (size - art) / 2
    oy = (size - art) / 2
    draw_cassette(d, size, ox, oy, s)
    img.save(path)
    print('ok', path, img.size)


# ícones "any" (fundo escuro completo, cantos por conta do launcher)
render(512, 0.86, os.path.join(OUT, 'icon-512.png'))
render(192, 0.86, os.path.join(OUT, 'icon-192.png'))
# maskable: arte menor (zona segura do círculo de 80%)
render(512, 0.62, os.path.join(OUT, 'icon-maskable-512.png'))
# apple-touch: full-bleed, arte um pouco menor
render(180, 0.80, os.path.join(OUT, 'apple-touch-icon.png'))

# favicon .ico (16/32/48 a partir de um render 96 sem texto)
base = render(96, 0.88, os.path.join(OUT, '_tmp_fav.png'))
fav = Image.open(os.path.join(OUT, '_tmp_fav.png')).convert('RGBA')
fav.save(os.path.join(ROOT, 'favicon.ico'),
         sizes=[(16, 16), (32, 32), (48, 48)])
os.remove(os.path.join(OUT, '_tmp_fav.png'))
print('ok favicon.ico')
