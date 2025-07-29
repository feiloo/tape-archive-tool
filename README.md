# tape-archive-tool

this simple tool enables simple file archiving and retrieval to and from IBM Storage Protect with the dsmc command.

it does extensive checking and tracks additional metadata to ensure correct archival.

it is very strict and only archives big normal files and not folders.


### Notes:

deep folder hierarchies on windows are limited or use an extension: `\\?\`
this doesnt work entirely correctly with window 11 windows explorer. 
this could bite us wrt. windows usage.

tsm also cant directly archive files that have too long of a path, 
