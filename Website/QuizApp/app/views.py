from app import app, db
from flask import jsonify, request, abort
from .models import Quiz, Result


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/quiz/', methods=['GET'])
def quiz():
	quizzes = Quiz.query.all()
	s = ''
	for quiz in quizzes:
		s+= quiz.name
	return s	# TEMPLATE


@app.route('/quiz/', methods=['POST'])
def post_quiz():	
	if not request.json or not 'name' in request.json:
		abort(400)
	q = Quiz(name = request.json.get('name', 'Default'))
	db.session.add(q)
	db.session.commit()
	return q.name + " " + str(q.q_id)

@app.route('/quiz/<int:quiz_id>/', methods=['GET']) # list of results by ID
def get_results(quiz_id):
	q = Quiz.query.get(quiz_id)
	if not q:
		abort(400)
	s = ''	
	for result in q.results:
		s+= (str(result.relational_id) + " " + result.body +  " " + str(result.author.q_id) + "\n")
	return s # TEMPLATE
		

@app.route('/quiz/<int:quiz_id>/', methods=['POST']) #post new result to existing quiz
def post_result(quiz_id): 
	if not request.json or not 'body' in request.json:
		abort(400)
	q = Quiz.query.get(quiz_id)	
	if not q:
		abort(400)
	result = Result(relational_id = request.json['relational_id'], body=request.json['body'], author=q)
	db.session.add(result)
	db.session.commit()
	return result.body + " " + str(result.relational_id) + " " + str(result.author) + " " + str(result.quiz_id)


@app.route('/quiz/<int:quiz_id>/<int:result_id>/', methods=['GET']) # show specific result
def result(quiz_id, result_id):
	q = Quiz.query.get(quiz_id)
	results = q.results
	queried_result = None
	for result in results:
		if str(result.relational_id) == str(result_id):
			queried_result = result
			break
	return result.body + ' ' + str(result.relational_id)	 # HTML TEMPLATE



# # Optional - Delete Quizzes, Results