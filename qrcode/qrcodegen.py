import qrcode
n="1000"
img=qrcode.make(n)
img.save('num1.png')