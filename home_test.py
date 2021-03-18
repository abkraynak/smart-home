# home_test.py

from home import Home

h0 = Home('Andrew', 'SW 12th St')
print(h0._firstName)
print(h0._address)
print(h0.authenticate('admin', 'password'))
print(h0.authenticate('abkraynak', 'mypassword'))


h1 = Home('Brian', 'Fayetteville St')
print(h1._firstName)
print(h1._address)