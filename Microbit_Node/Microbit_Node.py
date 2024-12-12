from ble import *
from yolobit import *
button_a.on_pressed = None
button_b.on_pressed = None
button_a.on_pressed_ab = button_b.on_pressed_ab = -1
from wifi import __wifi__
from machine import RTC
import ntptime
import time
from homebit3_lcd1602 import LCD1602
from event_manager import *
from machine import Pin, SoftI2C
from homebit3_dht20 import DHT20
from homebit3_rgbled import RGBLed

def on_ble_message_string_receive_callback(chu_E1_BB_97i):
  global val, v_cmd, serial_id, serial_device, serial_value, cmd, v_id, find_soc, v_device, find_eoc, NODE_ID, v_value, CENTRAL_BLUETOOTH_NAME, one_cmd
  cmd = str(cmd) + str(chu_E1_BB_97i)

ble.on_receive_msg("string", on_ble_message_string_receive_callback)

lcd1602 = LCD1602()

event_manager.reset()

def on_event_timer_callback_J_t_f_H_M():
  global chu_E1_BB_97i, val, v_cmd, serial_id, serial_device, serial_value, cmd, v_id, find_soc, v_device, find_eoc, NODE_ID, v_value, CENTRAL_BLUETOOTH_NAME, one_cmd
  if cmd != '':
    find_soc = cmd.find('!') + 1
    find_eoc = cmd.find('#') + 1
    if find_soc != 0 and find_eoc != 0:
      one_cmd = cmd[int(find_soc - 1) : int(find_eoc)]
      cmd = cmd[int((find_eoc + 1) - 1) : ]
      proccess_one_cmd(one_cmd)

event_manager.add_timer_event(100, on_event_timer_callback_J_t_f_H_M)

def on_event_timer_callback_K_A_C_w_D():
  global chu_E1_BB_97i, val, v_cmd, serial_id, serial_device, serial_value, cmd, v_id, find_soc, v_device, find_eoc, NODE_ID, v_value, CENTRAL_BLUETOOTH_NAME, one_cmd
  lcd1602.move_to(0, 1)
  lcd1602.putstr((''.join([str(x) for x in ['%0*d' % (2, RTC().datetime()[4]), ':', '%0*d' % (2, RTC().datetime()[5]), ':', '%0*d' % (2, RTC().datetime()[6])]])))
  lcd1602.move_to(0, 0)
  lcd1602.putstr((''.join([str(x2) for x2 in ['%0*d' % (2, RTC().datetime()[2]), '/', '%0*d' % (2, RTC().datetime()[1]), '/', '%0*d' % (2, RTC().datetime()[0])]])))

event_manager.add_timer_event(1000, on_event_timer_callback_K_A_C_w_D)

dht20 = DHT20()

def on_event_timer_callback_C_H_b_O_c():
  global chu_E1_BB_97i, val, v_cmd, serial_id, serial_device, serial_value, cmd, v_id, find_soc, v_device, find_eoc, NODE_ID, v_value, CENTRAL_BLUETOOTH_NAME, one_cmd
  dht20.read_dht20()
  print_to_bluetooth_cmd(NODE_ID, 'TEMP', dht20.dht20_temperature())
  print_to_bluetooth_cmd(NODE_ID, 'HUMI', dht20.dht20_humidity())
  print_to_bluetooth_cmd(NODE_ID, 'LUMO', round(translate((pin2.read_analog()), 0, 4095, 0, 100)))

event_manager.add_timer_event(300000, on_event_timer_callback_C_H_b_O_c)

tiny_rgb = RGBLed(pin0.pin, 4)

# Mô tả hàm này...
def control_led_rgb(val):
  global chu_E1_BB_97i, v_cmd, serial_id, serial_device, serial_value, cmd, v_id, find_soc, v_device, find_eoc, NODE_ID, v_value, CENTRAL_BLUETOOTH_NAME, one_cmd, lcd1602, dht20, tiny_rgb
  tiny_rgb.show(0, hex_to_rgb(val))
  print_to_bluetooth_cmd(NODE_ID, 'LED_RGB', val)

