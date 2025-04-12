"""
Command-line interface for varnishlog-to-elasticsearch.
"""

import sys
import os
import argparse
from .parser import main_loop as pipe_main_loop
from .vsl import main as vsl_main_loop

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Parse Varnish logs and send them to Elasticsearch"
    )
    parser.add_argument(
        "--method",
        choices=["pipe", "vsl"],
        default="vsl",
        help="Method to read Varnish logs (default: vsl)"
    )
    args = parser.parse_args()

    try:
        if args.method == "vsl":
            vsl_main_loop()
        else:
            pipe_main_loop(sys.stdin)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 