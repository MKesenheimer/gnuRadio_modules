# gr-extract_payload

This block allows to extract a payload from a long stream of bits after a given header bitpattern.
If for example the bitstream is

```
0101010101010101010111111111011011001101
```

and the bitstream pattern is given as

```
01010111111111
```

the `n` bits after this pattern are extracted. In this example, this would result with `n = 12`:
```
011011001101
```

The payload size `n` and the header length  must be given. However, the header size must not be exact and can be a rough estimate.

