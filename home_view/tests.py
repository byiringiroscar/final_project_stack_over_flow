# from django.test import TestCase
#
# # Create your tests here.


import phonenumbers
from phonenumbers import carrier, timezone, geocoder
from phonenumbers.phonenumberutil import number_type

number = "+250"
print(carrier._is_mobile(number_type(phonenumbers.parse(number))))
print(phonenumbers.parse("+911234567890"))

my_number = phonenumbers.parse("+911234567890")
print(carrier.name_for_number(my_number, "en"))

print(timezone.time_zones_for_number(my_number))

print(geocoder.description_for_number(my_number, "en"))

print(phonenumbers.is_valid_number(my_number))
print(phonenumbers.is_possible_number(my_number))
