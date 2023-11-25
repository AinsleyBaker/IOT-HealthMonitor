# Raspberry Pi Health Monitoring Program
This project incorporates the Raspberry Pi to monitor a persons heartrate and surrounding temperature and humidity. 
Equipment:
Raspberry Pi
Breadboard
Jumper Wires
KY-039 Heartbeat Sensor
MCP3008 ADC
LED
DHT11 Temperature and Humidity Sensor
Twilio API

The projects initialises when a person places their finger on the KY-039 hearbeat sensor for 5 seconds where their hearrate will be calculated by finding the time between each pulse in signal from the MCP3008. The average BPM is calculated and the temperature and humidity is collected for the surrounding environment. A critical check is performed on the collected values. If any parameter falls into a critical range, an LED will rapidly flash, signaling a potential health concern. Simultaneously, a critical message is sent to a predefined phone number using the Twilio API.

This project is suitable for monitoring elderly health accurately and quickly while alerting caretakers of potential health concerns.

