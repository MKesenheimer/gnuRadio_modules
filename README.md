# gnuRadio Modules

A collection of various gnuRadio modules.

* [OOK Demodulator](https://github.com/MKesenheimer/gnuRadio_modules/tree/master/gr-OOK_demodulator): A hierarchy block to demodulate OOK (ASK) signals.
* [Extract Payload](https://github.com/MKesenheimer/gnuRadio_modules/tree/master/gr-extract_payload): A C++ block which allows to extract a payload from a long stream of bits after a given header bitpattern.
* [Find max channel](https://github.com/MKesenheimer/gnuRadio_modules/tree/master/gr-find_max_channel): A C++ block to find the channel with the maximum value.
* [Set variable](https://github.com/MKesenheimer/gnuRadio_modules/tree/master/gr-set_variable): A python block that allows setting a variable at runtime.
* [Manchester decode](https://github.com/MKesenheimer/gnuRadio_modules/tree/master/gr-manchester_decode): Decode a Manchester-encoded bit stream.
* [Manchester encode](https://github.com/MKesenheimer/gnuRadio_modules/tree/master/gr-manchester_encode): Encode a bit stream into a Manchester-encoded bit stream

## Generating modules
```
gr_modtool newmod <name of module>
cd <module>
gr_modtool add -t general -l cpp
