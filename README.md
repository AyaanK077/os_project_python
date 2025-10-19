# OS Project (Python version)
# Ayaan Khan
# ARK220001
# CS 4348.504
# Prof. Salazar
# 10/19/2025

This folder contains three programs as required:

- `logger.py` — reads log lines from STDIN and appends timestamped entries to a given log file.
- `encryption.py` — Vigenère cipher backend supporting `PASS`, `ENCRYPT`, `DECRYPT`, `QUIT`.
- `driver.py` — launches both subprocesses and provides an interactive menu.

## How to run

1. Make sure you have **Python 3.9+** installed.
2. Open a terminal in this folder:
   ```bash
   cd /mnt/data/os_project_python
   ```
3. Run the driver with a log file path (it will be created if missing):
   ```bash
   python driver.py session.log
   ```

## Notes
- Input must be letters only (A–Z). Case-insensitive; everything is uppercased internally.
- Passwords are not stored in history and are never logged.
- Processes communicate over pipes; `-u` ensures unbuffered I/O for snappy interaction.
- To exit cleanly, use the `quit` command in the driver.
