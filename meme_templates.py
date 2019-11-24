import os
import shelve

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from dotenv import load_dotenv


class meme_templates():
    """
    Defines a meme template, template consists of a name, meme template image
    path, a font, text regions, and image regions.
    """

    temp_image_name = "temp.jpg"
    load_dotenv()
    image_dir    = os.getenv('MEME_TEMPLATE_DIR')
    default_font = os.getenv('DEFAULT_FONT')

    def __init__(
            self, name, img, fnt=default_font, 
            text_regions=None, image_regions=None):

        assert isinstance(name, str)
        assert isinstance(img, str)
        assert isinstance(fnt, str) or fnt == None
        assert os.path.exists(f'./{self.image_dir}/{img}')

        if isinstance(text_regions, list):
            for i in text_regions: 
                assert isinstance(i,  tuple)
        else:
            assert text_regions == None

        if isinstance(image_regions, list):
            for i in image_regions: 
                assert isinstance(i, tuple)
        else:
            assert image_regions == None

        self.name          = name
        self.img           = './' + self.image_dir + '/' +  img
        self.fnt           = fnt
        self.text_regions  = text_regions
        self.image_regions = image_regions
        

    def format_text(self, image, draw, text, reg):
        """ 
        Calculate the font size and the wrap the text to fit inside the
        designated dimensions.  Return font, and wrapped text
        """
        # size of text block
        reg_width  = self.text_regions[reg][2] - self.text_regions[reg][0]
        reg_height = self.text_regions[reg][3] - self.text_regions[reg][1]

        # init values
        text_height, text_width = 0, 0

        # calculate maximum reasonable font size
        image_width, image_height = image.size


        # fit text inside box
        while True:
            meme_font = ImageFont.truetype(self.fnt, font_size)
            line, wrapped_text = "", ""

            for word in text.split():
                # line with next word
                line_new = line + " " + word
                line_width, temp = draw.textsize(line_new, font=meme_font)

                if line_width <= reg_width:
                    line = line_new
                else:
                    wrapped_text += line + "\n"
                    line = word 

                # text has to many lines, decrease font size
                temp, text_height = draw.multiline_textsize(
                        wrapped_text, font=meme_font)

                if text_height > reg_height:
                    font_size = int(font_size * 0.98)
                    break;
                # Text is to long
                if font_size <= 4:
                    print("error, one or more text fields too long")
                    return

            wrapped_text += line
            temp, text_height = draw.multiline_textsize(
                    wrapped_text, font=meme_font)

            if text_height <= reg_height:
                return wrapped_text, meme_font



    def create_meme(self, *args):
        """
        Create a meme inserting the specified text, or image onto the meme
        template image
        """
        img_obj = Image.open(self.img)
        draw = ImageDraw.Draw(img_obj) 

        i = 0
        for arg in args:
            # get formated text, and its size
            text, meme_font = self.format_text(img_obj, draw, arg, i)

            # draw text on image
            draw.rectangle(list(self.text_regions[i]), outline="red")
            draw.multiline_text(
                (self.text_regions[i][0], self.text_regions[i][1]),
                text, font=meme_font, align="center", fill="black")
            i += 1

        img_obj.save(self.temp_image_name)
        return self.temp_image_name



joker = meme_templates(
    "joker", "joker-trailer.jpg", text_regions=[(0,0,100,40)])

two_buttons = meme_templates(
    "two-buttons", "two-buttons.jpg", 
    text_regions=[(62,84,230,170), (260,50,448,126)])

two_buttons.create_meme("test", "word test bacon eggs pizzzzzza")
