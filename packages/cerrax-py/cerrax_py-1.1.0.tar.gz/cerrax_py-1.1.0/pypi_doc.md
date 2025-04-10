#  Dot Dictionary


 Makes a Python dictionary that can access keys with dot notation in addition to brackets ( ```[]```).

## ``` class DotDict(dict):```



 A Python dictionary that allows you to access keys in dot notation style.


 **Example:**

```
mycar = DotDict(
    year = 2023,
    make = 'Dodge',
    model = 'Challenger',
    trims = DotDict(
        sport = DotDict(horsepower=256),
        rt = DotDict(horsepower=425),
        demon = DotDict(horsepower=712),
    )
)


 print(mycar.year, mycar['model'], 
         mycar.trims.rt.horsepower, 'hp')

```



 **Output:** ```2023 Challenger 425 hp```


 Attributes can be accessed by dot notation, as well as traditional bracket notation. New attributes can only be added via bracket notation. This essentially creates a dictionary that works like a JavaScript Object.

#  Grid Data Structure


 A data structure to manipulate and traverse a 2-dimensional array in an intutive manner.

## ``` class Grid:```


**Attributes:**

* ```width```: the width of the grid
* ```height```: the height of the grid
* ```focus_xy```: a tuple of coordinates within the grid data indicating the cell which is currently in focus
* ```focus_obj```: the data within the cell which is currently focused
* ```grid```: the raw 2-D array which stores the data


#### ``` def __init__(self, width = None, height = None, default = None, data = None):```

**Parameters:**

* ```width```: the width of the grid
* ```height```: the height of the grid
* ```default```: a default value to insert into empty cells
* ```data```: a 2-D array of data to populate the new grid



 A ```Grid```object is a rectangluar 2-dimensional array, meaning that each row has the same number of columns. The size of this structure can be determined either by the provided ```width```and ```height```, or by the ```data```passed into it. The ```width```and ```height```must be specified unless ```data```has been provided. If ```data```is provided without ```width```or ```height,```the dimensions of the ```data```will be used as the size of the ```Grid```object.

**NOTE:**  The ```data```is assumed to be rectangular as well, and the height and width are determined by the first row and first column, respectively. If any rows below the first row are longer, they will be truncated and that data will not be inserted into the ```Grid```object.



 If both ```data```and the ```width```or ```height```is provided, the appropriate dimension of the grid will be sized according to that value. If the value is greater than the dimension of the ```data```, the ```default```value will be inserted into those cells. If the value is less than the dimension of the ```data```, then those cells will not be copied to the ```Grid```object. (See the ```populate()```method below for more details)

#### ``` def populate(self, data):```

**Parameters:**

* ```data```: a 2-D array of data to populate the grid



 This method fills in the ```Grid```object with the contents of each cell of the provided ```data```object. The insertion to each cell of the ```Grid```object is a simple assignment. This means that literal values will be copies, but Python objects will be references.

**NOTE:**  Because Python always does pass by reference, the assignment which takes place in ```populate()```places a **reference** to any Python object which is in the cell of ```data```. If you wish to have shallow or deep copies in the ```Grid```object, you must do those before passing the ```data```to this method.


#### ``` def check_bounds(self, value, upper, lower, raise_exc=True):```

**Parameters:**

* ```value```: the value to check
* ```upper```: the maximum threshold of ```value```
* ```lower```: the minimum threshold of ```value```
* ```raise_exc```: a boolean indicating if an ```IndexError```should be raised when ```value```exceeds the ```upper```or ```lower```bounds


**Returns:**  The ```value,```possibly adjusted by the bounds, or raise an ```IndexError```



 Usually, this method simply returns the unaltered ```value,```unless it exceeds one or both of the bounds provided ( ```upper```and ```lower```). However, if ```raise_exc```is set to ```False```, then this method will adjust the ```value```to stay within the bounds. If the ```value```exceeds one of the bounds, the method returns the bound itself, since it is the furthest value allowed. This can be useful in situations where you implicitly need the value to stay within the bounds without raising an error.

#### ``` def focus(self, x=None, y=None, stay_in_bounds=False):```

**Parameters:**

