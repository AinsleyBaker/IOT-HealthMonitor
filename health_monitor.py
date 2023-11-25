# Importing required libraries
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
from twilio.rest import Client
import Adafruit_MCP3008

# Initialising twilio API and Client
account_sid = "Account SID"
auth_token = 'AUTH Token'
client = Client(account_sid, auth_token)

# GPIO Mode(BOARD/BCM)
GPIO.setmode(GPIO.BCM)
# Setting pin configurations
led_pin = 14
dht_pin = 4
CLK = 11
MISO = 9
MOSI = 10
CS = 8    
# Initialising MCP3008, LED and DHT sensor
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
GPIO.setup(led_pin, GPIO.OUT)
dht_sensor = Adafruit_DHT.DHT11
# Value to check for heartbeat
signal_threshold = 250
# Critical thresholds for humidity, temperatures and heartrate
humidity_threshold = 65
humidity_min_threshold = 40
temperature_threshold = 35
temperature_min_threshold = 20
bpm_threshold = 90
bpm_min_threshold = 60

# Function to get signal readings from MCP3008 ACD and calculate BPM
def get_bpm():
    heartbeat_times = []
    bpm_values = []
    start_time = time.time()
    try:
        while time.time() - start_time < 5:
            signal = mcp.read_adc(0)
            # If a signal that represents a heartbeat is detected
            if signal > signal_threshold:
                current_time = time.time()
                if heartbeat_times:
                    # Obtain time between each heartbeat and calculate/display BPM
                    time_between_heartbeats = current_time - heartbeat_times[-1]
                    bpm = int(60/time_between_heartbeats)
                    bpm_values.append(bpm)
                    print(f"Current BPM is {bpm}")
                heartbeat_times.append(current_time)
        # Check if there are BPM values and return the average
        if len(bpm_values) > 0:
            avg_bpm = sum(bpm_values) / len(bpm_values)
            return avg_bpm
    except Exception as e:
        print("An error has occured:", e)

# Function to send messages to phone using twilio
def send_message(message):
    try:
        client.messages.create(body="Health Alert: " + message,
                                from_='sending phone', to="receiving phone")
    except Exception as e:
        print("An error has occured:", e)

# Function to flash led rapidly
def flash_led():
    led_state = False
    for i in range(20):
        # If on, turn off
        if led_state:
            GPIO.output(led_pin, GPIO.LOW)
        # When off, turn on
        else:
            GPIO.output(led_pin, GPIO.HIGH)
        led_state = not led_state
        time.sleep(0.1)

# Main function to display sensor readings and check for critical conditions
def main():
    # Collect Sensor Readings
    humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)
    avg_bpm = get_bpm()
    message_list = []
    # Display sensor readings
    print(f"Heartrate: {avg_bpm} BPM")
    print(f"Temperature: {temperature}°C")
    print(f"Humidity: {humidity}%")

    # Check for critical humidity ranges
    if humidity > humidity_threshold:
        message_list.append("Humidity is too high.")
    elif humidity < humidity_min_threshold:
        message_list.append("Humidity is too low.")
    # Check for critical temperature ranges
    if temperature > temperature_threshold:
        message_list.append("Temperature is too high.")
    elif temperature < temperature_min_threshold:
        message_list.append("Temperature is too low.")
    # Check for critical bpm ranges
    if avg_bpm > bpm_threshold:
        message_list.append("Heart rate is too high.")
    elif avg_bpm < bpm_min_threshold:
        message_list.append("Heart rate is too low.")
    
    # If critical, send a message and flash the LED
    if message_list:
        message = " ".join(message_list)
        send_message(message)
        flash_led()
    # Reset pin modes to input
    GPIO.cleanup()

if __name__ == "__main__":
    main()