def on_ble_disconnected_callback():
  global chu_E1_BB_97i, val, v_cmd, serial_id, serial_device, serial_value, cmd, v_id, find_soc, v_device, find_eoc, NODE_ID, v_value, CENTRAL_BLUETOOTH_NAME, one_cmd
  display.show(Image("11111:10001:10001:10001:11111"))
  while not ble.is_connected():
    ble.connect(CENTRAL_BLUETOOTH_NAME)
  display.show(Image("00000:04440:04440:04440:00000"))

ble.on_disconnected(on_ble_disconnected_callback)

# Mô tả hàm này...
def proccess_one_cmd(v_cmd):
  global chu_E1_BB_97i, val, serial_id, serial_device, serial_value, cmd, v_id, find_soc, v_device, find_eoc, NODE_ID, v_value, CENTRAL_BLUETOOTH_NAME, one_cmd, lcd1602, dht20, tiny_rgb
  v_id = v_cmd[1]
  v_device = v_cmd[3]
  v_value = v_cmd[5 : 11]
  if v_id == NODE_ID:
    if v_device == '1':
      control_led_rgb(v_value)
    elif v_device == '2':
      control_relay(v_value)
    elif v_device == '3':
      control_fan(v_value)

# Mô tả hàm này...
def control_relay(val):
  global chu_E1_BB_97i, v_cmd, serial_id, serial_device, serial_value, cmd, v_id, find_soc, v_device, find_eoc, NODE_ID, v_value, CENTRAL_BLUETOOTH_NAME, one_cmd, lcd1602, dht20, tiny_rgb
  pin3.write_digital((int(val)))
  print_to_bluetooth_cmd(NODE_ID, 'RELAY', int(val))

# Mô tả hàm này...
def print_to_bluetooth_cmd(serial_id, serial_device, serial_value):
  global chu_E1_BB_97i, val, v_cmd, cmd, v_id, find_soc, v_device, find_eoc, NODE_ID, v_value, CENTRAL_BLUETOOTH_NAME, one_cmd, lcd1602, dht20, tiny_rgb
  ble.send((''.join([str(x3) for x3 in ['!', serial_id, ':', serial_device, ':', serial_value, '#']])))

# Mô tả hàm này...
def control_fan(val):
  global chu_E1_BB_97i, v_cmd, serial_id, serial_device, serial_value, cmd, v_id, find_soc, v_device, find_eoc, NODE_ID, v_value, CENTRAL_BLUETOOTH_NAME, one_cmd, lcd1602, dht20, tiny_rgb
  pin1.write_analog(round(translate((int(val)), 0, 100, 0, 1023)))
  print_to_bluetooth_cmd(NODE_ID, 'FAN', int(val))

def on_ble_message_string_receive_callback(chu_E1_BB_97i):
  global val, v_cmd, serial_id, serial_device, serial_value, cmd, v_id, find_soc, v_device, find_eoc, NODE_ID, v_value, CENTRAL_BLUETOOTH_NAME, one_cmd
  cmd = str(cmd) + str(chu_E1_BB_97i)

ble.on_receive_msg("string", on_ble_message_string_receive_callback)

if True:
  display.show(Image("33333:30003:30003:30003:33333"))
  __wifi__.connect_wifi('ABCD', '@512TVTSS')
  ntptime.settime()
  (year, month, mday, week_of_year, hour, minute, second, milisecond) = RTC().datetime()
  RTC().init((year, month, mday, week_of_year, hour+7, minute, second, milisecond))
  NODE_ID = '1'
  cmd = ''
  CENTRAL_BLUETOOTH_NAME = 'ohstem-yolobit-eacc'
  while not ble.is_connected():
    ble.connect(CENTRAL_BLUETOOTH_NAME)
  lcd1602.backlight_on()
  lcd1602.clear()
  display.show(Image("00000:04440:04440:04440:00000"))

while True:
  event_manager.run()
  time.sleep_ms(1000)
  time.sleep_ms(10)
