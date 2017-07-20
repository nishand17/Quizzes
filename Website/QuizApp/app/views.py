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
	return s	


@app.route('/quiz/', methods=['POST'])
def postQuiz():	
	if not request.json or not 'name' in request.json:
		abort(400)
	q = Quiz(name = request.json.get('name', 'Default'))
	db.session.add(q)
	db.session.commit()
	return q.name

# @app.route('/quiz/<int:quiz_id>/', methods=['GET']) # list of results by ID

# @app.route('/quiz/<int:quiz_id>/', methods=['POST']) #post new result to existing quiz

# @app.route('/quiz/<int:quiz_id>/<int:result_id>/', methods=['GET']) # show specific result

# # Optional - Delete Quizzes, Results