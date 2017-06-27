class Category:
	def __init__(self, name, numQuestions, totalPoints):
		self.name = name
		self.numQuestions = numQuestions
		self.totalPoints = totalPoints
		self.questions = []
		
class Question:
	def __init__(self, studentAnswer, correctAnswer, pointsGiven, category):
		self.studentAnswer = studentAnswer
		self.correctAnswer = correctAnswer
		self.pointsGiven = pointsGiven
		self.category = category
	
		
		