* ```x```: the horizontal coordinate to focus on in the grid
* ```y```: the vertical coordinate to focus on in the grid
* ```stay_in_bounds```: a boolean indicating if this method should automatically correct the focus coordinates if the provided ```x```or ```y```values are outside the bounds of the grid


**Returns:**  The content of the cell at ( ```x```, ```y```) in the grid.



 A major concept of the ```Grid```is **focus**, also referred to in some other data structures and data mangement utilities as a "cursor". The focus of the ```Grid```is the specific cell which can be read or manipulated. This method will use the provided ```x```and/or ```y```values to set the focus of the ```Grid```to a specific cell. The coordinate system in use with a ```Grid```object is such that the cell in the top left corner is coordinate (0, 0). and values along the x and y axes are positive integer values. There are no decimal or negative values in a ```Grid```object's coordinates. If the provided ```x```or ```y```values are not within the bounds of the grid, an ```IndexError```will be raised, unless ```stay_in_bounds```is set to ```True```(see below).


 If an ```x```or ```y```value is not provided, this method will use the current focus ```x```or ```y```coordinate. Calling ```focus()```, with no arguments, simply retuns the currently focused cell contents. Calling ```focus(x=2)```would move the focus to the third column of the currently focused row.

**NOTE:**  Keep in mind that the ```Grid```coordinate system starts at (0,0), so the first column is an x-coordinate of 0, not 1.



 If ```stay_in_bounds```is set to ```True```, then this method implicitly limits the focus to the bounds of the grid. Any value outside the bounds, will be automatically corrected to the bound(s) that were crossed. This is useful for implementations that may attempt to exceed the grid bounds, but don't necessarily need to raise an exception when it occurs.

#### ``` def focus_up(self, amount=1, stay_in_bounds=False):```

**Parameters:**

* ```amount```: the number of cells to shift the focus upwards
* ```stay_in_bounds```: a boolean indicating if this method should automatically correct the focus coordinates if it is outside the bounds of the grid


**Returns:**  The content of the cell that is ```amount```number of cells above the currently focused cell.



 This a convenience method which shifts the focus of the ```Grid```object upwards by an ```amount.```It directly calls the ```focus()```method (see above).

#### ``` def focus_down(self, amount=1, stay_in_bounds=False):```

**Parameters:**

* ```amount```: the number of cells to shift the focus downwards
* ```stay_in_bounds```: a boolean indicating if this method should automatically correct the focus coordinates if it is outside the bounds of the grid


**Returns:**  The content of the cell that is ```amount```number of cells below the currently focused cell.



 This a convenience method which shifts the focus of the ```Grid```object downwards by an ```amount.```It directly calls the ```focus()```method (see above).

#### ``` def focus_left(self, amount=1, stay_in_bounds=False):```

**Parameters:**

* ```amount```: the number of cells to shift the focus to the left
* ```stay_in_bounds```: a boolean indicating if this method should automatically correct the focus coordinates if it is outside the bounds of the grid


**Returns:**  The content of the cell that is ```amount```number of cells to the left of the currently focused cell.



 This a convenience method which shifts the focus of the ```Grid```object to the left by an ```amount.```It directly calls the ```focus()```method (see above).

#### ``` def focus_right(self, amount=1, stay_in_bounds=False):```

**Parameters:**

* ```amount```: the number of cells to shift the focus to the right
* ```stay_in_bounds```: a boolean indicating if this method should automatically correct the focus coordinates if it is outside the bounds of the grid


**Returns:**  The content of the cell that is ```amount```number of cells to the right of the currently focused cell.



 This a convenience method which shifts the focus of the ```Grid```object to the right by an ```amount.```It directly calls the ```focus()```method (see above).

#### ``` def replace_focused(self, newitem):```


 Replaces the item currently in focus with ```newitem```.

**Parameters:**

* ```newitem```: the data to replace the currently focused item in the grid


#### ``` def typewriter_traverse(self):```

**Returns:**  a ```TypewriterGridIterator```for use in a ```for```loop


#### ``` def serpentine_traverse(self):```

**Returns:**  a ```SerpentineGridIterator```for use in a ```for```loop


#### ``` def vertical_typewriter_traverse(self):```

**Returns:**  a ```VerticalTypewriterGridIterator```for use in a ```for```loop


#### ``` def vertical_serpentine_traverse(self):```

