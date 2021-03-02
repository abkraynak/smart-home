# lock_test.py

from home import Home

h0 = Home('Andrew', 'SW 12th St')

h0.print_locks()
h0.add_lock('Front Door', 1234)
h0.print_locks()
h0.add_lock('Garage Door', 5678)
h0.print_locks()
h0.print_locks()

h0.enable_lock('Front Door', 1234)
h0.enable_lock('Garage Door', 5678)

h0.print_locks()