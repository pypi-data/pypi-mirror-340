# pyCony
pyCone is a small utility package for python projects debugging, reverse engineering and tracing 

## Installation
```shell
pip install pyCony  
#    OR 
pip install pip install git+https://github.com/rzbhatti/pyCony.git
```
## Usage
```python
from pycony import *
```


## Functions
- open_console()
- print_stack(depth=None)
- pickle_args(n, pkl_sufix=None, file_path=None)
- print_stack(depth=None)
- load_pickled_args(file_path)
- open_console_print_stack(depth=None)
- **[Optional]** set_trace() --> https://docs.python.org/3/library/pdb.html

# Example
```python 
from pycony import open_console_show_stack_depth

def my_function(arg):
    value = arg * 5
    print(f"Inside my_function with value: {value}")
    open_console_print_stack(depth=2)
    print("Back in my_function")

my_function(10)
```


