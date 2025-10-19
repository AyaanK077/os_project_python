#!/usr/bin/env python3
import sys
import string

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
A2I = {c:i for i,c in enumerate(ALPHABET)}
I2A = {i:c for i,c in enumerate(ALPHABET)}

def only_letters(s: str) -> bool:
    return all(ch.isalpha() for ch in s)

def vigenere(text: str, key: str, mode: str) -> str:
    # text and key should be uppercase letters only
    res = []
    klen = len(key)
    ki = 0
    for ch in text:
        t = A2I[ch]
        k = A2I[key[ki % klen]]
        if mode == "ENCRYPT":
            v = (t + k) % 26
        else:
            v = (t - k) % 26
        res.append(I2A[v])
        ki += 1
    return "".join(res)

def main():
    passkey = None
    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue
        parts = line.split(maxsplit=1)
        cmd = parts[0].upper()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd in ("QUIT",):
            print("RESULT", flush=True)
            break

        if cmd in ("PASS", "PASSKEY"):
            candidate = arg.strip().upper()
            if not candidate:
                print("ERROR Missing password", flush=True)
                continue
            if not only_letters(candidate):
                print("ERROR Password must contain letters only", flush=True)
                continue
            passkey = candidate
            print("RESULT", flush=True)
            continue

        if cmd in ("ENCRYPT", "DECRYPT"):
            if passkey is None:
                print("ERROR Password not set", flush=True)
                continue
            text = arg.strip().upper()
            if not text:
                print("ERROR Missing input", flush=True)
                continue
            if not only_letters(text):
                print("ERROR Input must contain letters only", flush=True)
                continue
            out = vigenere(text, passkey, "ENCRYPT" if cmd == "ENCRYPT" else "DECRYPT")
            print("RESULT", out, flush=True)
            continue

        print("ERROR Unknown command", flush=True)

if __name__ == "__main__":
    main()
