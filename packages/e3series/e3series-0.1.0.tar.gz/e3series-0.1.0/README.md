# Python wrapper for the E3.series COM interface

python e3series is a wrapper library for the E3.series COM interface.
The library enhances the automatic code completion and static program verification for python programs that automate E3.series.

This library requires a working instance of the software Zuken E3.series.

## Getting Started

Install the library via pip:
```
pip install e3series
```

Use the library:
```python
import e3series as e3

app = e3.Application()
app.PutInfo(0, "hello, world!")
```

