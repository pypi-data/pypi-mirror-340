from PIL import Image
import matplotlib

__version__ = "0.3.1"

def add_fitter(img, fit_img, output_img) -> Image.Image:
    import math

    flag = Image.open(fit_img)
    file = img
    if file:
        head = Image.open(file)
        width, height = flag.size
        flag2 = flag.crop((66, 0, height+66, height))
        for i in range(height):
            for j in range(height):
                color = flag2.getpixel((i, j))
                distance = int(math.sqrt(i**2+j**2))
                alpha = 255-distance//4
                if alpha<0:
                    alpha = 0
                new_color = color[0:-1]+(alpha, )
                flag2.putpixel((i, j), new_color)
        flag_new = flag2.resize(head.size)
        head.paste(flag_new, (0, 0), flag_new)
        head.save(output_img)
    return head

def text_painting(img, char:list, output:str=None) -> str:
    img = Image.open(img)
    img = img.resize((60,60))
    img = img.convert('L')
    txt = ''
    for i in range(60):
        for j in range(60):
            txt += char[int(len(char) * (img.getpixel((j,i)) / 256))]
        txt += "\n"
    if output is not None:
        result=open(output,"w")
        result.write(txt)
        result.close()
    else:
        print(txt)
    return txt

def latex2text(text, output=None):
    if output is None:
        from pylatexenc.latex2text import LatexNodes2Text
        converter = LatexNodes2Text()
        latex_str = text
        readable_str = converter.latex_to_text(latex_str)
        print(readable_str)  # 输出：E = mc²
    else:
        from matplotlib import mathtext
        mathtext.math_to_image(text, output, dpi=300) 

def create_image(red:int, green:int, blue:int, width:int, height:int, alpha:int = 100, output_image=None) -> Image.Image:
    """
    Create a new image.
    
    :params float red: Image depth of red.
    :params float green: Image depth of green.
    :params float blue: Image depth of blue.
    :params float alpha=1: Image depth of alpha.
    :params int width: Image width.
    :params int height: Image height.
    
    :return Image: The created image
    """

    image = Image.new('RGBA', (width, height), (red, green, blue, alpha))
    if output_image is not None:
        image.save(output_image)
    return image