[![build status](https://gitlab.com/abusix/ahocorapy/badges/master/build.svg)](https://gitlab.com/abusix/ahocorapy/commits/master)
[![coverage report](https://gitlab.com/abusix/ahocorapy/badges/master/coverage.svg)](https://gitlab.com/abusix/ahocorapy/commits/master)

# ahocorapy - Fast Many-Keyword Search in Pure Python

ahocorapy is a pure python implementation of the Aho-Corasick Algorithm.
Given a list of keywords one can check if at least one of the keywords exist in a given text in linear time.


## Basic Usage:

### Creation of the Search Tree

```python
kwtree = KeywordTree(case_insensitive=True)
kwtree.add('malaga')
kwtree.add('lacrosse')
kwtree.add('mallorca')
kwtree.add('mallorca bella')
kwtree.finalize()
```

### Searching

```python
result = kwtree.search('My favorite islands are malaga and sylt.')
print result
```

Prints :
```python
('malaga', 24)
```

The search method always returns the first keyword found, or None if there is none.

```python
result = kwtree.search('crossing on mallorca bella')
print result
```

Prints :
```python
('mallorca', 12)
```
and not 'mallorca bella'. Since 'mallorca' is a strict prefix of it.

## Drawing Graph

You can print the underlying graph with the Visualizer class.
This feature requires a working pygraphviz library installed.

```python
from ahocorapy_visualizer.visualizer import Visualizer
visualizer = Visualizer()
visualizer.draw('readme_example.png', kwtree)
```

The resulting .png of the graph looks like this: 

![graph for kwtree](img/readme_example.png "Keyword Tree")

