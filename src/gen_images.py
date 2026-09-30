#!/usr/bin/env python3
"""Gera as imagens de exemplo do deck BBDW com o Gemini do projeto do totem.

A chave vem de ../../fabricadesoftware/.env (GEMINI_KEY) e nunca é impressa.
Visitantes são fictícios: primeiro gera a "foto no totem" (base-*), depois
cada feature usa essa foto como entrada, igual ao fluxo real do totem.

Uso (com o venv do fabricadesoftware, que já tem google-genai):
  python gen_images.py              # gera tudo que ainda não existe
  python gen_images.py nome1 nome2  # (re)gera só esses
"""
import os, sys, pathlib
from google import genai
from google.genai import types

HERE = pathlib.Path(__file__).resolve().parent
ENV = HERE.parents[1] / "fabricadesoftware" / ".env"
OUT = HERE / "img" / "gen"
OUT.mkdir(parents=True, exist_ok=True)

for line in ENV.read_text().splitlines():
    if line.startswith("GEMINI_KEY=") and "GEMINI_KEY" not in os.environ:
        os.environ["GEMINI_KEY"] = line.split("=", 1)[1].strip().strip('"').strip("'")
client = genai.Client(api_key=os.environ["GEMINI_KEY"])

FLASH = "gemini-3.1-flash-image"
PRO = "gemini-3-pro-image"

PALETTE = ("a palette of electric lemon yellow and royal blue as the main colors, with touches of deep indigo "
           "and cyan (colors only — never write color names or codes as text in the image)")
KEEP = ("Keep the exact face, facial features, skin tone, hairstyle, glasses and identity of every person from the "
        "input photo — each one must be clearly recognizable. Photorealistic, high detail, cinematic lighting.")
WEBCAM = ("Candid photo taken by a photo-kiosk webcam at a tech conference in Brasília, chest-up framing, neutral indoor "
          "convention-center lighting, slightly soft webcam quality, plain background. Realistic photo, no text.")
SCREEN = ("Behind them a giant LED screen displays the text \"BB DIGITAL WEEK 2026\" in bold clean sans-serif letters "
          "with a gradient in " + PALETTE + "; the only readable text is \"BB DIGITAL WEEK 2026\", spelled exactly "
          "B-B D-I-G-I-T-A-L W-E-E-K 2-0-2-6 with crisp, perfectly formed letters.")

