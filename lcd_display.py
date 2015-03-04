#!/usr/bin/python

import time
import Adafruit_GPIO.MCP230xx as MCP
import Adafruit_GPIO as GPIO


PIN_RW = 10
PIN_RS = 5
PIN_VDD = 6
PIN_VSS = 8
PIN_ENA = 4

PIN_DB0 = 11
PIN_DB1 = 3
PIN_DB2 = 12
PIN_DB3 = 2
PIN_DB4 = 13
PIN_DB5 = 1
PIN_DB6 = 14
PIN_DB7 = 0
gpio = MCP.MCP23017(0x20,busnum=1)
LCD_DISPLAYON = 0x0c
LCD_DISPLAYOFF = 0x08
LCD_CURSORHOME = 0x03
LCD_NEXTLINE = 0xC0
LCD_CLEARSCRN = 0x01
LCD_ENTRYMODE = 0x06
LCD_8BITMODE = 0x38  #8bit/2line mode
LCD_SETCURSOR = 0x10
LCD_BLINKCURSR = 0x0F 
LCD_WAKEUP = 0x30


def writed8(value):
	gpio.output_pins({ PIN_DB0: (value        & 1) > 0,
                           PIN_DB1: ((value >> 1) & 1) > 0,
                           PIN_DB2: ((value >> 2) & 1) > 0,
                           PIN_DB3: ((value >> 3) & 1) > 0, 
			   PIN_DB4: ((value >> 4) & 1) > 0,
                           PIN_DB5: ((value >> 5) & 1) > 0,
                           PIN_DB6: ((value >> 6) & 1) > 0,
                           PIN_DB7: ((value >> 7) & 1) > 0 }) 

def command(input):
	#Set Command Data
        writed8(input)

        #Set Register Select to Command = LOW
        gpio.output(PIN_RS, GPIO.LOW)

        #Set R/W bit to LOW for write
        gpio.output(PIN_RW, GPIO.LOW)

        #Set Enable to High
        gpio.output(PIN_ENA, GPIO.HIGH)
	time.sleep(0.03)
        #Clock Enable
        gpio.output(PIN_ENA, GPIO.LOW)
  
def write_data(value):
	writed8(value)
	gpio.output(PIN_RS, GPIO.HIGH)
	gpio.output(PIN_RW, GPIO.LOW)
	#Set Enable to High
        gpio.output(PIN_ENA, GPIO.HIGH)
        time.sleep(0.03)
        #Clock Enable
        gpio.output(PIN_ENA, GPIO.LOW)

def write_string(str):
	for x in (str):
          write_data(int(ord(x)))

def main():
	gpio.setup(PIN_VDD, GPIO.OUT)
	gpio.setup(PIN_VSS, GPIO.OUT)
	gpio.setup(PIN_RS, GPIO.OUT)
	gpio.setup(PIN_RW, GPIO.OUT)
	gpio.setup(PIN_ENA, GPIO.OUT)

	for pin in (PIN_DB0, PIN_DB1, PIN_DB2, PIN_DB3, PIN_DB4, PIN_DB5, PIN_DB6, PIN_DB7):
		gpio.setup(pin, GPIO.OUT)
        	gpio.output(pin, GPIO.LOW);
	gpio.output(PIN_VDD, GPIO.HIGH)
	gpio.output(PIN_VSS, GPIO.LOW)
        time.sleep(0.01)

        command(LCD_WAKEUP)
        time.sleep(0.02)
        command(LCD_8BITMODE)
        time.sleep(0.02)
        command(LCD_SETCURSOR)
        time.sleep(0.02)
        command(LCD_CURSORHOME)
        command(LCD_DISPLAYON)
        command(LCD_ENTRYMODE)
        command(LCD_CLEARSCRN)
        write_string("Works")
        command(LCD_NEXTLINE)
        write_string("GoodGood")

#
# Minimum setting to run display VDD and VSS
# using default pin directions
#
def after_init():
	time.sleep(0.01)
	gpio.output(PIN_VDD, GPIO.HIGH)
	gpio.output(PIN_VSS, GPIO.LOW)

def display_info():
	after_init()
        command(LCD_CLEARSCRN)
        write_string("Great!")
        command(LCD_NEXTLINE)
        write_string("GoodGood")

def counter():
	after_init()
        command(LCD_CLEARSCRN)
        write_string("Counting")
        command(LCD_NEXTLINE)
        write_string("time: ")
	for x in range(0,10):
		write_string(str(x))
		command(0xc6)
		time.sleep(0.5)

def display_off():
        command(LCD_DISPLAYOFF)

main()
#display_info()
#counter()
