# Travelling Salesman Problem

The travelling salesman problem is an NP-Hard problem which consist of calculating the shortest total distance to travel between a set of cities, without going twice to the same cities, and returning at the end to the original city.
This python application contains 5 algorithms, with four fast approximations of the problem and one slow exact resolution of the problem.
Created by three developers : Axelle MAZUY, Florian VAN LIEDEKERKE, Etienne BINGINOT

## Installation

To launch the application, you will need python 3.10 installed on your computer.
Then, you can install the dependency with :
```
  pip install matplotlib
  pip install numpy
```

## Usages

You can launch the app with the following command :
```
  python3 main.py
```

The app will then generate for a predeterminate sized (configurable in the file main.py) a matrix, which represent the Euclidian weight matrix for the problem.
Then, the app will calculate the shortest path with each algorithm, showing at the screen a representation of the path. The total weight of the path is also printed.


## License

This project is under [MIT License](https://github.com/Pootouf/Algorithms-Travelling-Salesman-Problem/blob/main/LICENSE)
