from PIL import Image

'''
	Resizes and overwrites an image
'''
def resize_image(path, width, height):
	image = Image.open(path)
	image = image.resize((64, 64))
	image.save(path)
