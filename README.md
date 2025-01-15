# Tool to convert smiles format data into a format that can be handled by pmopt

## background on this tool and [pmopt][1]
This tool converts compound data in smiles format into a format that can be handled by [pmopt][1].  
[pmopt][1] is a tool developed by our laboratory that can perform pattern mining on a wide variety of data.  
Data converted using this tool can be input directly into [pmopt][1].

[1]:https://github.com/takeuchi-lab/pmopt

## Required Python Packages

- `pysmiles`: Used to read molecular SMILES notation.
- `pandas`: Used for data frame manipulation.
- `networkx`: Used for manipulating network graphs.
- `scikit-learn`: Used for cross-validation of machine learning models (specifically `KFold` from the `model_selection` module).

## Installation Method

Python packages can be installed using `pip`. Please run the following command:

```sh
pip install pysmiles pandas networkx scikit-learn
```

## Usage
Grant execute permission to the following 2 shell scripts.
```sh
chmod +x format_conversion.sh
chmod +x make_cvdata.sh
```

Specify the name of the csv file, the column name of the variable you want to retrieve, the column name where the smiles format data is stored, and the name of the output file and run.
```
./format_conversion.sh smiles_test.csv logp smiles transformed.csv
```

The following shell script can be executed to generate segmented data for use in cross-validation. Specify the file name and the number of divisions and output path.
```
./make_cvdata.sh transformed.csv 5 cvdata
```
