from yolobit import *
button_a.on_pressed = None
button_b.on_pressed = None
button_a.on_pressed_ab = button_b.on_pressed_ab = -1
from homebit3_rgbled import RGBLed
from event_manager import *
from ble import *
import sys
import uselect
from homebit3_lcd1602 import LCD1602
from machine import RTC
from wifi import __wifi__
import ntptime
import time
from machine import Pin, SoftI2C
from homebit3_dht20 import DHT20
from homebit3_ir_receiver import *
import music

# Mô tả hàm này...
def proccess_one_cmd(v_cmd):
  global val, chu_E1_BB_97i, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd, tiny_rgb, lcd1602, dht20, homebit3_ir_rx
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
    elif v_device == '4':
      control_door(v_value)
    elif v_device == '5':
      change_password(v_value)

tiny_rgb = RGBLed(pin0.pin, 4)

# Mô tả hàm này...
def control_led_rgb(val):
  global v_cmd, chu_E1_BB_97i, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd, tiny_rgb, lcd1602, dht20, homebit3_ir_rx
  tiny_rgb.show(0, hex_to_rgb(val))
  print_to_serial_cmd(NODE_ID, 'LED_RGB', val)

# Mô tả hàm này...
def control_door(val):
  global v_cmd, chu_E1_BB_97i, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd, tiny_rgb, lcd1602, dht20, homebit3_ir_rx
  if (int(val)) == 0:
    init_door_close_1()
    DOOR_STATUS = 1
  elif (int(val)) == 1:
    init_door_open_2()
    DOOR_STATUS = 2

# Mô tả hàm này...
def control_relay(val):
  global v_cmd, chu_E1_BB_97i, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd, tiny_rgb, lcd1602, dht20, homebit3_ir_rx
  pin3.write_digital((int(val)))
  print_to_serial_cmd(NODE_ID, 'RELAY', int(val))

event_manager.reset()

def on_event_timer_callback_J_t_f_H_M():
  global v_cmd, val, chu_E1_BB_97i, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd
  if cmd != '':
    find_soc = cmd.find('!') + 1
    find_eoc = cmd.find('#') + 1
    if find_soc != 0 and find_eoc != 0:
      one_cmd = cmd[int(find_soc - 1) : int(find_eoc)]
      cmd = cmd[int((find_eoc + 1) - 1) : ]
      ble.send(one_cmd)
      proccess_one_cmd(one_cmd)

event_manager.add_timer_event(100, on_event_timer_callback_J_t_f_H_M)

def read_terminal_input():
  spoll=uselect.poll()        # Set up an input polling object.
  spoll.register(sys.stdin, uselect.POLLIN)    # Register polling object.

  input = ''
  if spoll.poll(0):
    input = sys.stdin.read(1)

    while spoll.poll(0):
      input = input + sys.stdin.read(1)

  spoll.unregister(sys.stdin)
  return input

def on_event_timer_callback_k_D_V_o_z():
  global v_cmd, val, chu_E1_BB_97i, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd
  cmd = str(cmd) + str(read_terminal_input())

event_manager.add_timer_event(200, on_event_timer_callback_k_D_V_o_z)

# Mô tả hàm này...
def change_password(val):
  global v_cmd, chu_E1_BB_97i, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd, tiny_rgb, lcd1602, dht20, homebit3_ir_rx
  PASSWORD = val
  print_to_serial_cmd(NODE_ID, 'DOOR_PASS', val)

lcd1602 = LCD1602()

def on_event_timer_callback_K_A_C_w_D():
  global v_cmd, val, chu_E1_BB_97i, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd
  lcd1602.move_to(0, 0)
  lcd1602.putstr((''.join([str(x) for x in [' ', '%0*d' % (2, RTC().datetime()[4]), ':', '%0*d' % (2, RTC().datetime()[5]), ':', '%0*d' % (2, RTC().datetime()[6]), ' ', '%0*d' % (2, RTC().datetime()[2]), '/', '%0*d' % (2, RTC().datetime()[1]), ' ']])))

event_manager.add_timer_event(1000, on_event_timer_callback_K_A_C_w_D)

# Mô tả hàm này...
def control_fan(val):
  global v_cmd, chu_E1_BB_97i, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd, tiny_rgb, lcd1602, dht20, homebit3_ir_rx
  pin1.write_analog(round(translate((int(val)), 0, 100, 0, 1023)))
  print_to_serial_cmd(NODE_ID, 'FAN', int(val))

