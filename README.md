# tape-archive-tool


# Notes:

deep folder hierarchies on windows are limited or use an extension: `\\?\`
this doesnt work entirely correctly with window 11 windows explorer. 
this could bite us wrt. windows usage.

tsm also cant directly archive files that have too long of a path, 
but suspicously it allows it when theyre archived as subfolders instead of directly.

tsm asks interactively 

stackoverflows answer:
"yes | dsmc retrieve "/data/folder_1/" folder1/"
doesnt work and spams the tool.
it answers:
`The character '#' stands for any decimal integer.The only valid responses are characters from this set: [1, 2, 3, 4, A]`


Abort the replacing results in code 8
