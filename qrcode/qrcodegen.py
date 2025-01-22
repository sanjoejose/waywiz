import qrcode

n = "148"  # Data to encode in the QR code
img = qrcode.make(n)  # Generate the QR code
img.save('hod_it.png')  # Save the QR code as an image file

