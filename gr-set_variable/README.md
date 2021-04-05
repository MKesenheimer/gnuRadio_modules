# gr-set_variable

This is a block which takes a number as input and sets a previously defined variable.
This can be used if a variable needs runtime adjustment, for example a variable of
a low-pass filter etc.

The variable which should be adjusted during runtime needs to exist.

The output of the block states if the variable was updated or not.
If the output is not needed, one can connect a null sink to it.
