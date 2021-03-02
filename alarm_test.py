# alarm_test.py

from home import Home

h0 = Home('Andrew', 'SW 12th St')

print(h0._alarm.get_pin())

h0._alarm.set_pin(1234)
print(h0._alarm.get_pin())

h0._alarm.enable(4321)
status = h0._alarm.get_status()
print(status)

h0._alarm.enable(1234)
status = h0._alarm.get_status()
print(status)

h0._alarm.enable(1234)
status = h0._alarm.get_status()
print(status)

h0._alarm.disable(4321)
status = h0._alarm.get_status()
print(status)

h0._alarm.disable(1234)
status = h0._alarm.get_status()
print(status)