# Mô tả hàm này...
def init_door_close_1():
  global v_cmd, val, chu_E1_BB_97i, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd, tiny_rgb, lcd1602, dht20, homebit3_ir_rx
  pin7.servo_write(10)
  pin7.servo_release()
  print_to_serial_cmd(NODE_ID, 'DOOR', '0')
  PASS_INPUT = ''

# Mô tả hàm này...
def print_pass_input():
  global v_cmd, val, chu_E1_BB_97i, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd, tiny_rgb, lcd1602, dht20, homebit3_ir_rx
  lcd1602.move_to(10, 1)
  lcd1602.putstr('______')
  if DOOR_STATUS == 3:
    lcd1602.move_to(10, 1)
    lcd1602.putstr(PASS_INPUT)
  else:
    chu_E1_BB_97i = ''
    for i in PASS_INPUT:
      chu_E1_BB_97i = str(chu_E1_BB_97i) + '*'
    lcd1602.move_to(10, 1)
    lcd1602.putstr(chu_E1_BB_97i)

def on_event_timer_callback_Z_l_c_f_o():
  global v_cmd, val, chu_E1_BB_97i, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd
  if DOOR_STATUS == 0:
    if True:
      init_door_close_1()
      DOOR_STATUS = 1
  elif DOOR_STATUS == 1:
    door_close_1()
    if PASS_INPUT == PASSWORD:
      init_door_open_2()
      DOOR_STATUS = 2
  elif DOOR_STATUS == 2:
    door_open_2()
    if PASS_INPUT == PASSWORD:
      init_change_password_3()
      DOOR_STATUS = 3
    if INPUT_KEY_CONTROL == 'A':
      INPUT_KEY_CONTROL = ''
      init_door_close_1()
      DOOR_STATUS = 1
  elif DOOR_STATUS == 3:
    change_password_3()
    if INPUT_KEY_CONTROL == 'A':
      INPUT_KEY_CONTROL = ''
      init_door_close_1()
      DOOR_STATUS = 1
    if INPUT_KEY_CONTROL == 'E':
      INPUT_KEY_CONTROL = ''
      homebit3_ir_rx.clear_code()
      init_door_open_2()
      DOOR_STATUS = 2
    if len(PASS_INPUT) == 6:
      print_to_serial_cmd(NODE_ID, 'DOOR_PASS', PASS_INPUT)
      PASSWORD = PASS_INPUT
      init_door_open_2()
      DOOR_STATUS = 2
  else:
    DOOR_STATUS = 0

event_manager.add_timer_event(50, on_event_timer_callback_Z_l_c_f_o)

dht20 = DHT20()

# Mô tả hàm này...
def door_close_1():
  global v_cmd, val, chu_E1_BB_97i, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd, tiny_rgb, lcd1602, dht20, homebit3_ir_rx
  lcd1602.move_to(0, 1)
  lcd1602.putstr('LOCKED')
  PASS_INPUT = str(PASS_INPUT) + str(read_remote_number())
  print_pass_input()
  if len(PASS_INPUT) == 6 and PASS_INPUT != PASSWORD:
    PASS_INPUT = ''

def on_ble_message_string_receive_callback(chu_E1_BB_97i):
  global v_cmd, val, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd
  print(chu_E1_BB_97i, end =' ')

ble.on_receive_msg("string", on_ble_message_string_receive_callback)

homebit3_ir_rx = IR_RX(Pin(pin10.pin, Pin.IN)); homebit3_ir_rx.start();

# Mô tả hàm này...
def read_remote_number():
  global v_cmd, val, chu_E1_BB_97i, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd, tiny_rgb, lcd1602, dht20, homebit3_ir_rx
  INPUT_KEY = ''
  if homebit3_ir_rx.get_code() == IR_REMOTE_0:
    INPUT_KEY = '0'
  if homebit3_ir_rx.get_code() == IR_REMOTE_1:
    INPUT_KEY = '1'
  if homebit3_ir_rx.get_code() == IR_REMOTE_2:
    INPUT_KEY = '2'
  if homebit3_ir_rx.get_code() == IR_REMOTE_3:
    INPUT_KEY = '3'
  if homebit3_ir_rx.get_code() == IR_REMOTE_4:
    INPUT_KEY = '4'
  if homebit3_ir_rx.get_code() == IR_REMOTE_5:
    INPUT_KEY = '5'
  if homebit3_ir_rx.get_code() == IR_REMOTE_6:
    INPUT_KEY = '6'
  if homebit3_ir_rx.get_code() == IR_REMOTE_7:
    INPUT_KEY = '7'
  if homebit3_ir_rx.get_code() == IR_REMOTE_8:
    INPUT_KEY = '8'
  if homebit3_ir_rx.get_code() == IR_REMOTE_9:
    INPUT_KEY = '9'
  if homebit3_ir_rx.get_code() == IR_REMOTE_A:
    INPUT_KEY_CONTROL = 'A'
  if homebit3_ir_rx.get_code() == IR_REMOTE_E:
    INPUT_KEY_CONTROL = 'E'
  if INPUT_KEY != '':
    music.play(['G3:0.25'], wait=True)
  homebit3_ir_rx.clear_code()
  return INPUT_KEY

