# saved_instance



## About

SavedInstance is a persistent Python dictionary. It allows you to store and retrieve data based on key and value in a dictionary format.


## Introduction

SavedInstance is:

 - **Just dict**: For accessing or modifying data, there are no separate methods,  you can work with the same way as a dictionary.
 - **Flexi type**: SavedInstance can store all python types and custom user defined class
 - **Inbuilt secure**:  Provides a functionality to store the data in encrypted format, it automatically encrypts the data and decrypts it on demand.
 - **Thread safe**: Designed to work reliably in multi-threaded and multi-processing environments.

## Example
Alice.py
```
Alice.py

from saved_instace import simple_storage

simple_storage = simple_storage()

# writing
simple_storage["message"] = "Hello World"

```
Bob.py
```
Bob.py

from saved_instance import simple_storage

simple_storage = simple_storage()

# Reading
print(simple_storage["message"])

```

## Getting Started

### Install

```
pip install saved_instance
```

### Config
```
svd config init --project-name your-project-name
```
Run above the command in root of your project

## License
MIT