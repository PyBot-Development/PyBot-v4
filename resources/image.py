from PIL import Image, ImageFont, ImageDraw
try: from resources import support
except: import support

async def GENERATE_CAN(name, text, bottom_text=""):
    if len(text) > 20 or len(bottom_text) > 30:
        return False
    W, H = (582,975)
    font_ = ImageFont.truetype(f"{support.path}/resources/fonts/NotoSansJP/NotoSansJP-Medium.otf", 50)
    font__ = ImageFont.truetype(f"{support.path}/resources/fonts/NotoSansJP/NotoSansJP-Medium.otf", 30)
    img = Image.open(f"{support.path}/resources/templates/can_template.png")

    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(text, font=font_)
    w2, h2 = draw.textsize(bottom_text, font=font__)

    draw.text(((W-w)/2, 300), text, (255,255,0), font=font_)
    draw.text(((W-w2)/2, 700), bottom_text, (0,0,0), font=font__)

    img.save(f"{support.path}/data/temp/{name}.png")
    return(f"{support.path}/data/temp/{name}.png")