from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw

inky_display = auto()
inky_display.set_border(inky_display.WHITE)

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

font = ImageFont.truetype('./assets/Consolas.ttf', 22)

message = "Hello, World!"
w, h = font.getsize(message)
x = (inky_display.WIDTH / 2) - (w / 2)
y = (inky_display.HEIGHT / 2) - (h / 2)

draw.text((x, y), message, inky_display.YELLOW, font)
inky_display.set_image(img)
inky_display.show()