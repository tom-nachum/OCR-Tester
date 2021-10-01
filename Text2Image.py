import csv
import os
from PIL import Image, ImageDraw, ImageFont
from glob import glob
from random import randrange
from itertools import combinations
import sys
import codecs

# _fonts_dir = rf'C:\Windows\Fonts'
_fonts_dir = 'fonts'
_this_dir = os.path.abspath(os.curdir.strip('.') + 'images')

ENGLISH = 'abcdefghijkl\nmnopqrstuvwxyz\nABCDEFGHIJKLMN\nOPQRSTUVWXYZ\n'
HEBREW = 'אבגדהוזחטיכלמנסעפצקרשתםףץן' + "\n"
SWEDEN = 'bcdfghjklmnp\nqrstvwxzaeiouyåäö\nÅÄÖABCDEFGHIJKLM\nNOPQRSTUVWXYZ\n'
SPANISH = 'ñ' + ENGLISH[:-1] + 'Ñ'
NUMBERS = '0123456789\n'
SYMBOLS = '~,`!@#$%^&*()-_+={}[]|\/:;"<>.?\'' + "\n"
LANG_DICT = {ENGLISH: "eng", HEBREW: "heb", SPANISH: "spa", SWEDEN: "swe", NUMBERS: "",
             SYMBOLS: ""}
LANGUAGES = [ENGLISH, HEBREW, SWEDEN, SPANISH]
CHARACTERS = LANGUAGES + [NUMBERS, SYMBOLS]
FILE_FORMATS = ['png', 'jpeg', 'jpg']
FONT_SIZES = [8, 9, 32, 71, 72]
PIC_HEIGHT = 1024
PIC_WIDTH = 1280
NOT_SUPPORTS_HEBREW = ["Arial Black", "Bahnschrift", "Cambria", "Cambria Math",
                       "Candara", "Comic Sans MS", "Consolas", "Constantia", "Corbel",
                       "Ebrima", "Forte", "Franklin Gothic Medium", "Gabriola",
                       "Gadugi", "Georgia", "Impact", "Ink Free", "Lucida Console",
                       "Marlett", "MS Gothic", "Segoe Print", "Segoe Script"]
simple_sentence_english = "Simple Test"
simple_sentence_hebrew = "טסט פשוט"
simple_sentence_swedish = "å ä ö enkelt test Å Ä Ö"
simple_sentence_spanish = "ñ prueba simple Ñ"
SIMPLE_TESTS = [simple_sentence_english, simple_sentence_hebrew,
                simple_sentence_swedish, simple_sentence_spanish]

pic_id = 212  # TODO: Change to 1

colors = {
    'white': (0xff, 0xff, 0xff),
    'black': (0x00, 0x00, 0x00),
    'gray': (0x80, 0x80, 0x80),
    'red': (0xff, 0x00, 0x00),
    'green': (0x00, 0xff, 0x00),
    'blue': (0x00, 0x00, 0xff),
}


def list_fonts():
    """ Returns a list of supported fonts. """
    glob_list = glob(os.path.join(_fonts_dir, '*.ttf'))
    # basic_list = sorted(['arial', 'verdana', 'times', 'tahoma', 'symbol', 'georgia',
    #                      'frank', 'cour', 'consola', 'comic', 'cambriab'])
    all_fonts = ["Aharoni Bold", "Arial", "Arial Black", "Bahnschrift",
                 "Calibri", "Cambria", "Cambria Math", "Candara", "Comic Sans MS",
                 "Consolas", "Constantia", "Corbel", "Courier New", "David",
                 "David Bold", "Ebrima", "Forte", "Franklin Gothic Medium", "FrankRuehl",
                 "Gabriola", "Gadugi", "Georgia", "Gisha", "Gisha Bold", "Impact",
                 "Ink Free", "Levenim MT", "Levenim MT Bold", "Lucida Console",
                 "Lucida Sans Unicode", "Marlett", "Microsoft Sans Serif", "Miriam",
                 "Miriam Fixed", "MS Gothic", "Narkisim", "Rod", "Segoe Print",
                 "Segoe Script", "Segoe UI", "Tahoma", "Times New Roman"]
    # fonts = [font for font in basic_list if
    #          os.path.join(_fonts_dir, f"{font}.ttf") in glob_list]
    fonts = [font for font in all_fonts if
             os.path.join(_fonts_dir, f"{font}.ttf") in glob_list]
    return fonts


def list_colors():
    """ Returns a list of supported colors. """
    clrs = [color for color, value in colors.items()]
    return clrs


def random_text(size):
    """ Returns a random string with upper and lower letters (may or not contain spaces). """
    # letters = ascii_letters + '  '
    letters = '\n\n\n       ABC'
    return ''.join([letters[randrange(0, len(letters))] for i in range(size)])


