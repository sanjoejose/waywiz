import qrcode

n = "126"  # Data to encode in the QR code
img = qrcode.make(n)  # Generate the QR code
img.save('CS FACULTY ROOM 1.png')  # Save the QR code as an image file

