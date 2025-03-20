import qrcode

n = "https://docs.google.com/forms/d/e/1FAIpQLSdemVa98tUnbmVM-uTWCCaweD_fL8ZF4WuY620E0fjWruPn1A/viewform"  # Data to encode in the QR code
img = qrcode.make(n)  # Generate the QR code
img.save('Vote.png')  # Save the QR code as an image file