**Returns:**  a ```VerticalSerpentineGridIterator```for use in a ```for```loop


#### ``` def spiral_in_traverse(self):```

**Returns:**  a ```SpiralInGridIterator```for use in a ```for```loop


## ``` class AbstractGridIterator:```



 An abstract class for deriving iterators for a ```Grid```object.


 ```GridIterator```classes are unique in that they don't simply return the content of the cell, they also return the x and y coordinates of the cell. When using a ```GridIterator```, you must account for these extra values:

```
mygrid = Grid(24, 12)
for x, y, item in mygrid.typwriter_traverse():
   # do stuff

```


## ``` class TypewriterGridIterator(AbstractGridIterator):```



 "Typewriter" traversal is the most common way to traverse a 2-dimensional array. The iterator starts at (0, 0), and moves along the x-axis. When it reaches the end of the row, it goes down to the next row, and begins again at the 0 x-coordinate and travels along the x-axis.


 **Example:**

```
1234
5678    typwriter
9000    traversal = 123456789000

```


## ``` class SeprentineGridIterator(AbstractGridIterator):```



 "Serpentine" traversal is another fairly common traversal method. The iterator starts at (0, 0), and moves along the x-axis, just like a typewriter traversal. However, when it reaches the end of the row, it simply changes direction after moving down a row.


 **Example:**

```
1234
5678    serpentine
9000    traversal = 123487659000

```


## ``` class VerticalTypewriterGridIterator(AbstractGridIterator):```



 "Vertical Typewriter" traversal is the same as typewriter, except turned vertically. Starting at (0, 0), the iterator moves down the column. When it reaches the end of the column, it goes to the next one and, starting again at the 0 y-coordinate, traverses down teh column.


 **Example:**

```
1234    vertical
5678    typewriter
9000    traversal = 159260370480

```


## ``` class VerticalSeprentineGridIterator(AbstractGridIterator):```



 "Vertical Serpentine" traversal is the same as serpentine, except turned vertically. Starting at (0, 0), the iterator moves down the column. When it reaches the end of the column, it changes direction, and traverses up the next column.


 **Example:**

```
1234    vertical
5678    serpentine
9000    traversal = 159062370084

```


## ``` class SpiralInGridIterator(AbstractGridIterator):```



 "Spiral In" traversal is concerned with visiting the outermost cells of the grid before visiting those closer to the center. The iterator starts at (0, 0), and moves along the x-axis. However, upon reaching the end of the x-axis, it moves down the column, then backwards across the bottom row, and upwards towards the start. Upon reaching the start, the iterator moves down 1 row and does the same movement again, 1 "layer" deeper (and thus 1 unit closer to the center) than before. This continues until it reaches the center of the grid.


 **Example:**

```
1234
5678    spiral in
9000    traversal = 123480009567

```


#  Indented Text File Reader


 Utility for reading indented blocks of text from a file and forming a tree data structure for use in Python. This allows Python programs to use config files and data files which respect whitespace the same as Python itself.

## ``` class IndentReader:```


**Attributes:**

* ```filepath```: path to the file this reads
* ```node_class```: the Python class this uses for its nodes (default is the ```Node```class below)
* ```preserve_newlines```: boolean describing if the reader keeps newlines in the node ```data```
* ```allowed_indents```: a string of characters which are considered valid indentations
* ```indent_char```: the character or string the reader has identified for use as indentation in the current file
* ```current_line```: the current line number the reader is parsing
* ```root```: the root node of the tree data structure generated by the reader


#### ``` def __init__(self, filepath, node_class = None, preserve_newlines = False, allowed_indents = ' \t', root_data='<root>'):```

**Parameters:**

