from home import Home

h0 = Home('Andrew', 'SW 12th St')
print(h0._firstName)
print(h0._address)
print(h0.get_alarm_pin())

h0.set_alarm_pin(1234)
print(h0.get_alarm_pin())

h0.enable_alarm(4321)
status = h0.get_alarm_status()
print(status)

h0.enable_alarm(1234)
status = h0._alarm.get_status()
print(status)

h0.enable_alarm(1234)
status = h0.get_alarm_status()
print(status)

h0.disable_alarm(4321)
status = h0.get_alarm_status()
print(status)

h0.disable_alarm(1234)
status = h0.get_alarm_status()
print(status)


h1 = Home('Brian', 'Fayetteville St')
print(h1._firstName)
print(h1._address)