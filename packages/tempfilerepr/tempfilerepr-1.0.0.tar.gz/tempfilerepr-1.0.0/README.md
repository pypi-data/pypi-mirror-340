![PyPI](https://img.shields.io/pypi/v/tempfilerepr)
![GitHub](https://img.shields.io/github/license/mildmelon/tempfilerepr?style=flat)

# Repri encode/decoder for Python

Encoder and decoder for the [Repri encoding](https://www.kuon.ch/post/2020-02-27-repri/),
python implementation of https://github.com/kuon/java-repri

## Usage

Install with pip:
```
$ pip install tempfilerepr
```

Example:
```python
from tempfilerepr import encode_code_by_lines, tempfilerepr


data = b'my test data'  # Length of bytes must be a multiple of 4

enc_data = encode_code_by_lines(data)
print(enc_data)  # 'G67S97T4WR2XEP4STZYE8'

dec_data = tempfilerepr(enc_data)
print(dec_data)  # bytearray(b'my test data')

assert data == dec_data  # True
```

## License

Licenses under the MIT License (LICENSE-MIT or http://opensource.org/licenses/MIT)
