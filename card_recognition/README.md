# Playing cards recognition
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/mit)
[![openCV version](https://img.shields.io/badge/openCV-%3E%3D%204.2-green)](https://img.shields.io/badge/openCV-%3E%3D%204.2-green)  
A script to recognize playing cards

## How to use

Test the detection:
```sh
python3 card.py test/cards_01.png
```
You will obtain something like this:  
![result](screenshot/result.png)

## How it works

* Generate the values and symbols set
* Find contour to get separated value and symbol
* Find all the card on the image
* Extract the top left corner of each card
  * For each value and symbol of card, compare it with the values and symbols set
  
At this step, the behavior is the same as the [digit_recognition](../digit_recognition#how-it-works) behavior