# nome: (referências, modelo, prompt, proporção)
JOBS = {
    # ---------- fotos de entrada (visitantes fictícios) ----------
    "base-grupo": ([], FLASH,
        "A group of four Brazilian coworkers at a tech conference: a woman in a wheelchair with short grey hair in front, "
        "a tall Black woman with braids, a young white man with red hair and freckles, and a Brazilian man in his 40s with "
        "a moustache; all wearing conference lanyards and smiling. " + WEBCAM, "4:3"),
    "base-senior": ([], FLASH,
        "A Brazilian man in his early 60s, grey beard, bald, wearing a light blue button-down shirt and a conference "
        "lanyard, friendly smile. " + WEBCAM, "3:4"),
    "base-jovem": ([], FLASH,
        "A Brazilian university student in her early 20s, Indigenous-Brazilian features, long straight black hair, "
        "round glasses, oversized denim jacket and a conference lanyard, big smile. " + WEBCAM, "3:4"),

    # ---------- palestrante no BBDW ----------
    "palestrante-senior": (["base-senior"], PRO,
        "Place the man from this photo as the solo keynote speaker on the main stage of a large technology conference, "
        "wearing a headset microphone, one hand raised mid-sentence, confident. " + SCREEN + " Medium shot from the "
        "front rows: the speaker stands center-right, framed from the knees up and filling the lower two thirds of the frame, face large and clearly lit by a "
        "warm spotlight; heads and raised phones of the audience along the bottom edge, stage lights and haze. " + KEEP + " Vertical portrait composition (2:3, like a 10×15 photo print).", "2:3"),
    "palestrante-grupo": (["base-grupo"], PRO,
        "Place the four people from this photo as panelists in a debate on the main stage of a large technology "
        "conference, standing close together at center stage as a group (the woman in the wheelchair in front), one "
        "of them speaking into a handheld microphone while the others smile at the audience. " + SCREEN + " Shot from "
        "the front rows, faces large and clearly lit, backs of audience heads at the bottom edge. " + KEEP +
        " Vertical portrait composition (2:3, like a 10×15 photo print).", "2:3"),

    # ---------- você no futuro digital ----------
    "futuro-grupo": (["base-grupo"], PRO,
        "Show the four people from this photo as a team of AI researchers in a bright, modern, realistic research lab "
        "in Brasília: they wear normal smart-casual clothes (shirts, blazers, knitwear) with white lab coats open over "
        "them on two of them, and their conference lanyards; the woman stays in her own ordinary wheelchair. They are "
        "gathered around a large glass table that projects a subtle holographic 3D map of Brasília and data charts, one "
        "of them pointing at it, all smiling and engaged. Clean white and light-wood lab with large monitors showing "
        "graphs, plants, big windows with daylight and Niemeyer-style architecture outside. Only small accent lights "
        "in " + PALETTE + ". Realistic, not sci-fi, no costumes, no armor. " + KEEP +
        " Vertical portrait composition (2:3, like a 10×15 photo print), no text.", "2:3"),
    "futuro-jovem": (["base-jovem"], PRO,
        "Transform the young woman from this photo into an AI researcher of the year 2036: augmented-reality glasses, "
        "a translucent holographic neural-network visualization floating in front of her, soft light accents in "
        + PALETTE + ", at dusk on a rooftop terrace overlooking a futuristic Brasília skyline with the Esplanada and "
        "the National Congress towers. " + KEEP + " Vertical portrait composition (2:3, like a 10×15 photo print), no text.", "2:3"),

    # ---------- jornal do futuro ----------
    "jornal-senior": (["base-senior"], PRO,
        "Create the full front page of a Brazilian printed broadsheet newspaper named \"CORREIO DO FUTURO\", dated "
        "\"Brasília, 27 de outubro de 2036\". Main headline in Portuguese: \"Engenheiro de Brasília cria rede de "
        "energia solar inteligente para todo o Centro-Oeste\". A large front-page photo of the man from the input photo, "
        "ten years older, smiling in front of solar panels at sunset — keep his face recognizable. Below, three smaller "
        "news columns in Portuguese with short headlines: \"Carros autônomos já são maioria no Eixo Monumental\", "
        "\"IA ajuda produtor do cerrado a dobrar a colheita\", \"Escolas do DF ensinam programação desde o 1º ano\". "
        "Classic newsprint look, black and white with slight paper texture, serif masthead, realistic newspaper "
        "layout, legible headlines, Portuguese text only.", "3:4"),

    # ---------- envelopamento ----------
    "wrap-bbdw": (["wrap-starwars"], PRO,
        "This is a studio product mockup of a photo-kiosk totem. Keep EXACTLY the same totem shape, proportions, "
        "rounded edges, screen positions, printer slot and camera angle. Show the WHOLE totem from floor to top with "
        "generous empty margin around it, centered, on a seamless light-grey studio background with a soft floor "
        "shadow. Replace only the vinyl wrap artwork with a design for a technology conference: deep black base with "
        "large bold diagonal bands in electric lemon yellow and royal blue, thin cyan circuit lines, and the text "
        "\"BB DIGITAL WEEK 2026\" in large clean white sans-serif letters on the side panel below the side screen. "
        "The screens are ON and glowing, showing a photo-booth app menu with three large buttons over a dark blue "
        "interface. No other text. Photorealistic product render.", "2:3"),
    "totem-evento": (["wrap-bbdw"], PRO,
        "Place this exact totem (same shape, same yellow/blue/black wrap, same \"BB DIGITAL WEEK 2026\" text) inside "
        "the busy exhibition hall of a large technology conference in a modern Brazilian convention center. A young "
        "woman with a conference lanyard is touching the front screen while two friends wait beside her smiling; "
        "people walking in the background, slightly blurred, warm event lighting, some yellow and blue stage lights "
        "far behind. The whole totem is visible from floor to top. Photorealistic event photo, vertical 2:3.", "2:3"),
}

REF_DIRS = [OUT, HERE / "img" / "out"]


def ref_part(name):
    for d in REF_DIRS:
        for ext, mime in ((".png", "image/png"), (".jpg", "image/jpeg")):
            p = d / (name + ext)
            if p.exists():
                return types.Part.from_bytes(data=p.read_bytes(), mime_type=mime)
    sys.exit("referência ausente: " + name)


def gen(name):
    refs, model, prompt, aspect = JOBS[name]
    contents = [ref_part(r) for r in refs] + [prompt]
    cfg = types.GenerateContentConfig(response_modalities=["IMAGE"],
                                      image_config=types.ImageConfig(aspect_ratio=aspect))
    r = client.models.generate_content(model=model, contents=contents, config=cfg)
    for part in r.candidates[0].content.parts:
        if part.inline_data:
            (OUT / f"{name}.png").write_bytes(part.inline_data.data)
            print("ok", name, model)
            return
    print("SEM IMAGEM", name, r.candidates[0].finish_reason)


if __name__ == "__main__":
    names = sys.argv[1:] or [n for n in JOBS if not (OUT / f"{n}.png").exists()]
    for n in names:
        gen(n)
