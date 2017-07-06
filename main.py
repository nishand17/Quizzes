import google_sender
import google_execution
from grade_classes import Category, Question, is_float, is_int
from jinja2 import Environment, FileSystemLoader, select_autoescape

def grade(gradeID, name):
	'''
	1. Retrieve both template and response data 
	2. Run through each question keeping track of studentAnswer, correctAnswer, isCorrect, category
	3. Keep track of Categories including categoryName, totalNumQuestions, numCorrect
	categoryArr has questionArr with an array of its questions
	put this all in an html template and google_sender per studentAnswer (Overview of quiz (# correct total, small category breakdown, chart), detailed by category)
	Tuesday: Grading process
	Wednesday: Email mockups

	TODO - Make sure we don't grade something twice (already graded checker)
	'''
	template_data = google_execution.main('getTemplateData',[gradeID])
	response_data = google_execution.main('getResponsesData', [gradeID])
	question_indices = [x for x in range(len(template_data)) if template_data[x][0] == 'Question']
	for student_row in range(1, len(response_data)):
		categories = []
		for question_index, response_place in zip(question_indices, range(3, 3+len(question_indices))):
			if template_data[question_index][5].split(',')[0] == 'checkbox': # special cases for checkboxes because it has several answers/repsonses
				points_per_check = float(1)/len(template_data[question_index][6].split(','))
				student_answer_list = response_data[student_row][response_place].split(',')
				student_answers = [x.strip(' ') for x in student_answer_list]
				correct_answers_list = template_data[question_index][6].split(',')
				correct_answers = [x.strip(' ') for x in correct_answers_list]
				points_given = 0
				for choice in range(len(template_data[question_index][6].split(','))):
					try:
						if student_answers[choice] in correct_answers:
							points_given+=points_per_check
					except IndexError:
						print ""
				checkbox_category = template_data[question_index][7]
				checkbox_name = template_data[question_index][1]
				student_answers_string = ', '.join(student_answers)
				correct_answers_string = ', '.join(correct_answers)
				q = Question(student_answers_string, correct_answers_string, points_given, checkbox_category, checkbox_name)
				category_gen = [x for x in range(len(categories)) if categories[x].name == checkbox_category]
				if len(category_gen) == 0:
					c = Category(checkbox_category)
					c.numQuestions+=1
					c.totalPoints+=points_given
					c.questions.append(q)
					categories.append(c)
				else:
					category_index = category_gen[0]
					categories[category_index].numQuestions+=1
					categories[category_index].totalPoints+=points_given
					categories[category_index].questions.append(q)		
				continue
			else:
				student_answer = response_data[student_row][response_place].strip(' ')
				correct_answer = template_data[question_index][6].strip(' ')
				points = 0
				if is_float(correct_answer):
					student_float = float(student_answer)
					correct_float = float(correct_answer)
					partial = float(template_data[question_index][8])
					low_bound = abs(correct_float) - partial
					high_bound = abs(correct_float) + partial
					print partial, low_bound, high_bound
					if student_float == correct_float: 
						points+=1
					else:
						if low_bound <= abs(student_float) <= high_bound: 
							points+=0.5 
				    		  	
				elif is_int(correct_answer):
					student_int = int(student_answer)
					correct_int = int(correct_answer)
					partial = float(template_data[question_index][8])
					low_bound = abs(correct_int) - partial
					high_bound = abs(correct_int) + partial
					print partial, low_bound, high_bound
					if student_int == correct_int:
						points+=1
					else:
						if low_bound <= abs(student_int) <= high_bound: 
							points+=0.5
													
				    		
				else: 
					if student_answer == correct_answer: 
						points+=1
				question_category = template_data[question_index][7]		
				question_name = template_data[question_index][1]
				q = Question(student_answer, correct_answer, points, question_category, question_name)
				category_gen = [x for x in range(len(categories)) if categories[x].name == question_category]
				if len(category_gen) == 0:
					c = Category(question_category)
					c.numQuestions+=1
					c.totalPoints+=points
					c.questions.append(q)
					categories.append(c)
				else:
					category_index = category_gen[0]
					categories[category_index].numQuestions+=1
					categories[category_index].totalPoints+=points
					categories[category_index].questions.append(q)
		totalQuestions = 0;
		totalCorrect = 0;				
		for cat in categories: 
			cat.correctPercentage = round((float(cat.totalPoints)/float(cat.numQuestions)*100), 2)
			totalQuestions+= cat.numQuestions
			totalCorrect+= cat.totalPoints

			question_string = ''
			for category_q in cat.questions: 
				question_string += "Question Name: " + category_q.name + " Student Answer: " + category_q.studentAnswer + " Correct Answer: " + category_q.correctAnswer + " Points Given: " + str(category_q.pointsGiven) + "\n"
			print "CategoryName: ", cat.name, " CategoryNumQ: ", cat.numQuestions, " Total Points: ", cat.totalPoints, "Percentage", cat.correctPercentage, " Questions\n", question_string, 	
		templateLoader = FileSystemLoader(searchpath="./templates")
		templateEnv = Environment(loader=templateLoader)
		TEMPLATE_FILE = "index.html"
		template = templateEnv.get_template(TEMPLATE_FILE)
		outputText = template.render(name=name, final_score=totalCorrect, total_questions=totalQuestions, categories=categories)
		google_sender.run('nishand@gmail.com', response_data[student_row][1], ('Your Grade Report for '+name), outputText)



