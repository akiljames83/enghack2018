#a70776a16ea44fe661bbb0e2aaec1e12

import indicoio
indicoio.config.api_key = ''

# single example
print(indicoio.sentiment("I love writing code!"))

# batch example
indicoio.sentiment([
    "I love writing code!",
    "Alexander and the Terrible, Horrible, No Good, Very Bad Day"
])

something = 'something'
options = {'this': 1, 'that': 2, 'there': 3}

for i in xrange(1000000):
    if something in options:
        the_thing = options[something]
    else:
        the_thing = 4

