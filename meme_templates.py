import os
import os.path
import shelve
import random

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from dotenv import load_dotenv


class MemeTemplates():
    """
    Defines a meme template, template consists of a name, meme template image
    path, a font, text regions, and image regions.
    """

    load_dotenv()
    template_dir    = os.getenv('MEME_TEMPLATE_DIR')
    default_font    = os.getenv('DEFAULT_FONT')
    temp_image_name = os.getenv('TEMP_IMAGE')

    def __init__( self, name: str, img_name: str, fnt_path: str = default_font,
            image_regions: list = [], captions: list = []):

        assert os.path.exists(f'./{self.template_dir}/{img_name}'),\
                    "File does not exist"

        # assign instance variables
        self.name          = name
        self.img_path      = './' + self.template_dir + '/' +  img_name
        self.fnt_path      = fnt_path
        self.image_regions = image_regions
        self.captions      = captions


    def format_text(self, img_obj, draw, text, region):
        """ 
        Calculate the font size and the wrap the text to fit inside the
        designated dimensions.  Return font, and wrapped text
        """
        # size of text block
        reg_width  = region[2] - region[0]
        reg_height = region[3] - region[1]

        # init values
        text_height, text_width = 0, 0

        # calculate maximum reasonable font size
        img_width, img_height = img_obj.size
        fnt_size = int(img_height * 0.12)

        # fit text inside box
        while True:
            fnt_obj = ImageFont.truetype(self.fnt_path, fnt_size)
            line, wrapped_text = "", ""

            for word in text.split():
                # line with next word
                line_new = line + " " + word
                line_width, temp = draw.textsize(line_new, font=fnt_obj)
                
                if line_width <= reg_width:
                    line = line_new
                else:
                    # if line is longer than allowed add a new line
                    wrapped_text += line + "\n"
                    line = word 

                temp, text_height = draw.multiline_textsize(
                        wrapped_text, font=fnt_obj)

                # Text has to many lines, decrease font size
                if text_height > reg_height:
                    fnt_size = int(fnt_size * 0.98)
                    break
                # Text is to long
                if (fnt_size <= 4):
                    pass

            wrapped_text += line

            temp, text_height = draw.multiline_textsize(
                wrapped_text, font=fnt_obj)

            if text_height <= reg_height:
                return wrapped_text, fnt_obj


    def create_meme(self, messages=[], image_dirs=[]):
        """
        Create a meme inserting the specified text, or image onto the meme
        template image
        """
        img_obj = Image.open(self.img_path)
        draw    = ImageDraw.Draw(img_obj) 

        i = 0
        for caption in self.captions:
            region = caption["region"]
            # get formated text, and its size
            text, fnt_obj = self.format_text(img_obj, draw, messages[i], region)
            i += 1

            draw.multiline_text(
                (region[0], region[1]),
                text, font=fnt_obj, align="center", fill="black")

        images = []
        for image_dir in image_dirs:
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            images += [os.path.join(image_dir, f) for f in os.listdir(image_dir)
                       if os.path.isfile(os.path.join(image_dir, f))] 

        # paste images onto template
        for region in self.image_regions:
            rand = random.choice(images)
            rand_img = Image.open(rand) 

            width  = region[2] - region[0]
            height = region[3] - region[1]

            rand_img = rand_img.resize((width,height))
            img_obj.paste(rand_img, (region[0], region[1]))

        img_obj.save(self.temp_image_name)
        return self.temp_image_name



two_buttons = MemeTemplates("two-buttons", "two-buttons.jpg")
two_buttons.captions = [
    {"region": (62,84,230,170),  "emotion": "Happy", "subjective": None},
    {"region": (260,50,448,126), "emotion": "Sad",   "subjective": None}
]

drake = MemeTemplates("drake", "drake.jpg")
drake.image_regions=[(601,0,1197,591), (601,592,1197,1197)]

news = MemeTemplates("news", "news.jpg", image_regions=[(26,206,710,590)])
news.captions = [
    {"region": (137,64,720,90), "emotion": None, "subjective": "Fact"}
]

prison = MemeTemplates("prison", "prison.jpg")
prison.captions = [
    {"region": (272,258,362,299), "emotion": "Sad", "subjective": None}
]

head_out = MemeTemplates("head_out", "head_out.jpg")
head_out.captions = [
    {"region": (0,0,798,73), "emotion": None, "subjective": "Opinion"}
]

tension = MemeTemplates("tension", "tension.jpg")
tension.captions = [
    {"region": (307,480,600,520), "emotion": "Sad", "subjective": None}
]

first_words = MemeTemplates( "first_words", "first_words.jpg")
first_words.captions = [
    {"region": (32,360,458,500), "emotion": None, "subjective": None}
]

database = shelve.open('memes.db')
database[two_buttons.name] = two_buttons
database[drake.name]       = drake
database[news.name]        = news
database[prison.name]      = prison
database[head_out.name]    = head_out
database[tension.name]     = tension
database[first_words.name] = first_words
database.close()
