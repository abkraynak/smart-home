# home-test.py

from home import Home

# Testing homes
h0 = Home('Andrew', 'SW 12th St')
print(h0._firstName)
print(h0._address)

h1 = Home('Brian', 'Fayetteville St')
print(h1._firstName)
print(h1._address)


# Testing alarms
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


# Testing lights
h0.print_lights()
h0.add_light('Kitchen')
h0.print_lights()
h0.add_light('Bedroom')
h0.add_light('Living Room')
h0.print_lights()


# Testing locks
h0.print_locks()
h0.add_lock('Front Door', 1234)
h0.print_locks()
h0.add_lock('Garage Door', 5678)
h0.print_locks()
h0.print_locks()






