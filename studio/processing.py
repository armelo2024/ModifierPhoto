from io import BytesIO
from PIL import Image, ImageColor
from rembg import remove

def remove_background_and_apply_color(infile, bg_color="#FFFFFF", transparent=False):
    # Lire l'image
    img = Image.open(infile).convert("RGBA")

    # Retirer l'arrière-plan (retourne PNG avec alpha)
    with BytesIO() as input_buf:
        img.save(input_buf, format="PNG")
        result = remove(input_buf.getvalue())

    fg = Image.open(BytesIO(result)).convert("RGBA")

    if transparent:
        # On garde la transparence
        out = fg
    else:
        # Appliquer une couleur unie sous le calque alpha
        color = ImageColor.getrgb(bg_color)
        bg = Image.new("RGBA", fg.size, color + (255,))
        bg.paste(fg, (0, 0), fg)
        out = bg.convert("RGB")  # fond opaque

    # Retourner les octets
    out_bytes = BytesIO()
    fmt = "PNG" if transparent else "JPEG"
    out.save(out_bytes, format=fmt, quality=90)
    out_bytes.seek(0)
    return out_bytes, fmt.lower()
