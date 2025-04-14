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

## Use a custom color distance

As an example, this code shows using a custom color distance to generate a
palette for people with protanopia, a form of color blindness.

**Disclaimer:** This has *not* been tested with color blind users and might not
even correctly assess color differences as seen by protanopes&mdash;it's for
demonstration purposes only!

```python
hpe = np.array([
    [0.4002, 0.7076, -0.0808],
    [-0.2263, 1.1653, 0.0457],
    [0,      0,      0.9182]
])
hpe_inv = np.linalg.inv(hpe)
lms = colorspace("lms", ["long", "medium", "short"])
register_space(lms, *derived_rgb_functions(ciexyz, lms, lambda x: hpe_inv @ x, lambda x: hpe @ x))
```


```python
# Protanopia matrix from https://ixora.io/projects/colorblindness/color-blindness-simulation-research/
protan_matrix = np.array([
    [0, 1.05118294, -0.05116099],
    [0, 1,          0          ],
    [0, 0,          1          ]
])
def protan(x):
    return np.array(lms(*(protan_matrix @ cieluv(*x).to_lms())).to_cieluv())

def protan_dist(a, b):
    a = protan(a)
    b = protan(b)
    return np.linalg.norm(b - a)

cm = ListedColormap([c.to_rgb().safe() for c in glasbey(8, seed=485, color_dist=protan_dist)])
cm
```

![Possibly a color palette optimized for protanopia](images/output_16_0.png)
