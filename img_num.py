import matplotlib.pyplot as plt
import image_to_numpy
# Load your image file
img = image_to_numpy.load_image_file("./img/under.jpg")
# Show it on the screen (or whatever you want to do)
plt.imshow(img)
plt.show()