# Serendipity Matrix 

The package provides the methods to provide the serendipity matrix and for visualizing the serendipity matrix in a horizontal bar chart. The serendipity matrix is an innovative method to understand the behavior of a prediction model for classification problems. 

This matrix provides information about the degree of certainty that the classifier has in its own predictions, indicating whether it is robust and reliable or uncertain and doubtful. This method has two variants: the class-independent serendipity
matrix and the class-specific serendipity matrix depending on the kind of analysis required. 

By analyzing the data provided by them, our goal is to improve the reliability and explainability of prediction models and to provide users with a clearer understanding of why a model is certain or uncertain about its predictions.

## Installation

Serendipity Matrix can be installed from [PyPI](https://pypi.org/project/serendipity_matrix/)

```bash
pip install serendipity_matrix
```

Or you can clone the repository and run:

```bash
pip install .
```

## Sample usage

```python
from serendipity_matrix import class_indep_matrix, class_spec_matrix, plot_class_spec
from sklearn.naive_bayes import GaussianNB
from ucimlrepo import fetch_ucirepo

# Loads the dataset
wine_quality  = fetch_ucirepo(id=186) 
X, y = wine_quality.data.features, wine_quality.data.targets.squeeze()

# Training and predict
model = GaussianNB().fit(X, y)
result = model.predict_proba(X)

# Calculates and prints the class-independent serendipity matrix
ci_matrix = class_indep_matrix(y, result)
print(ci_matrix)

# Calculates and prints the class-specific serendipity matrix
cs_matrix = class_spec_matrix(y, result)
print(cs_matrix)

# Plots the class-specific serendipity matrix
plot_class_spec(y, result)
```

## Result sample

### Class-independent serendipity matrix

|Reliability|Overconfidence|Underconfidence|Serendipity|
|:---------:|:------------:|:-------------:|:---------:|
|  0.26401  |    0.29623   |    0.318717   |  0.021864 |

### Class-specific serendipity matrix

|CLASS_NAME|Reliability|Overconfidence|Underconfidence|Serendipity|
|:--------:|:---------:|:------------:|:-------------:|:---------:|
|    3     |  0.072567 |  0.493307    |    0.412262   |  0.021864 |
|    4     |  0.054267 |  0.310598    |    0.597766   |  0.037369 |
|    5     |  0.383453 |  0.308486    |    0.198692   |  0.109368 |
|    6     |  0.272532 |  0.264399    |    0.267862   |  0.195207 |
|    7     |  0.227578 |  0.400299    |    0.308644   |  0.063479 |
|    8     |  0.010690 |  0.017746    |    0.902782   |  0.068782 |
|    9     |  0.031477 |  0.137502    |    0.822256   |  0.008765 |

### Class-specific serendipity matrix horizontal bar chart

![Class-specific serendipity matrix](https://github.com/agarcon/Serendipity-Matrix/raw/main/Resources/Example_class-specific_serendipity_matrix_for_wine_dataset.png)


## Citation

The methodology is described in detail in:

[1] J. S. Aguilar-Ruiz and A. García Conde, “”<!-- , Scientific Reports, 14:10759, 2024, doi: 10.1038/s41598-024-61365-z. Also, the mathematical background of the multiclass classification performance can be found in: in IEEE Access.-->