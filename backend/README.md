### Usage

### Program assumption

1. Input file is expected to follow NIM12 specification. Invalid file is not handled and will throw error
2.

### Speed vs. Security

Generating SQL comes with risk of SQL injection if it's not carefully designed. For this case I'm using (PyPika)[https://github.com/kayak/pypika]. However due to the processing load that comes with sanitizing, this library is significantly slower than generating string. So, for demo purposes I enable an option to turn off sanitizing.

### Performance optimisation

As per the problem statement, this software can handle CSV file up to 1 GB. It is expected that the insert statement generated will be larger than 1GB. To avoid storing all the results in the memory resulting in Out Of Memory, the CSV file is processed in batches, with output incrementally written to the disk for each processed chunk.

To generate a mock file:

```python
python3 -m app generate_file
```

Take note that

### Testing
