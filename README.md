This is a temporary fork of cc65 to discuss some serial driver issues.

The problem:
- When there's a lot of data to receive the NmiHnadler will terminate the transmit in TryToSend. This leaves data in the transmit buffer.
- The documentation is explicit that transmitting is not interrupt driven, and the documentation is correct in that regard.
- The only way to flush the transmit buffer is to send more bytes.

The solution?
- Allow calling the TryToSend procedure in the serial driver.
- It would be nice to get back the number of free and queued bytes.

What's in this repo:
- A modified c64 serial driver, where ser_ioctl() calls TryToSend.
- A modified terminal, based on the sample:
  - Faster baud rate, 38400 instead of 9600.
  - Faster print through cbm_k_chrout() instead of putchar().
  - Optionally calls TryToSend in every loop iteration.

Instructions:
- clone the repo
- compile the modified cc65: `make all`
- change to the `ser-try-to-send` directory
- compile the modified terminal: `./compile.sh`
- start the tcp server: `./server.py`
- in a new terminal, start vice:
  - `./start-vice.sh terminal-do-not-try-to-send.prg`
  - `./start-vice.sh terminal-do-try-to-send.prg`
- Walk in the meadow. You are the purple lozenge. WASD controls you.
- Every keypress that was successfully queued will increment the border color.
- If you press the buttons too quickly, sometimes, the key presses gets queued, but not transmitted. Press space to do nothing but force a flush.
- Liberal application of TryToSend makes the problem disappear.
