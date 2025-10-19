#!/usr/bin/env python3
import sys
import subprocess
import os
import shlex

MENU = """
Commands:
  password  - set or reuse a password (passkey) for encryption/decryption
  encrypt   - encrypt a string (from history or new)
  decrypt   - decrypt a string (from history or new)
  history   - show session history
  quit      - exit
"""

def ask_choice(prompt: str, choices: list[str]) -> int:
    """
    Prompt user to choose 1..N or 0 to go back.
    Returns index in choices (0-based) or -1 for "new/back".
    """
    while True:
        print(prompt)
        for i, item in enumerate(choices, 1):
            print(f"  {i}. {item}")
        print("  0. Enter a new value / back")
        sel = input("Select: ").strip()
        if sel.isdigit():
            n = int(sel)
            if n == 0:
                return -1
            if 1 <= n <= len(choices):
                return n - 1
        print("Invalid selection. Try again.\n")

def letters_only_or_error(s: str) -> str | None:
    if not s:
        print("Error: empty input.\n")
        return None
    if not s.isalpha():
        print("Error: only letters A-Z are allowed.\n")
        return None
    return s

def main():
    if len(sys.argv) != 2:
        print("Usage: driver.py <log_file>", file=sys.stderr, flush=True)
        sys.exit(1)

    log_file = sys.argv[1]
    py = sys.executable  # use same interpreter

    # Launch logger (stdin piped). No need to read logger stdout.
    logger = subprocess.Popen(
        [py, "-u", "logger.py", log_file],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    # Launch encryption program (stdin/stdout piped).
    enc = subprocess.Popen(
        [py, "-u", "encryption.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    def log(line: str):
        # line format: ACTION MESSAGE
        try:
            logger.stdin.write(line + "\n")
            logger.stdin.flush()
        except Exception:
            pass

    history: list[str] = []  # store inputs and results per spec
    log("START Driver started")

    try:
        while True:
            print(MENU)
            cmd = input("Enter command: ").strip().lower()

            if cmd == "quit":
                log("CMD quit")
                # Tell children to quit
                try:
                    enc.stdin.write("QUIT\n")
                    enc.stdin.flush()
                    # read one response line from encryption
                    resp = enc.stdout.readline().strip()
                except Exception:
                    resp = "ERROR"
                log(f"RESULT {resp}")
                try:
                    logger.stdin.write("QUIT\n")
                    logger.stdin.flush()
                except Exception:
                    pass
                print("Goodbye.")
                break

            elif cmd == "history":
                log("CMD history")
                if not history:
                    print("[empty]")
                else:
                    for i, item in enumerate(history, 1):
                        print(f"{i}: {item}")
                log("RESULT OK")

            elif cmd == "password":
                log("CMD password")
                choice = ask_choice("Use a previous string as password?", history)
                if choice == -1:
                    pw = input("Enter new password (letters only): ").strip().upper()
                else:
                    pw = history[choice].strip().upper()

                pw = letters_only_or_error(pw)
                if not pw:
                    log("ERROR invalid password")
                    continue

                try:
                    enc.stdin.write(f"PASS {pw}\n")
                    enc.stdin.flush()
                    resp = enc.stdout.readline().strip()
                except Exception as e:
                    resp = f"ERROR {e}"

                if resp.startswith("RESULT"):
                    print("Password set.")
                    # Do NOT store passwords in history.
                    log("RESULT Password set")
                else:
                    print(resp)
                    log(f"{resp}")

            elif cmd in ("encrypt", "decrypt"):
                log(f"CMD {cmd}")
                verb = "string to " + cmd
                choice = ask_choice(f"Use a previous string for {cmd}?", history)
                if choice == -1:
                    s = input(f"Enter {verb} (letters only): ").strip().upper()
                    s = letters_only_or_error(s)
                    if not s:
                        log("ERROR invalid input")
                        continue
                    history.append(s)
                else:
                    s = history[choice].strip().upper()

                try:
                    enc.stdin.write(f"{cmd.upper()} {s}\n")
                    enc.stdin.flush()
                    resp = enc.stdout.readline().strip()
                except Exception as e:
                    resp = f"ERROR {e}"

                if resp.startswith("RESULT"):
                    
                    parts = resp.split(maxsplit=1)
                    out = parts[1] if len(parts) > 1 else ""
                    print(out)
                    if out:
                        history.append(out)
                    log(f"RESULT {out if out else 'OK'}")
                else:
                    print(resp)
                    log(resp)

            else:
                print("Unknown command.\n")

    finally:
        log("EXIT Driver exiting")
        try:
            logger.stdin.write("QUIT\n")
            logger.stdin.flush()
        except Exception:
            pass
        # Terminate children if still alive
        for p in (enc, logger):
            try:
                p.terminate()
            except Exception:
                pass

if __name__ == "__main__":
    main()
