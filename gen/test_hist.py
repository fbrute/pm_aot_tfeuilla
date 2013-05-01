import matplotlib.pyplot as plt
from numpy.random import normal
#gaussian_numbers = normal(size=1000)
gaussian_numbers = [1,1,2,3,4,4,4,3,1.01,4.4,4.5,5]
plt.hist(gaussian_numbers)
plt.title("Gaussian Histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()
