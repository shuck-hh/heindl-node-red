/**********************************************************************
 * Filename    : MatrixKeypad.cpp
 * Description : Obtain the key code of 4x4 Matrix Keypad
 * Author      : www.freenove.com
 * modification: 2019/12/27
 **********************************************************************/
#include "Keypad.hpp"
#include <stdio.h>

const byte ROWS = 4;
const byte COLS = 4;

char keys[ROWS][COLS] = {
    {'1', '2', '3', 'A'},
    {'4', '5', '6', 'B'},
    {'7', '8', '9', 'C'},
    {'*', '0', '#', 'D'}};

byte rowPins[ROWS] = {1, 4, 5, 6};
byte colPins[COLS] = {12, 3, 2, 0};

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

int main()
{
    printf("Program is starting ... \n");

    wiringPiSetup();

    FILE *file = fopen("keys.txt", "w");
    char key = 0;
    keypad.setDebounceTime(50);

    while (1)
    {
        key = keypad.getKey();

        if (key)
        {
            printf("You Pressed key : %c\n", key);

            rewind(file); // zurück zum Anfang
            fprintf(file, "%c\n", key);
            fflush(file); // sofort schreiben
        }
    }

    fclose(file);
    return 1;
}
