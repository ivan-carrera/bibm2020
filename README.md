# A Representation Method for Cellular Lines based on SVM and Text Mining

## Iván Carrera, Ines Dutra, and Eduardo Tejera
### Departamento de Informática y Ciencias de la Computación, Escuela Politécnica Nacional. Quito, Ecuador.
### Departamento de Ciencia de Computadores, Universidade do Porto, Portugal.
### Grupo de Quimio-Bioinformática, Universidad de Las Am´ericas. Quito, Ecuador.

### Programa de Doutoramento em Ciência de Computadores FCUP.

#### Abstract.
One major problem in Bioinformatics is the discovery of new cell line interactions with chemical compounds. Computational methods for cell-line screening are fundamental to optimize cost and time in the drug discovery processes. However, in order to build these methods, we need a computational representation for cell lines. Current methods for modeling cell line interactions rely on comparing genetic expression profiles, but these are usually unknown.

In this work we propose a method to characterize and represent cell lines by text processing the scientific literature. We collect abstracts of scientific papers about cellular lines from Cellosaurus and PubMed. These documents are then represented as TF-IDF vectors. We build a data set for classification with the document vectors having the cell line identifier as the target class. We then apply a multiclass SVM classification method. We use Support Vector Domain Description to describe and characterize each cell line with its corresponding hyperplane obtained with a one-vs-rest training. We evaluated several configurations of classifiers, using micro-averaged precision as metric to choose the best classifier, and were able to characterize a set of 300+ cellular lines.

#### Keywords: Machine Learning · Bioinformatics · Text mining
