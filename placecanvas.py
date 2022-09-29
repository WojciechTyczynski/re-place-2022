from PIL import Image
import os
class PlaceCanvas:
    def __init__(self, width, height):
        self.canvas = img = Image.new('RGB', (width, height), color = 'white')


    def update_pixel(self, x,y,color):
        """
        Sets the specific x,y coordinate in the canvas to the given hex color.

        example:
        update_pixel(10,10,"#B4FBB8")
        """
        h = color.lstrip('#')
        rgb_value = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        self.canvas.putpixel((x,y), rgb_value)

    def save_canvas(self, path = "images"):
        if(os.path.exists(f'{path}/images.png')):
            i = 0 
            while(os.path.exists(f'{path}/images ({i}).png')):
                i += 1
            self.canvas.save(f'{path}/images ({i}).png')
        else:
            self.canvas.save(f'{path}/images.png')