import calendar
import datetime
import json
import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont

from lib.waveshare_epd import epd7in5b_V2 as epd_m


# configs
calendar_start = calendar.SUNDAY
tmp_dir = './tmp'
assets_dir = './assets'

## Fonts, texts
normal_font = '{}/TenorSans-Regular.ttf'.format(assets_dir)
font_year_family = font_month_family = font_days_family = font_SMTWTFS_family = normal_font
font_year_size = 28
font_month_size = 56
font_days_size = 40
font_SMTWTFS_size = 22
SMTWTFS_texts = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]  # 7 days
SMTWTFS_red_color = [0]
days_red_color_in_week = [0]

# margins
left_margin = 15
right_margin = 15
top_margin = 15
bottom_margin = 15

# master size
# https://www.waveshare.com/product/displays/e-paper/epaper-1/7.5inch-e-paper-b.htm
# 800 * 480 img size
master_x = epd_m.EPD_WIDTH
master_y = epd_m.EPD_HEIGHT

COLORED = 0
NON_COLORED = 255


def exists(path, isdir=None):
    if isdir:
        if not os.path.isdir(path):
            raise FileNotFoundError(path)
    else:
        if not os.path.isfile(path):
            raise FileNotFoundError(path)


def check_assets():
    # directories
    exists(assets_dir, isdir=True)
    exists(tmp_dir, isdir=True)
    # font
    exists(font_year_family)
    exists(font_month_family)
    exists(font_days_family)
    exists(font_SMTWTFS_family)


def dict_startswith_month(dic, s):
    return {k[-2:]: v for k, v in dic.items() if k.startswith(s)}


def dict_holidays(year, month):
    path = '{}/{}-{}.json'.format(tmp_dir, str(year), str(month).zfill(2))
    if os.path.isfile(path):
        with open(path) as f:
            d = json.load(f)
        if (datetime.datetime.now() - datetime.datetime.fromisoformat(d['lastupdate'])).days >= 14:
            d = dict_holiday_json(year, month)
            with open(path, 'w') as f:
                json.dump(d, f)
    else:
        with open(path, 'w') as f:
            d = dict_holiday_json(year, month)
            json.dump(d, f)
    # replace str key to int.
    # json cannnot save int key, only str.
    return {int(k): v for k, v in d['holidays'].items()}


def get_holidays():
    holiday_jp_url = "https://holidays-jp.github.io/api/v1/date.json"
    headers = {
        "Accept-Language": "ja_JP",
    }
    r = urllib.request.Request(holiday_jp_url, headers=headers, method='GET')
    with urllib.request.urlopen(r) as res:
        body = res.read().decode("utf-8")
    return json.loads(body)


def dict_holidays_of_month(year, month):
    holidays = get_holidays()
    key_startswith = '{}-{}'.format(str(year), str(month).zfill(2))
    return dict_startswith_month(holidays, key_startswith)


def dict_holiday_json(year, month):
    data = {}
    data['lastupdate'] = str(datetime.datetime.now())
    data['year'] = year
    data['month'] = month
    data['holidays'] = dict_holidays_of_month(year, month)
    return data


def circle_pos(center_x, center_y, radius, margin=0, margin_top=0, margin_left=0):
    radius = radius - margin
    circle_x_start = center_x - radius - margin_left
    circle_x_end = center_x + radius - margin_left
    circle_y_start = center_y - radius - margin_top
    circle_y_end = center_y + radius - margin_top
    return (circle_x_start, circle_y_start, circle_x_end, circle_y_end)


def draw_day(draw, day, day_x, day_y, col_width, days_col_height, font, today=None):
    if today:
        c = circle_pos((day_x + draw.textsize(str(day), font=font)[0]/2),
                       (day_y + (days_col_height / 4)),
                       (days_col_height / 2),
                       margin=2,
                       margin_top=-5)
        draw.ellipse(c, fill=COLORED)
        draw.text((day_x, day_y), str(day), NON_COLORED, font=font)
    else:
        draw.text((day_x, day_y), str(day), COLORED, font=font)


