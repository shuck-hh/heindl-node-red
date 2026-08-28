# heindl-node-red

A Node RED project of mine to controll the state of windows based on the temperature

> [!IMPORTANT]  
> This is only public so that I can update my project via this repo! It is not intended to be used by anyone else although it's not forbidden!

# Requirements
- wiringPi (there's a note in the cpp folder for that)
- git
- yad (only if update.sh is used) (install via ```sudo apt install yad```)
- NodeRED for sure

# Compile the C++ part

run ```gcc MatrixKeypad.cpp Keypad.cpp Key.cpp -o MatrixKeypad -lwiringPi```

# Run the Project
run ```sudo ./MatrixKeypad``` and in a second terminal run ```python I2CLCD1602.py```
