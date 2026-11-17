import random
from PIL import Image, ImageDraw, ImageFont
import os

class GhostCaptcha:
    def __init__(self, frame_count = 5,height = 150, width = 600, captcha_text = "1412", auto_generate = False):
        self.height = height
        self.width = width
        self.auto_generate = auto_generate
        self.frame_count = frame_count
        self.captcha_text = self.auto_generate_captcha() if self.auto_generate else captcha_text

    def auto_generate_captcha(self):
        # generates a captcha code of 6 characters
        uppecase_letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        digits = "0123456789"
        
        sample_space = []
        for entity in [uppecase_letter, digits]:
            length = len(entity)
            for _ in range(3):
                index = random.randint(0, length - 1)
                sample_space.append(entity[index])
        
        captcha_text = []
        count = len(sample_space)
        while sample_space:
            index = random.randint(0, count - 1)
            captcha_text.append(sample_space[index])
            count -= 1
            sample_space.pop(index)
        return "".join(captcha_text)

    def generate_ref_image(self):
        padding_percent = 4
        bg_color = (255, 255, 255)

        # blank image
        image = Image.new("RGB", (self.width, self.height), color = bg_color) 
        draw = ImageDraw.Draw(image)
        text = self.captcha_text
        
        font_path = os.getcwd() + r"\RES\JetBrainsMono-ExtraBold.ttf"
        font_size = 10
        while True:
            font = ImageFont.truetype(font_path, font_size)
            bbox = draw.textbbox((0, 0), text, font = font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            padding_width = (self.width - text_width)/2
            padding_height = (self.height - text_height)/2

            padding_width_percent = (padding_width/self.width)*100
            padding_height_percent = (padding_height/self.height)*100

            if padding_width_percent > padding_percent and padding_height_percent > padding_percent:
                font_size = max(font_size + 1, 10)
            else:
                font_size = max(font_size - 1, 10)
                break

        # top left coordinates         
        x = padding_width
        y = padding_height - bbox[1]

        draw.text((x, y), text, fill=(0, 0, 0), font = font)
        return image

    def generate_frame(self, ref_image):
        ref_pixels =  ref_image.load()
        focus_cordinates = {}
        frames = []
        for x in range(self.width):
            for y in range(self.height):
                if ref_pixels[x,y] == (0,0,0):
                    focus_cordinates[(x,y)] = random.getrandbits(1)
        bg_color = (255, 255, 255)
        for _ in range(self.frame_count):
            ghost_image = Image.new("RGB", (self.width, self.height), color = bg_color)
            ghost_pixel = ghost_image.load()
            for x in range(self.width):
                for y in range(self.height):
                    if (x,y) in focus_cordinates:
                        ghost_pixel[x,y] = (0,0,0) if focus_cordinates[(x,y)] == 1 else (255,255,255)
                    else:
                        ghost_pixel[x,y] = (0,0,0) if random.getrandbits(1) == 1 else (255,255,255)
            frames.append(ghost_image)
        return frames
            

    def generate_gif(self):
        ref_image = self.generate_ref_image()
        frames = self.generate_frame(ref_image)
        output_path = os.path.join(os.getcwd(), "output_animation.gif")
        frames[0].save(output_path, 
                       save_all=True,
                       append_images=frames[1:],  # All subsequent frames
                       duration=10,              # Duration of each frame in milliseconds (100ms = 0.1s)
                       loop=0                     # 0 = infinite loop, numbers = specific repeat count
                       )
        print(self.captcha_text)
        


        
        

GC = GhostCaptcha(auto_generate=True, frame_count= 100,height=150, width=600)
GC.generate_gif()
#print(GC.auto_generate_captcha())
        


        