option = raw_input("Enter what you wish to do (send, create, view, grade)\n")

if option == 'send':	
	# TODO validate form info
	quiz_list = google_execution.main('getSendList', None)
	print "Here are your quizzes that can be sent out. If the quiz you wish to send out isn't here, make sure to fill out "
	for index in range(len(quiz_list)):
		print index+1, "- " + quiz_list[index]
	sendID = input("Enter the quiz number ")
	if sendID not in range(1, len(quiz_list)+1):
		print "Sorry, there is no quiz with that ID"
		exit()

	send_info = google_execution.main('getSendInfo', [sendID]) 
	matrix, link, description, name = send_info['respondents'], send_info['formUrl'], send_info['description'], send_info['title']
	del matrix[0]
	message = """\
			<html>
			  <head></head>
			  <body>
			  <center>
			  <div style="box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);">
			  	<table bordercolor="#c29df9" frame="box" bgcolor="#EDE7F6" style="border-collapse: separate; border-spacing: 15px;">
			  		<th bgcolor = "#673AB7" style="color: #f7faff;"><h1>Fill out %s</h1></th>
			  		<tr>
			  			<td align="left" width="400" bgcolor="#fdfdfd" style="padding:30px; color: #333333;"><b>I've invited you to fill out my form: %s<b></td>
			  		</tr>		  		
			  		<tr>
			  			<td align="center" style="padding:10px; "><a href=%s><button style="background-color: #673AB7; border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px;">Complete Form</button></a></td>
			  		</tr>
			  		<tr>
			  			<td><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google_2015_logo.svg/2000px-Google_2015_logo.svg.png" width="75px" height="25px"></td>
			  		</tr>			  		
			  	</table>	
	  		  </div>
			  </center>   
			  </body>
			</html>
			"""%(name, description, link)

	for email_row in matrix:
		google_sender.run("nishand@gmail.com", email_row[0], "Google Quiz Invitation via QuizApp", message)		
elif option == 'create' or option == 'view':
	create_list = google_execution.main('getCreateList', None)
	print "Here are the current quizzes you can view and create"
	for index in range(len(create_list)):
		print index+1, "- " + create_list[index]
	viewID = input("Enter the number of the corresponding quiz")	
	if viewID not in range(1, len(create_list)+1):
		print "Sorry, there is no quiz with that ID"
		exit()
	quiz_info = google_execution.main('readFromSheet', [viewID])	
	print "Published Link:", quiz_info[0], "\nEdit Link:", quiz_info[1]
elif option == 'grade':
	grade_list = google_execution.main('getGradeList', None)
	print "Here are the current quizzes you can grade"
	for index in range(len(grade_list)):
		print index+1, "- " + grade_list[index]
	gradeID = input("Enter the number of the corresponding quiz")
	if gradeID not in range(1, len(grade_list)+1):
		print "Sorry, there is no quiz with that ID"
		exit()
	grade(gradeID, grade_list[gradeID-1])	


	
