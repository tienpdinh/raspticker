from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw, ImageOps
from FinancialModelingPrepApi import FinancialModelingPrepApi
import asyncio
import secret
from datetime import datetime, timezone

inky_display = auto()
inky_display.set_border(inky_display.WHITE)

async def main():
    ticker = 'DKNG'
    fmp = FinancialModelingPrepApi(str(secret.API_KEY))
    while True:
        img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype('./assets/Consolas.ttf', 22)
        price = await fmp.get_stock_price(ticker)
        ticker_w, ticker_h = font.getsize(ticker)
        price_w, price_h = font.getsize(price)
        ticker_x = (inky_display.WIDTH / 2) - (ticker_w / 2)
        ticker_y = (inky_display.HEIGHT / 2) - (ticker_h / 2) - ticker_h
        price_x = (inky_display.WIDTH / 2) - (price_w / 2)
        price_y = (inky_display.HEIGHT / 2) - (price_h / 2) + price_h

        draw.text((ticker_x, ticker_y), ticker, inky_display.BLACK, font)
        draw.text((price_x, price_y), str(price), inky_display.BLACK, font)
        inky_display.set_image(img)
        inky_display.show()

        print(f'Updated at {datetime.now(timezone.utc)}!')
        await asyncio.sleep(5)

asyncio.run(main())