def text_image(text, test_type, font_type='Arial', font_size=20,
               text_x=0, text_y=0,
               img_width=PIC_WIDTH, img_height=PIC_HEIGHT,
               file_format='png', lang='eng'):
    """ creates a PNG image with the desired text and parameters.

    File is created in the current working directory.

    :param int img_width: horizontal size of image
    :param int img_height: vertical size of image
    :param str text: text to write into image. Text may overflow beyond image bounds.
    :param str font_type: type of font, from supported list (see list_fonts())
    :param int font_size: size of font in points
    :param int text_x: x coordinate to start of text
    :param int text_y: y coordinate to start of text
    :returns: None
    """
    global pic_id
    img_color = 'white'
    font_color = 'black'
    if img_color not in list_colors() or font_color not in list_colors():
        raise ValueError("Invalid color. Check available colors with 'list_colors()'")
    if font_type not in list_fonts():
        raise ValueError("Invalid font. Check available fonts with 'list_fonts()'")

    img = Image.new('RGB', (img_width, img_height), color=colors[img_color])
    fnt = ImageFont.truetype(os.path.join(_fonts_dir, f"{font_type}.ttf"), font_size)
    d = ImageDraw.Draw(img)
    d.text((text_x, text_y), text, font=fnt, fill=colors[font_color])

    # th = str(hash(text))[-6:]
    # img_name = f"{font_type}_{font_size}id_{pic_id}." + file_format
    img_name = f"{pic_id}_testType_{test_type}_{font_type}_{font_size}." + file_format
    file_name = os.path.join(_this_dir, img_name)
    print(f"Creating image {file_name}")
    img.save(file_name)
    pic_id += 1
    # print(lang)
    # print(repr(text))
    # expected_texts.append(text)
    # writer.writerow([img_name])


def generate_file_formats():
    for f in FILE_FORMATS:
        text_image('', 'file_format', file_format=f)
        text_image(ENGLISH, 'file_format', file_format=f)


def generate_font_size():
    for f_size in FONT_SIZES:
        for lang in [HEBREW, ENGLISH]:
            text_image(lang, 'font_size', font_size=f_size, lang=LANG_DICT[lang])


def generate_sub_lang():
    for i in range(1, len(CHARACTERS) + 1):
        for sub_set in list(combinations(CHARACTERS, i)):
            lang = LANG_DICT[sub_set[0]]
            for i in range(1, len(sub_set)):
                if sub_set[i] not in [SYMBOLS, NUMBERS]:
                    lang += "+" + LANG_DICT[sub_set[i]]
            text_image("".join(sub_set), 'sub_lang', lang=lang)


def generate_length_of_text():
    letters = "a"
    cols = 116
    rows = 44
    text_image(letters, 'length_of_text')
    for pos in [0, PIC_HEIGHT / 2, PIC_HEIGHT - 20]:
        text_image(letters * cols, 'length_of_text', text_y=pos)
    text_image('\n'.join([letters * cols] * rows), 'length_of_text')


def generate_position_of_text():
    letters = "A"
    for corner in [(0, 0), (0, PIC_HEIGHT - 40),
                   (PIC_WIDTH - 40, 0), (PIC_WIDTH - 40, PIC_HEIGHT - 40)]:
        text_image(letters, 'position', text_x=corner[0], text_y=corner[1], font_size=40)
    text_image(letters, 'position', text_x=int(PIC_WIDTH / 2),
               text_y=int(PIC_HEIGHT / 2), font_size=40)
    for mid in [(0, int((PIC_HEIGHT - 40) / 2)), (int((PIC_WIDTH - 40) / 2), 0),
                (PIC_WIDTH - 40, int((PIC_HEIGHT - 40) / 2)),
                (int((PIC_WIDTH - 40) / 2), PIC_HEIGHT - 40)]:
        text_image(letters, 'position', text_x=mid[0], text_y=mid[1], font_size=40)
    generate_angle_of_text()


def generate_angle_of_text():
    letters = "Y  Y  Y  Y"
    for angle in [(PIC_WIDTH, PIC_HEIGHT), (PIC_HEIGHT, PIC_WIDTH),
                  (PIC_WIDTH, PIC_HEIGHT), (PIC_HEIGHT, PIC_WIDTH)]:
        text_image(letters, 'position', text_x=int(PIC_WIDTH / 2),
                   text_y=int(PIC_HEIGHT / 2),
                   img_width=angle[0],
                   img_height=angle[1], font_size=40)


def generate_space():
    for i in range(5):
        text_image(random_text(40), 'space')


def generate_fonts():
    for f in list_fonts():
        if f == 'Marlett':
            continue
        for s in [8, 72]:
            if f not in NOT_SUPPORTS_HEBREW:
                text_image(HEBREW, 'fonts', font_type=f, font_size=s, lang="heb")
            text_image(ENGLISH, 'fonts', font_type=f, font_size=s)


def generate_line_spaces():
    for i in range(4):
        text_image(ENGLISH + '\n' * i + HEBREW, 'line_spaces', lang="eng+heb")


def generate_simple_tests():
    for sentence in SIMPLE_TESTS:
        text_image(sentence, 'simple_tests', font_size=40,
                   text_x=int(PIC_WIDTH / 2),
                   text_y=int(PIC_HEIGHT / 2))


def generate_pictures():
    generate_file_formats()
    generate_sub_lang()
    generate_fonts()
    generate_font_size()
    generate_length_of_text()
    generate_space()
    generate_position_of_text()
    generate_line_spaces()
    generate_simple_tests()


if __name__ == '__main__':
    # text_image(600, 200, 'Never imagine yourself', 'cambriab', 30, 15, 25)
    # text_image(500, 300, 'not to be otherwise', 'times', 26, 25, 35)
    # text_image(550, 400, 'than what it might appear', 'arial', 32, 35, 45)
    # text_image(600, 200, 'to others that what you were', 'verdana', 16, 55, 65)
    # text_image(500, 300, 'or might have been was not', 'tahoma', 26, 65, 75)
    # text_image(700, 400, random_text(30), 'cour', 40, 75, 85)
    # text_image(600, 400, random_text(40), 'cour', 30, 30, 85)
    #
    # print(list_fonts())
    # print(list_colors())
    #
    # print(random_text(10))
    # print(random_text(10))

    # generate_pictures()
    print('Ya zalame')
