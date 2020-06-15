# CellChar: A SVM-based characterization method for cellular lines using text processing

## Iván Carrera, Ines Dutra, and Eduardo Tejera
### Departamento de Informática y Ciencias de la Computación, Escuela Politécnica Nacional. Quito, Ecuador.
### Departamento de Ciencia de Computadores, Universidade do Porto, Portugal.
### Grupo de Quimio-Bioinformática, Universidad de Las Am´ericas. Quito, Ecuador.

### Programa de Doutoramento em Ciência de Computadores FCUP.

#### Abstract.
Cellular lines are an important tool for research in drug discovery. Computational prediction of cell line interactions with candidate drug chemical compounds is a fundamental step to improve and optimize _in vitro_ assays in the drug discovery processes.
One of the main problems of in silico prediction of cell line interactions with chemical compounds is the computational representation of cellular lines. Methods for QSAR modeling of cell line interactions compare genetic expression profiles. However, gene expression of cell lines is usually unknown. CellChar is a SVM-based characterization method for cellular lines. We obtain a representation for cell lines from text mining the scientific literature.
We use two main knowledge sources: Cellosaurus, a knowledge resource on cell lines, and PubMed, a database of the NIH biomedical literature. We retrieve and analyze the scientific literature, then classify the scientific papers according to the cell lines they relate to, and afterwards, obtain a description of the cell line.
We have been able to successfully characterize a set of cellular lines. We evaluate several configurations of linear Support Vector Classifiers, using micro-averaged precision as metric to choose the best classifier. Data and software are available for experimental reproducibility.

#### Keywords: Knowledge representation · Document classification · Machine Learning · Bioinformatics · Drug Discovery
