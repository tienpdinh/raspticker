import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import subprocess
import time

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)
# Create the SSD1306 OLED class.
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)


# Input pins:
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT
button_A.pull = Pull.UP

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT
button_B.pull = Pull.UP

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT
button_L.pull = Pull.UP

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT
button_R.pull = Pull.UP

button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT
button_U.pull = Pull.UP

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT
button_D.pull = Pull.UP

button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT
button_C.pull = Pull.UP


# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 0
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

font = ImageFont.truetype('assets/Consolas.ttf', 10)

# Feature toggle to display pihole info
pihole = False

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    if not button_A.value:
        pihole = not pihole

    if pihole:
        cmd = 'pihole version | head -n 1 | cut -d ' ' -f6'
        PiHoleVersion = subprocess.check_output(cmd, shell = True)
        cmd = 'pihole status'
        PiHoleStatus = subprocess.check_output(cmd, shell = True)

        draw.text((x, top),       "Version: " + PiHoleVersion.decode('ascii'),  font=font, fill=255)
        draw.text((x, top+8),     PiHoleStatus.decode('ascii') + '%', font=font, fill=255)
    else:
        # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell = True)
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell = True)
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell = True)
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell = True)
        cmd = "vcgencmd measure_temp | cut -d '=' -f2"
        Temp = subprocess.check_output(cmd, shell = True)

        # Write two lines of text.

        draw.text((x, top),       "IP: " + IP.decode('ascii'),  font=font, fill=255)
        draw.text((x, top+8),     CPU.decode('ascii') + '%', font=font, fill=255)
        draw.text((x, top+16),    MemUsage.decode('ascii'),  font=font, fill=255)
        draw.text((x, top+25),    Disk.decode('ascii'),  font=font, fill=255)
        draw.text((x, top+33),    "CPU Temp: "+ Temp.decode('ascii'), font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.show()
    time.sleep(.1)