import argparse
import img_fit

class OutputAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        self.handle_output(parser, namespace, values)

    @staticmethod
    def handle_output(parser, namespace, values):
        setattr(namespace, "output", values) 

parser = argparse.ArgumentParser(description="img_fit commands")
subparsers = parser.add_subparsers(dest="command", required=True)

p_text = subparsers.add_parser("text", help="Get the image text")
p_text.add_argument("from_img", help="The image you want to change",type=str) 
p_text.add_argument("chars", nargs="+", help="The chars ypu want to make a text painting.",type=str) 
p_text.add_argument("-o","--output",action=OutputAction,type=str,help="The output path.")  

subparsers.add_parser("version", help="Get the version.")

p_fitter = subparsers.add_parser("fitter", help="Fitter the image.")
p_fitter.add_argument("from_img",help="The image you want to change",type=str)
p_fitter.add_argument("fitter_img",help="The fitter image.",type=str)
p_fitter.add_argument("output_img",help="The output image path.",type=str)

p_latex = subparsers.add_parser("latex", help="Get the text latex.")
p_latex.add_argument("text",help="The image you want to change",type=str)
p_latex.add_argument("-o","--output",action=OutputAction,type=str,help="The output path.")  

p_create = subparsers.add_parser("create", help="Create a new image.")
p_create.add_argument("img",help="The image you want to change",type=str)
p_create.add_argument("r",help="Image depth of red.",type=int)
p_create.add_argument("g",help="Image depth of green.",type=int)
p_create.add_argument("b",help="Image depth of blue.",type=int)
p_create.add_argument("width",help="Image width.",type=int)
p_create.add_argument("height",help="Image height.",type=int)
p_create.add_argument("a",help="Image depth of alpha.",type=float,default=1,nargs="?")

args = parser.parse_args()
try:
    if args.command == "text":
        img_fit.text_painting(args.from_img,args.chars,args.output)
    elif args.command == "fitter":
        img_fit.add_fitter(args.from_img,args.fitter_img,args.output_img)
    elif args.command == "latex":
        img_fit.latex2text(args.text,args.output)
    elif args.command == "create":
        img_fit.create_image(args.r,args.g,args.b,args.width,args.height,args.a,args.img)
    elif args.command == "version":
       print(f'version:imgfit {img_fit.__version__}')
except FileNotFoundError as fe:
    print("Error:",fe)
