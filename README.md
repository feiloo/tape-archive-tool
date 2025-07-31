# tape-archive-tool

this simple tool enables simple file archiving and retrieval to and from IBM Storage Protect with the dsmc command.

tested only on headless linux/opensuse-leap with python 3.12

### design features

* it does extensive checking and tracks additional metadata to ensure correct archival.
* it is very strict and only archives big normal files and not folders.
* single file

dependencies:

* dsmc
* sha256sum command 
* python standard library

### usage

```
usage: archive_tool.py [-h] {list,archive,retrieve,recall,delete,info} ...

Archive system client utility

positional arguments:
  {list,archive,retrieve,recall,delete,info}
    list                List all archived objects or all in the given paths
    archive             Migrate files to the archive system
    retrieve            Retrieve a copy of an archived object
    recall              Migrate an archived object back to its original path
    delete              Remove an object from the archives
    info                Print archive system information

options:
  -h, --help            show this help message and exit

```

### Notes:

deep folder hierarchies on windows are limited or use an extension: `\\?\`
this doesnt work entirely correctly with window 11 windows explorer. 
this could bite us wrt. windows usage.

tsm also cant directly archive files that have too long of a path, 
