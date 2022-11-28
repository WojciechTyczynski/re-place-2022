from PIL import Image
import os
class placecanvas:
    def __init__(self, width, height):
        self.canvas = Image.new('RGB', (width, height), color = 'white')


    def update_pixel_hex(self, x,y,color):
        """
        Sets the specific x,y coordinate in the canvas to the given hex color.

        example:
        update_pixel(10,10,"#B4FBB8")
        """
        h = color.lstrip('#')
        rgb_value = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        self.canvas.putpixel((x,y), rgb_value)

    def update_pixel_int(self, x,y,color):
        """
        Sets the specific x,y coordinate in the canvas to the given hex color.

        example:
        update_pixel(10,10, 8318294)
        """
        self.canvas.putpixel((x,y), self.getRGBfromI(color))

    def save_canvas(self, path = "images/"):
        name = ''
        if(os.path.exists(f'{path}images.png')):
            i = 0 
            while(os.path.exists(f'{path}images {i}.png')):
                i += 1
            self.canvas.save(f'{path}images {i}.png')
            return f'images {i}.png'
        else:
            self.canvas.save(f'{path}images.png')
            return 'images.png'

    def get_image(self):
        return self.canvas

    def getRGBfromI(self, RGBint):
        blue =  RGBint & 255
        green = (RGBint >> 8) & 255
        red =   (RGBint >> 16) & 255
        return red, green, blue