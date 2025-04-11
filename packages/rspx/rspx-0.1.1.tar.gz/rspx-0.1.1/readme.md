# rust extension for python

## Installation

```bash
pip install rspx

# or
uv add rspx
```

## Usage

```python
import rspx


def main():
    print(f"rs module: {rspx.__all__}")
    print(f"rs doc: {rspx.__doc__}")
    print(f"rust sum: {rspx.sum(1, 1)}")
    print(f"rust fib: {rspx.fib(10)}")


if __name__ == "__main__":
    main()

```

## Development

### build

```ruby
task rs:b

# or 
task build

# task build:pyo3
```

### publish

```ruby
# publish to pypi
task rs:up

# or
task up
```
