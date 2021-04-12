# christmas-light-finder
Identifies the bright lights on an image of a Christmas tree through filtering and clustering, counts the number of lights

<img width="50%" height="50%" src="https://github.com/tyler-pruitt/Christmas-Light-Finder/blob/main/Christmas.jpg?raw=true">

Filters the image into red, green, and blue. Since green seems to be the most vibrant image of the three, filter and cluster the green image.

<img width="50%" height="50%" src="https://github.com/tyler-pruitt/Christmas-Light-Finder/blob/main/red.png?raw=true">

<img width="50%" height="50%" src="https://github.com/tyler-pruitt/Christmas-Light-Finder/blob/main/green.png?raw=true">

<img width="50%" height="50%" src="https://github.com/tyler-pruitt/Christmas-Light-Finder/blob/main/blue.png?raw=true">

Since green seems to be the most vibrant image of the three, filter and cluster the green image.

With pixel threshold set to 240 (out of 255) and the minimum island size set to 100,
number of lights = 88.
