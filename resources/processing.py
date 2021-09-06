from PIL import Image, ImageFont, ImageDraw
try: from resources import support
except: import support
from gtts import gTTS
from datetime import datetime

async def GENERATE_CAN(name, text, bottom_text=""):
    if len(text) > 90 or len(bottom_text) > 90:
        return False
    def add_n(text, after:int):
        x = ""
        for i, letter in enumerate(text):
            if i % after == 0:
                x += '\n'
            x += letter
        x = x[1:]
        return x

    text = add_n(text, 20)
    bottom_text = add_n(bottom_text, 30)

    W, H = (582,975)
    font_ = ImageFont.truetype(f"{support.path}/resources/fonts/NotoSansJP/NotoSansJP-Medium.otf", 50)
    font__ = ImageFont.truetype(f"{support.path}/resources/fonts/NotoSansJP/NotoSansJP-Medium.otf", 30)
    img = Image.open(f"{support.path}/resources/templates/can_template.png")

    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(text, font=font_)
    w2, h2 = draw.textsize(bottom_text, font=font__)

    draw.text(((W-w)/2, 300-(h/2)), text, (255,255,0), font=font_)
    draw.text(((W-w2)/2, 700-(h2/2)), bottom_text, (0,0,0), font=font__)

    img.save(f"{support.path}/data/temp/{name}.png")
    return(f"{support.path}/data/temp/{name}.png")

async def tts(txt, languag):
    date = str(datetime.utcnow()).replace(":", "-")
    speech = gTTS(text = u'{}'.format(txt), lang = languag, slow = False)
    speech.save(f"{support.path}/data/temp/{date}.mp3")
    return(f"{support.path}/data/temp/{date}.mp3")