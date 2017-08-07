from app import app, db
from flask import jsonify, request, abort, render_template
from .models import Quiz, Result


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/quiz/', methods=['GET'])
def quiz():
	quizzes = Quiz.query.all()
	return render_template('all_quizzes.html', quizzes=quizzes)


@app.route('/quiz/', methods=['POST']) # Post new quiz
def post_quiz():	
	if not request.json or not 'name' in request.json:
		abort(400)
	q = Quiz(name = request.json.get('name', 'Default'))
	db.session.add(q)
	db.session.commit()
	return str(q.q_id)

@app.route('/quiz/<int:quiz_id>/', methods=['GET']) # list of results by ID
def get_results(quiz_id):
	q = Quiz.query.get(quiz_id)
	if not q:
		abort(400)
	return render_template('quiz_results.html', quiz=q, results=q.results)
		

@app.route('/quiz/<int:quiz_id>/', methods=['POST']) #post new result to existing quiz
def post_result(quiz_id): 
	if not request.json or not 'body' in request.json:
		abort(400)
	q = Quiz.query.get(quiz_id)	
	if not q:
		abort(400)
	result = Result(relational_id = request.json['relational_id'], body=request.json['body'], author=q, quiz_id=q.q_id)
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
	return result.body 



# # Optional - Delete Quizzes, Results