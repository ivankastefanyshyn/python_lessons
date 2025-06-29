import my_module

# import function
my_module.greeting("Yana")
my_module.greeting("Ivanka")

# import variable
print(my_module.person)
hm = my_module.person["age"]
print(hm)

# import list and access its elements
print(my_module.numbers)
print(my_module.numbers[0:2])

new_sentence = my_module.sentence.upper()
print(new_sentence)

import math

print(math.pi)
print(math.sin(100))
print(dir(math))
print(dir(my_module))

# import with from
from my_module import sentence

print(sentence)
print(sentence.count("e"))

# dir()function
print(dir())

# __name__testing
my_module.say_hello()

# search path
import sys
from pprint import pprint

print(sys.path)