* ```filepath```: path to the file this reads
* ```node_class```: the Python class this uses for its nodes (default is the ```Node```class below)
* ```preserve_newlines```: boolean describing if the reader keeps newlines in the node ```data```
* ```allowed_indents```: list of strings which are considered valid indentations
* ```root_data```: default ```data```placed in the root node



 When an ```IndentReader```object is instantiated, it will immediately attempt to read and parse the file. Once ```IndentReader```identifies a valid indent string (via the ```allowed_indents```value), all indents must use that same character or string for their indentation (just like Python, you cannot mix tabs and spaces for indentation).


 The completed data structure is available for direct consumption via the ```root```attribute. In the event that an error occurs during parsing, the reader raises a ```ReaderError```. The exception message indicates the error and line number. The ```root```data structure, ```current_line```, and ```indent_char```remain after parsing is complete in order to provide debug information, if necessary.


 This class can be subclassed to create a specialized reader for specific file formats or use cases. Typically the only override needed is to change the ```parse_data()```method to use logic that is specific to the use case desired. You may also want to provide a different ```node_class```for this reader (see the ```Node```class below).

#### ``` def prepare_for_read(self):```


 Resets all variables to prepare to read a new file.

#### ``` def read_file(self):```


 Reads and parses the file of ```filename```and stores the result in the ```root```attribute. This method is automatically called upon object instantiation.

#### ``` def parse_line(self, line):```

**Parameters:**

* ```line```: the raw line of text read from the file



 Parses the line, identifies the indentation level, then creates a node and inserts it into  the tree.

#### ``` def find_node(self, indent):```

**Parameters:**

* ```indent```: the indent string to match


**Returns:**  The parent node which matches the ```indent```provided



 Starting at the current node, this method traverses back up the parents to find the indentation level that matches, then returns the parent node of that indentation level. If no matching node is found, this raises a ```ReaderError```.

#### ``` def prepare_node(self, rawline, indent):```

**Parameters:**

* ```rawline```: the raw line of text from the file
* ```indent```: the indentation string found on the line


**Returns:**  a new ```Node```object with the ```indent```and ```data```parsed from the ```rawline```



 This method calls the ```parse_data()```method to assemble the data for the ```Node```object.

#### ``` def parse_data(self, line, rawline):```

**Parameters:**

* ```line```: the stripped line
* ```rawline```: the untouched raw text from the file


**Returns:**  Any valid Python data to store in the ```data```of a ```Node```object.



 This method should be overridden in any subclasses to provide more specific logic to parse and prepare data read from the file. By default, this method just returns the ```line```value.

#### ``` def output(self, exclude_root=False):```

**Parameters:**

* ```exclude_root```: do not include the ```root```node in the output string


**Returns:**  A prettified string of the data structure stored within ```root```.


## ``` class ReaderError(Exception):```



 A generic exception class for ```IndentReader```.

## ``` class Node:```


**Attributes:**

* ```parent```: the parent ```Node```of this node
* ```indent```: the indentation string this node's ```data```was found at in the file
* ```level```: the indent level of the node (root level is 0)
* ```child_indent```: the indentation string of this node's ```children```
* ```children```: a list of child ```Node```objects
* ```data```: the data stored in this node



 The tree data structure in the ```IndentReader```is formed by connecting ```Node```objects to each other as parents and children. Each node has 1 parent and 0 or more children.


 This class can be used to derive subclasses in order to customize the behavior of individual nodes of the ```IndentReader.```Provide the subclass to the ```node_class```parameter of the ```IndentReader```constructor.

#### ``` def __init__(self, parent=None, indent='', data=''):```

**Parameters:**

* ```parent```: the parent ```Node```object
* ```indent```: the indentation string this node's ```data```was found at in the file
* ```data```: the data stored in this node


#### ``` def add_child(self, node):```

**Parameters:**

* ```node```: the ```Node```object to add as a child



 This method sets the ```child_indent```attribute, adds the ```node```to this node's ```children```, and assigns this node as the ```parent```or ```node```.

#### ``` def output(self, level=0, exclude_self=False):```

**Parameters:**

* ```level```: indicates how far the prettified data should be indented
* ```exclude_self```: do not include the ```data```in the output string


**Returns:**  A prettified string of the ```data```and ```children```of this node


#  Indexed Object


 A chimera of data structures, this object is an ordered, indexed hashtable with the ability to access attributes by both dot notation and bracket notation.

## ``` class IndexedObject():```



 This object provides the benefits of several data structures simultaneously.


 **Attribute Access**

* Dot notation - ```myobj.attr```
* Bracket notation (key) - ```myobj['attr']```
* Bracket notation (index) - ```myobj[2]```
* Built-in ```getattr()```function - ```getattr(myobj,```'attr', None)
* Instance ```get()```method - ```myobj.get('attr',```None)
* Can use ```len()```to get number of attributes



 **Attribute Storage**

