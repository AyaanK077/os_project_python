#!/usr/bin/env python3
import sys
from datetime import datetime

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def main():
    if len(sys.argv) != 2:
        print("Usage: logger.py <log_file>", file=sys.stderr, flush=True)
        sys.exit(1)

    log_path = sys.argv[1]
    try:
        with open(log_path, "a", encoding="utf-8") as logf:
            while True:
                line = sys.stdin.readline()
                if not line:
                    break  # EOF
                line = line.rstrip("\n")
                if line == "QUIT":
                    # Do not log QUIT as an action; just exit.
                    break
                
                if not line.strip():
                    continue
                parts = line.split(maxsplit=1)
                action = parts[0]
                message = parts[1] if len(parts) > 1 else ""
                logf.write(f"{timestamp()} [{action}] {message}\n")
                logf.flush()
    except Exception as e:
        print(f"Logger error: {e}", file=sys.stderr, flush=True)
        sys.exit(2)

if __name__ == "__main__":
    main()
