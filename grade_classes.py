class Category:
	def __init__(self, name):
		self.name = name
		self.numQuestions = 0
		self.totalPoints = 0
		self.correctPercentage = 0
		self.questions = []
		
class Question:
	def __init__(self, studentAnswer, correctAnswer, pointsGiven, category, name):
		self.studentAnswer = studentAnswer
		self.correctAnswer = correctAnswer
		self.pointsGiven = pointsGiven
		self.category = category
		self.name = name

def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def is_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False
		
		