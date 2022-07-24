# from django.test import TestCase

# Create your tests here.

class Math:
    @staticmethod
    def add5(x):
        return x + 5


print(Math.add5(8))



























# class Person:
#     number_of_people = 0
#
#     def __init__(self, name):
#         self.name = name
#         Person.add_person()
#
#     @classmethod
#     def number_of_people_(cls):
#         return cls.number_of_people
#
#     @classmethod
#     def add_person(cls):
#         cls.number_of_people += 1
#
#
# p1 = Person('oscar')
#
# print(Person.number_of_people_())
#
#
#
#
#


# class People:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def get_age(self):
#         return self.age
#
#
# class Job(People):
#     def __init__(self):
#         self.applyied = []
#
#     def add_people(self, apply):
#         if apply.get_age() > 25:
#             self.applyied.append(apply)
#
#     def list_win(self):
#         for win in self.applyied:
#             print("win ===", win.name)
#
#
# p1 = People("oscar", 32)
# p2 = People("jim", 12)
# p3 = People("zerus", 40)
#
# job = Job()
# job.add_people(p1)
# job.add_people(p2)
# job.add_people(p3)
#
# print(job.list_win())

# class Student:
#     def __init__(self, name, age, grade):
#         self.name = name
#         self.age = age
#         self.grade = grade
#
#     def get_grade(self):
#         return self.grade
#
#
# class Course:
#     def __init__(self, name, max_students):
#         self.name = name
#         self.max_students = max_students
#         self.students = []
#
#     def add_student(self, student):
#         if len(self.students) < self.max_students:
#             self.students.append(student)
#             return True
#         return False
#
#     def get_average_grade(self):
#         value = 0
#         for student in self.students:
#             value += student.get_grade()
#         return value/len(self.students)
#
#
# s1 = Student("oscar", 19, 40)
# s2 = Student("geno", 19, 75)
# s3 = Student("jill", 19, 65)
#
# course = Course('Science', 2)
# course.add_student(s1)
# course.add_student(s2)
# print(course.add_student(s3))
#
# print(course.students[0].name)
# print(course.get_average_grade())


# game = "oscar, jim, roone"
#
# zerus = game.split(',')
# for zero in zerus:
#     print(zero)

# class Guitar:
#     def __init__(self, n_strings=6):
#         self.n_strings = n_strings
#         self.play()
#         self.__cost = 50
#
#     def play(self):
#         print(" pam pam pam pam pam")
#
# class BassGuitar(Guitar):
#     pass
#
#
#
# class ElectricGuitar(Guitar):
#     def __init__(self):
#         super().__init__(n_strings = 8)
#         self.colour = ("#000000", "#FFFFFFFF")
#
#     def playLouder(self):
#         print("pam pam pam pam".upper())
#
#     def __secret(self):
#         print("this guitar actually cost me $", self._Guitar__cost, "only!")
#
#
# my_guitar = ElectricGuitar()
# # print(my_guitar._ElectricGuitar__secret())
# print("my base guitar has", BassGuitar(4).n_strings, "string")
# print("my electric guitar has ", my_guitar.n_strings, "string")
