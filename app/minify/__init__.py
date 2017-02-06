import requests

def css(version):
	cssMin=requests.post("http://cssminifier.com/raw", data={"input":open("content/assets/css/style.css", "r").read()}).text
	open("tmp/build/assets/css/style.min.css", "w+").write(cssMin)
	return 1

def js():
	cssMin=requests.post("http://javascript-minifier.com/raw", data={"input":open("content/assets/js/app.js", "r").read()}).text
	open("tmp/build/assets/js/app.min.js", "w+").write(cssMin)
	return 1
