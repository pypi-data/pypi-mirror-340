# glasbeyish

This is a library that implements a method described in the paper "Colour
Displays for Categorical Images" by Glasbey et al. for finding optimal distinct
color palettes of a specified size.

Unlike the [glasbey](https://github.com/lmcinnes/glasbey) library, this library
implements the simulated annealing method described in the paper rather, than
the iterative method. The simulated annealing method can often give better color
palettes at the expense of longer run times.

## Examples

Generate a color palette with two colors.

```python
from glasbey import glasbey
from matplotlib.colors import ListedColorMap

cm = ListedColorMap([c.to_rgb() for c in glasbey(2)])
```

Generate a color palette with twelve colors.

```python
cm = ListedColorMap([c.to_rgb() for c in glasbey(12)])
```

Provide a random seed for reproducibility.

```python
cm = ListedColorMap([c.to_rgb() for c in glasbey(12, seed=485)])
cm2 = cm = ListedColorMap([c.to_rgb() for c in glasbey(12, seed=485)])
assert cm1 == cm2
```
