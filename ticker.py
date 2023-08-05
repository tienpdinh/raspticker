from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw, ImageOps
import FinancialModelingPrepApi
import asyncio
import secret

inky_display = auto()
inky_display.set_border(inky_display.WHITE)

async def main():
    fmp = FinancialModelingPrepApi(secret.API_KEY)
    ticker = 'DKNG'
    while True:
        img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype('./assets/Consolas.ttf', 22)
        price = await asyncio.run(fmp.get_price(ticker))
        ticker_w, ticker_h = font.getsize(ticker)
        price_w, price_h = font.getsize(price)
        ticker_x = (inky_display.WIDTH / 2) - (ticker_w / 2)
        ticker_y = (inky_display.HEIGHT / 2) - (ticker_h / 2) - ticker_h
        price_x = (inky_display.WIDTH / 2) - (price_w / 2)
        price_y = (inky_display.HEIGHT / 2) - (price_h / 2) + price_h

        draw.text((ticker_x, ticker_y), ticker, inky_display.BLACK, font)
        draw.text((price_x, price_y), price, inky_display.BLACK, font)
        inky_display.set_image(img)
        inky_display.show()

        await asyncio.sleep(5)

asyncio.run(main())