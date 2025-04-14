# glasbeyish

This is a library that implements a method described in the paper "Colour
Displays for Categorical Images" by Glasbey et al. for finding optimal distinct
color palettes of a specified size.

Unlike the [glasbey](https://github.com/lmcinnes/glasbey) library, this library
implements the simulated annealing method described in the paper rather, than
the iterative method. The simulated annealing method can often give better color
palettes at the expense of longer run times.

## Examples

These examples can also be found in the `examples.ipynb` Jupyter notebook.

```python
import numpy as np
from nice_colorsys import rgb
from glasbeyish import glasbey
from matplotlib.colors import ListedColormap
```

### Generate a palette with 2 colors


```python
cm = ListedColormap([c.to_rgb() for c in glasbey(2)])
cm
```

![Two color colormap](images/output_2_1.png)


### Generate a palette with 12 colors


```python
cm = ListedColormap([c.to_rgb() for c in glasbey(12)])
cm
```

![Twelve color colormap](images/output_4_0.png)


### Use a seed for reproducibility


```python
cm = ListedColormap([c.to_rgb() for c in glasbey(12, seed=485)])
cm
```

![Twelve color colormap, created with seed 485](images/output_6_0.png)


```python
cm = ListedColormap([c.to_rgb() for c in glasbey(12, seed=485)])
cm
```

![The same twelve color colormap, created with seed 485](images/output_7_0.png)



### Limit the colors that can be generated

Here, we'll try to make a bluish color palette by discarding colors too far from
blue. 


```python
def color_dist(a, b):
    return np.linalg.norm(np.array(a.to_cieluv()) - np.array(b.to_cieluv()))

cm = ListedColormap([c.to_rgb() for c in glasbey(12, seed=485, limit=lambda x: color_dist(x, rgb(0, 0, 1)) < 100)])
cm
```

![Bluish color map](images/output_9_0.png)



### Use a custom random color generator

In this example, we'll generate random colors with only blue components in the
RGB color space. `glasbey` expects the generated colors to be in the CIELUV
color space and won't automatically convert the colors from RGB to CIELUV for
us, so we have to do that ourselves. 


```python
rng = np.random.default_rng()
```


```python
def random_color(rng):
    return rgb(0, 0, rng.random()).to_cieluv()
    
cm = ListedColormap([c.to_rgb().safe() for c in glasbey(12, seed=485, random_color=random_color)])
cm
```

![Blue color map](images/output_12_0.png)

