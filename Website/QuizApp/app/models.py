from app import db

class Quiz(db.Model):
	q_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), index=True, unique=False)
	results = db.relationship('Result', backref='author', lazy='dynamic')

	def __repr__(self):
		return 'Quiz<%s, %s>' % (self.q_id, self.name)

class Result(db.Model):
	result_id = db.Column(db.Integer, primary_key=True)
	relational_id = db.Column(db.Integer, index=True, unique=False)
	body = db.Column(db.Text)
	quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.q_id'))

	def __repr__(self):
		return 'Result<%s, %s, %s>' % (self.result_id, self.relational_id, self.quiz_id)

# localhost:5000/quizNum/responseNum - responseNum (not unique) would be its order in the Quiz	