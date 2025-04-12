# digurl

A command-line tool to extract domain from URL and perform dig operations.

## Installation

```bash
pip install digurl
```

## Requirements

- Python 3.7+
- dig command (dnsutils package)

## Usage

Basic usage:
```bash
digurl https://www.example.com
```

With dig parameters:
```bash
digurl https://www.example.com +short
digurl https://www.example.com A +short
digurl https://www.example.com MX +noall +answer
```

## Features

- Extracts domain from URLs
- Supports all dig parameters
- Simple and easy to use

## License

MIT