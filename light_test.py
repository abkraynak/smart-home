# light_test.py

from home import Home

h0 = Home('Andrew', 'SW 12th St')

h0.print_lights()
h0.add_light('Kitchen')
h0.print_lights()
h0.add_light('Bedroom')
h0.add_light('Living Room')
h0.print_lights()

h0.set_light_color('Bedroom', 160, 255, 43)
col = h0.get_light_color('Bedroom')
print(col)

print(h0.get_light_brightness('Bedroom'))
h0.set_light_brightness('Bedroom', 70)
print(h0.get_light_brightness('Bedroom'))
h0.set_light_brightness('Living Room', 140)

status = h0.get_light_status('Bedroom')
print(status)

h0.enable_light('Bedroom')
h0.print_lights()