* Attributes are ordered
* Attributes can change order
* New attributes can be inserted at any index
* Keys, values, and key-value pairs can be iterated in order
* Can handle both keyed and keyless data in the same object


#### ``` def __init__(self, *args, **kwargs):```


 Creates a new ```IndexedObject```. This constructor creates the attributes differently based on the ```args```or ```kwargs```supplied to it. The constructor **cannot** accept both ```args```and ```kwargs```together. The object must be instantiated with either only ```args,```or only ```kwargs.```All attributes will be inserted into the object in the order they are passed to the constructor.


 If ```arg```values are tuples, it is assumed they are ```(key, value)``` tuples, and will assign attributes as such. Any other ```arg```values are considered keyless values, and will have an automatically generated key assigned to them. ```kwargs```are inserted exactly they are passed, with the attribute name being the ```kwarg```name, and the value being the ```kwarg```value. Because the ```args```can be read as either key-value tuples, or keyless values, you can get around the ```arg```& ```kwarg```limitation by inserting keyword args as key-value tuples instead.


 Keyless data is always given an automatically generated key anytime it is inserted into this object. Generated keys follow the pattern of ```_x_```where ```x```is an auto-incrementing counter that starts at zero. The increment is based on the lifetime of the object. For example, an ```IndexedObject```with 8 keyless attributes has a previously generated key of ```_7_```. If a new keyless attribute is added, this will increment to ```_8_```. However, if a keyless attribute is removed, the generated key does not decrement.

**NOTE:**  Objects which will frequently change the number of keyless attributes should not use ```IndexedObject```, since there is a possibility of encountering the upper bounds of Python's built in ```int```type (typically 2,147,483,647 for most Python interpreters).


#### ``` def get(self, key, default=None):```

**Parameters:**

* ```key```: the attribute name to retrieve
* ```default```: the value to return if the ```key```is not found


**Returns:**  The attribute indentified by ```key```, or the ```default```value if the key is not found


#### ``` def keys(self):```

**Returns:**  A list of the keys in this object, in order.


#### ``` def values(self):```

**Returns:**  A list of the values in this object, in order.


#### ``` def items(self):```

**Returns:**  A list of the ```(key, value)``` tuples in this object, in order.


#### ``` def index(self, key):```

**Parameters:**

* ```key```: the key to search for


**Returns:**  The index of a given ```key```.


#### ``` def insert(self, index, arg1, arg2=None):```

**Parameters:**

* ```index```: the index to insert the attribute
* ```arg1```: either the value, or the key to insert
* ```arg2```: the value to insert


* To insert keyless data: ``` myobj.insert(2, value) ```
* To insert keyed data:   ``` myobj.insert(2, key, value) ```


#### ``` def append(self, arg1, arg2=None):```

**Parameters:**

* ```arg1```: either the value, or the key to append
* ```arg2```: the value to append


* To append keyless data: ``` myobj.append(value) ```
* To append keyed data:   ``` myobj.append(key, value) ```


#### ``` def popindex(self, index):```

**Parameters:**

* ```index```: index of the attribute to remove


**Returns:**  A tuple of the key and value at the ```index```


#### ``` def pop(self, key=None):```

**Parameters:**

* ```key```: key of the attribute to remove


**Returns:**  A tuple of the index and value at the ```key```


#### ``` def extend(self, new_obj):```

**Parameters:**

* ```new_obj```: a ```list```, ```dict```, or ```IndexedObject```to append to this object



 Appends all of the attributes of ```new_obj```to this object. The attributes will be appended in order with the same keys. If duplicate keys are detected, a ```KeyError```is raised. When ```new_obj```is a ```list```, each value will have a key auto-generated before being appended.

**NOTE:**  Because duplicate keys are not allowed, using ```extend()```with an ```IndexedObject```that has keyless attributes will most likely cause a ```KeyError```to be raised.


#### ``` def reverse(self):```


 Reverses the order attributes in place.

#### ``` def copy(self):```

**Returns:**  A shallow copy of this object.


#### ``` def clear(self):```


 Removes all attributes from this object and resets the generated key to zero.

