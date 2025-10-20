 Development Log


## 2025-10-18 5:30

### Thoughts so far

I’ve read the project specification for Project 1. The assignment requires three separate programs (logger, encryption, and driver) that communicate using pipes. I’m implementing it in Python using the subprocess module because it’s faster to build, test, and debug than C, while still meeting the IPC requirement. I verified the Vigenere cipher logic works correctly with sample input (HELLO key, WORLD → DSCWR).  


### Plan for this session

- Initialize a Git repository and push it to GitHub.
- Begin working on the code for logger.py, encryption.py, and driver.py.
- Document how to run and maintain the project in the README.


## 2025-10-19 3:30
### Thoughts so far
Started writing the driver and logger parts. The logger writes to the file with timestamps, which looks clean. Had a small issue where it froze waiting for input, but I fixed that by making Python print and flush right away. That made everything respond instantly.

### Plan for this session
- Make the driver start both the logger and encryption programs.
- Build the menu with options like “password”, “encrypt”, “decrypt”, “history”, and “quit”.
- Make sure everything gets logged.
- Test that I can store and reuse strings in a session.

### Reflection
Got most of the structure working. The driver starts both programs and the logging works. The history feature saves what I type, and the password isn’t stored like the instructions said. It’s starting to feel like a real system now. Next I’ll finish the encryption logic so it’s ready to test end-to-end.



## 2025-10-19 7:15

### Thoughts so far

The encryption code is finally working right. I tested it with the example from the project sheet, and it gave the exact same output (HELLO key, WORLD → DSCWR). It took me a bit to fix how it handled upper and lowercase letters, but now it’s all consistent.


### Plan for this session

- Get the encryption program to accept all four commands (PASS, ENCRYPT, DECRYPT, QUIT).
- Make it show “RESULT” or “ERROR” depending on what happens.
- Make sure it only works on letters (no numbers or spaces).
- Run a few tests to confirm the math behind the cipher.


### Reflection

The cipher works great now. It correctly encrypts and decrypts, and it shows a proper “RESULT” when it succeeds. It also gives “ERROR Password not set” if I try to encrypt before setting one. Feels good to see it working. Next up: connecting this to the driver so I can control everything from one place.








