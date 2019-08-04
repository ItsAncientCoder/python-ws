class Student:
	def __init__(self,name,rollno,marks):
		self.name = name
		self.rollno = rollno
		self.marks = marks
	def display(self):
		print("name:", self.name)
		print("rollno:", self.rollno)
		print("marks:", self.marks)

s1 = Student("ramu",123,95)
print(s1.__dict__)
