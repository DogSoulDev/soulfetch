# Convert soul1.png to soulfetch_icon.ico using Pillow
from PIL import Image

png_path = 'assets/soul1.png'
ico_path = 'assets/soulfetch_icon.ico'

img = Image.open(png_path)
img.save(ico_path, format='ICO', sizes=[(256,256), (128,128), (64,64), (32,32), (16,16)])
print(f'Converted {png_path} to {ico_path}')
