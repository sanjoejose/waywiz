import qrcode

n = "100"  # Data to encode in the QR code
img = qrcode.make(n)  # Generate the QR code
img.save('num5.png')  # Save the QR code as an image file
