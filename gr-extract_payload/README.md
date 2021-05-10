# gr-extract_payload

This block allows to extract a payload from a long stream of bits after a given header bitpattern.
If for example the bitstream is

```
010101010101010101011111111101101100110
```

and the bitstream pattern is given as

```
01010111111111
```

the `n` bits after this pattern are extracted.

The payload size `n` and the header length  must be given. However, the header size must not be exact and can be a rough estimate.

