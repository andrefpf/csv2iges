# CSV TO IGES
This is a small python project meant to be used as a conversor from csv to iges.

## How to install it
You can wait I put it in pipy, or download this repository and use it directly.

## How to use it 
if you just want to convert something just type the following command in a terminal:
```
python csv2iges yourfile.csv
```
Obviously you need to have python installed in your machine.

If you want to use as a library, just write something like this in your python code:
```
import csv2iges

f = csv2iges.from_csv('yourfile.csv')
f.write_file('output.iges')
```

A third case is if your name is Olavo, so you must like the option --olavo. Just type
```
python csv2iges yourfile.csv -o outputfile.iges --olavo
```

## CSV structure
This project targets a very specific type of csv file like the following one:
```
1, point, 0.0, 0.0, 0.0
2, point, 1.0, 1.0, 1.0
3, line , 1, 2
```
It creates a line between two points with the coordinates (0,0,0) and (1,1,1) respectively.

if "points" or "line" isn't a descriptive enought name for you, you can specify other types. Checkout the Args section 

## Args
This is the structure of the command
```
python csv2iges yourfile.csv [options]
```
The options you can use in options section are the following:
- -h: Provides a help message
- -o arg: Let you wish the name of the output file. 
- -p arg: Let you choose the label to look for in the file to find the points.
- -l arg: Let you choose the label to look for in the file to find the lines.
- -s arg: Let you choose witch separator are you using in your csv file (usually "," but you can use ";" or anything your creative mind let you think).
- --olavo: A set of parameters designed for Olavo.