# Mô tả hàm này...
def print_to_serial_cmd(serial_id, serial_device, serial_value):
  global v_cmd, val, chu_E1_BB_97i, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd, tiny_rgb, lcd1602, dht20, homebit3_ir_rx
  print((''.join([str(x2) for x2 in ['!', serial_id, ':', serial_device, ':', serial_value, '#']])), end =' ')

# Mô tả hàm này...
def init_door_open_2():
  global v_cmd, val, chu_E1_BB_97i, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd, tiny_rgb, lcd1602, dht20, homebit3_ir_rx
  pin7.servo_write(170)
  pin7.servo_release()
  print_to_serial_cmd(NODE_ID, 'DOOR', '1')
  PASS_INPUT = ''
  INPUT_KEY_CONTROL = ''

# Mô tả hàm này...
def door_open_2():
  global v_cmd, val, chu_E1_BB_97i, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd, tiny_rgb, lcd1602, dht20, homebit3_ir_rx
  lcd1602.move_to(0, 1)
  lcd1602.putstr('OPENED')
  PASS_INPUT = str(PASS_INPUT) + str(read_remote_number())
  if len(PASS_INPUT) == 6 and PASS_INPUT != PASSWORD:
    PASS_INPUT = ''
  print_pass_input()

# Mô tả hàm này...
def init_change_password_3():
  global v_cmd, val, chu_E1_BB_97i, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd, tiny_rgb, lcd1602, dht20, homebit3_ir_rx
  PASS_INPUT = ''
  INPUT_KEY_CONTROL = ''

# Mô tả hàm này...
def change_password_3():
  global v_cmd, val, chu_E1_BB_97i, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd, tiny_rgb, lcd1602, dht20, homebit3_ir_rx
  lcd1602.move_to(0, 1)
  lcd1602.putstr('SET_PW')
  PASS_INPUT = str(PASS_INPUT) + str(read_remote_number())
  print_pass_input()

def on_button_b_pressed():
  global v_cmd, val, chu_E1_BB_97i, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd
  dht20.read_dht20()
  print_to_serial_cmd(NODE_ID, 'TEMP', dht20.dht20_temperature())
  print_to_serial_cmd(NODE_ID, 'HUMI', dht20.dht20_humidity())
  print_to_serial_cmd(NODE_ID, 'LUMO', round(translate((pin2.read_analog()), 0, 4095, 0, 100)))

button_b.on_pressed = on_button_b_pressed

def on_ble_message_string_receive_callback(chu_E1_BB_97i):
  global v_cmd, val, serial_id, serial_device, serial_value, v_id, cmd, PASSWORD, INPUT_KEY, PASS_INPUT, v_device, find_soc, DOOR_STATUS, INPUT_KEY_CONTROL, v_value, NODE_ID, find_eoc, i, one_cmd
  print(chu_E1_BB_97i, end =' ')

ble.on_receive_msg("string", on_ble_message_string_receive_callback)

if True:
  display.show(Image("33333:30003:30003:30003:33333"))
  __wifi__.connect_wifi('ABCD', '@512TVTSS')
  ntptime.settime()
  (year, month, mday, week_of_year, hour, minute, second, milisecond) = RTC().datetime()
  RTC().init((year, month, mday, week_of_year, hour+7, minute, second, milisecond))
  NODE_ID = '0'
  cmd = ''
  DOOR_STATUS = 0
  INPUT_KEY_CONTROL = ''
  PASSWORD = '123456'
  PASS_INPUT = ''
  lcd1602.backlight_on()
  lcd1602.clear()
  display.show(Image("00000:04440:04040:04440:00000"))

while True:
  event_manager.run()
  time.sleep_ms(1000)
  time.sleep_ms(10)
