import os,shutil,json
from PIL import Image

def generateMedia(pathFrom,pathTo):
	params=json.loads(open('config/media.json', 'r').read())
	os.makedirs('tmp/build/media/'+pathTo,0o777,1)
	for item in os.listdir('content/articles/'+pathFrom+'/media'):
		try:
			im = Image.open('content/articles/'+pathFrom+'/media/'+item)
			im.save('tmp/build/media/'+pathTo+'/full.png', 'PNG')
			width, height = im.size
			for sizeName in params:
				size=params[sizeName]
				try:
					finalWidth=size['width']
					finalHeight=size['height']
					if width<size['width']:
						size['width']=width
						size['height']=int(height*size['width']/width)
					if height<size['height']:
						size['height']=height
						size['width']=int(width*size['height']/height)
					if size['width']>0 and size['height']>0:#int((int((height-size['height'])/2
						thumb = im.crop((int(width/2-size['width']/2),int(width/2-size['height']/2),int(width/2+size['width']/2),int(width/2+size['height']/2)))
					if finalWidth!=size['width'] or	finalHeight!=size['height']:
						thumb = im.resize((finalWidth,finalHeight),resample=Image.LANCZOS)
				except:
					try:
						size['width']
					except KeyError:
						size['width']=int(width*size['height']/height)
					try:
						size['height']
					except KeyError:
						size['height']=int(height*size['width']/width)
					size=(size['width'],size['height'])
					thumb=im.resize(size,resample=Image.LANCZOS)
				thumb.save('tmp/build/media/'+pathTo+'/'+sizeName+'.png', 'PNG')
			return 1
		except Exception as e:
			continue