def create_calendar(year, month):
    calendar.setfirstweekday(calendar_start)
    now = datetime.datetime.now()
    weeks = calendar.monthcalendar(year, month)
    holidays = dict_holidays(year, month)

    # PIL
    # Image.new https://pillow.readthedocs.io/en/stable/reference/Image.html#constructing-images
    black_img = Image.new('1', (master_x, master_y), NON_COLORED)
    red_img = Image.new('1', (master_x, master_y), NON_COLORED)
    black_draw = ImageDraw.Draw(black_img)
    red_draw = ImageDraw.Draw(red_img)
    # fonts
    font_year = ImageFont.truetype(font_year_family, font_year_size)
    font_month = ImageFont.truetype(font_month_family, font_month_size)
    font_days = ImageFont.truetype(font_days_family, font_days_size)
    font_SMTWTFS = ImageFont.truetype(font_SMTWTFS_family, font_SMTWTFS_size)

    # columns
    col_width = (master_x - left_margin - right_margin)/7

    # YEAR
    year_x = master_x - right_margin - \
        black_draw.textsize(str(year), font=font_year)[0]
    black_draw.text((year_x, top_margin), str(year), COLORED, font=font_year)

    # MONTH
    month_x = (master_x - black_draw.textsize(str(month), font=font_month)[0])/2
    black_draw.text((month_x, top_margin), str(month), COLORED, font=font_month)

    # SMTWTFS and line
    for i, x in enumerate(SMTWTFS_texts):
        SMTWTFS_x = col_width * i + \
            (col_width - black_draw.textsize(x, font=font_SMTWTFS)
             [0])/2 + left_margin
        # if Sunday, font color is red
        if i in SMTWTFS_red_color:
            red_draw.text((SMTWTFS_x, top_margin + 75), x, COLORED, font=font_SMTWTFS)
        else:
            black_draw.text((SMTWTFS_x, top_margin + 75), x, COLORED, font=font_SMTWTFS)
    black_draw.line((15, 120, 785, 120), fill=COLORED, width=2)

    # DAYS
    days_col_height = (master_y - 120 - bottom_margin) / len(weeks)
    day_y = 120 + (days_col_height / 4)
    for days_of_week in weeks:
        # weeks
        for index, day in enumerate(days_of_week):
            # days of week
            if not day == 0:
                day_x = col_width * index + (col_width - black_draw.textsize(str(day),
                                                                             font=font_days)[0])/2 + left_margin
                if month == now.month and day == now.day:
                    if index in days_red_color_in_week or day in holidays:
                        draw_day(red_draw, day, day_x, day_y, col_width, days_col_height,
                                 font_days, today=True)
                    else:
                        draw_day(black_draw, day, day_x, day_y, col_width, days_col_height,
                                 font_days, today=True)
                else:
                    if index in days_red_color_in_week or day in holidays:
                        draw_day(red_draw, day, day_x, day_y, col_width, days_col_height,
                                 font_days)
                    else:
                        draw_day(black_draw, day, day_x, day_y, col_width, days_col_height,
                                 font_days)
        day_y = day_y + days_col_height
    
    return (black_img, red_img)


def write_to_epd(black_img, red_img):
    epd = epd_m.EPD()
    epd.init()
    epd.display(epd.getbuffer(black_img), epd.getbuffer(red_img))
    epd.sleep()


if __name__ == '__main__':
    check_assets()
    
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    month_offset = (now - datetime.datetime(year, month, 1)).days
    if (-365 + 31) <= month_offset <= (365 * 2):
        black_img, red_img = create_calendar(year, month)
    else:
        print('ERROR: Cannot create calendar. Select Year/Month is out of range.')
    
    write_to_epd(black_img, red_img)

