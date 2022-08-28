# from django.test import TestCase
#
# # Create your tests here.


def viralAdvertising(n):
    shared = n-1
    liked = 0
    cumulative = 0

    for i in range(n):
        liked = int(shared / 2)
        shared = int(liked * 3)
        print(shared)


print(viralAdvertising(5))
