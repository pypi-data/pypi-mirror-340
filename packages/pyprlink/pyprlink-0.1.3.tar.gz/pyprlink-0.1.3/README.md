# PyPrLink

A TCP/IP client for communicating with PrairieView.
Alternate for PrairieLink Application from Python. 
Python-PrairieLink (PyPrLink)

## Installation

```bash
pip install pyprlink
```

## Usage

### As a Python Module
```python
from pyprlink.tcp_client import ask_PV
# Send commands to PrairieView
ask_PV('-gmp', 'x')  # Get motor position for X-stage
ask_PV('-pg', '3', '400')  # Set PMT Gain on Channel 3 to 400
```
### From Command Line
After installation, you can use the `pypr` command directly:
```bash
pypr -gmp x
pypr -pg 3 400
```

## Development
Install development dependencies:
```bash
pip install -e ".[dev]"
```
Run tests:
```bash
pytest
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.
