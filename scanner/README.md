# Scanner
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/mit)
[![openCV version](https://img.shields.io/badge/openCV-%3E%3D%204.2-green)](https://img.shields.io/badge/openCV-%3E%3D%204.2-green)  
A script to extract document from an image and make a scanner like render

## How to use
Specify a file with a document on it:
```sh
# option: --color, --pdf (not implement yet)
python3 scanner.py [option] test/doc_normal.jpg
```

## How it works

* Read image
* Transform into grayscale
* Extract the document by apply a threshold
* Find contour and fix the picture perspective
* Render in color or black and white

![processing](screenshot/processing.png)