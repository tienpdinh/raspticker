from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw, ImageOps
from FinancialModelingPrepApi import FinancialModelingPrepApi
import asyncio
import secret
from datetime import datetime

inky_display = auto()
inky_display.set_border(inky_display.WHITE)

async def main():
    ticker = 'DKNG'
    fmp = FinancialModelingPrepApi(str(secret.API_KEY))
    while True:
        img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('./assets/Consolas.ttf', 24)
        font_medium = ImageFont.truetype('./assets/helvetica.ttf', 18)
        font_small = ImageFont.truetype('./assets/Consolas.ttf', 12)
        price = '$' + str(await fmp.get_stock_price(ticker))
        now = datetime.now()
        now_str = 'Updated: ' + now.strftime("%m/%d/%Y, %H:%M:%S")
        ticker_w, ticker_h = font_medium.getsize(ticker)
        price_w, price_h = font.getsize(price)
        now_w, now_h = font_small.getsize(now_str)
        ticker_x = (inky_display.WIDTH / 2) - (ticker_w / 2)
        ticker_y = (inky_display.HEIGHT / 6)
        price_x = (inky_display.WIDTH / 2) - (price_w / 2)
        price_y = (inky_display.HEIGHT / 2) - (price_h / 2)
        now_x = (inky_display.WIDTH / 2) - (now_w / 2)
        now_y = (2 * inky_display.HEIGHT / 3)

        draw.text((ticker_x, ticker_y), ticker, inky_display.BLACK, font_medium)
        draw.text((price_x, price_y), price, inky_display.YELLOW, font)
        draw.text((now_x, now_y), now_str, inky_display.BLACK, font_small)
        inky_display.set_image(img)
        inky_display.show()

        print(f'Updated at {now}!')
        await asyncio.sleep(6*60)

asyncio.run(main())