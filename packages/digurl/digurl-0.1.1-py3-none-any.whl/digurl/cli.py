#!/usr/bin/env python3
import argparse
import subprocess
from urllib.parse import urlparse
import sys
from typing import List, Optional

def extract_domain(url: str) -> str:
    """Extract domain from URL."""
    parsed = urlparse(url)
    if not parsed.netloc:
        # If no netloc, the entire url might be the domain
        return url.split('/')[0]
    return parsed.netloc

def run_dig(domain: str, args: List[str]) -> None:
    """Run dig command with given domain and arguments."""
    cmd = ['dig'] + args + [domain]
    try:
        process = subprocess.run(cmd, check=True)
        sys.exit(process.returncode)
    except subprocess.CalledProcessError as e:
        print(f"Error running dig: {e}", file=sys.stderr)
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("Error: 'dig' command not found. Please install dig (dnsutils package).", 
              file=sys.stderr)
        sys.exit(1)

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Extract domain from URL and perform dig operation'
    )
    parser.add_argument('url', help='URL to extract domain from')
    parser.add_argument('dig_args', nargs='*', 
                       help='Additional arguments to pass to dig')
    
    args = parser.parse_args()
    
    # Extract domain from URL
    domain = extract_domain(args.url)
    
    # Run dig with the extracted domain and any additional arguments
    run_dig(domain, args.dig_args)

if __name__ == '__main__':
    main()