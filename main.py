from GoogleAPI import google_sender, google_execution
from grade_classes import Category, Question, is_float, is_int
from jinja2 import Environment, FileSystemLoader, select_autoescape
import requests

def grade(gradeID, name):
	template_data = google_execution.main('getTemplateData',[gradeID])
	response_data = google_execution.main('getResponsesData', [gradeID])
	master_data = google_execution.main('getMasterData', None)
	question_indices = [x for x in range(len(template_data)) if template_data[x][0] == 'Question']
	for student_row in range(1, len(response_data)): # loops through each student and their responses
		categories = [] 
		if response_data[student_row][0].split(' ')[-1] == "GRADED": # Makes sure not to grade something twice 
			continue
		for question_index, response_place in zip(question_indices, range(3, 3+len(question_indices))): # loops though questions and responses
			if template_data[question_index][5].split(',')[0] == 'checkbox': # special cases for checkboxes because it has several answers/repsonses (that's the only difference, but more has to be accounted for - see the elif for more documentation)
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
				imagePaths = template_data[question_index][9].split(',')
				imagePaths = [x.strip(' ') for x in imagePaths]
				imageLinks = []
				for path in imagePaths:
					imageLinks.append(path)
					
				q = Question(student_answers_string, correct_answers_string, points_given, checkbox_category, checkbox_name, imageLinks)
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
				if is_float(correct_answer): # partial credit floats
					student_float = float(student_answer)
					correct_float = float(correct_answer)
					partial = float(template_data[question_index][8])
					low_bound = abs(correct_float) - partial
					high_bound = abs(correct_float) + partial
					if student_float == correct_float: 
						points+=1
					else:
						if low_bound <= abs(student_float) <= high_bound: 
							points+=1 			    		  	
				elif is_int(correct_answer): #partial credit ints
					student_int = int(student_answer)
					correct_int = int(correct_answer)
					partial = float(template_data[question_index][8])
					low_bound = abs(correct_int) - partial
					high_bound = abs(correct_int) + partial
					if student_int == correct_int:
						points+=1
					else:
						if low_bound <= abs(student_int) <= high_bound: 
							points+=1
				    		
				else: 
					if student_answer == correct_answer: # otherwise, an exact answer is required
						points+=1
				question_category = template_data[question_index][7]		
				question_name = template_data[question_index][1]
				imagePaths = template_data[question_index][9].split(',') # imagePaths are saved in the question structure to be accessed by the HTML rendering lib
				imagePaths = [x.strip(' ') for x in imagePaths]
				imageLinks = []
				for path in imagePaths:
					imageLinks.append(path)
				q = Question(student_answer, correct_answer, points, question_category, question_name, imageLinks)
				category_gen = [x for x in range(len(categories)) if categories[x].name == question_category] # finds correct category for this question - category_gen has max length 1 because each quiz only has 1 category of each name (duh)
				if len(category_gen) == 0: # new category created
					c = Category(question_category)
					c.numQuestions+=1
					c.totalPoints+=points
					c.questions.append(q)
					categories.append(c)
				else: # adds question to existing
					category_index = category_gen[0]
					categories[category_index].numQuestions+=1
					categories[category_index].totalPoints+=points
					categories[category_index].questions.append(q)
		totalQuestions = 0;
		totalCorrect = 0;				
		for cat in categories: #adds percentage to categories and prints raw grades
			cat.correctPercentage = round((float(cat.totalPoints)/float(cat.numQuestions)*100), 2)
			totalQuestions+= cat.numQuestions
			totalCorrect+= cat.totalPoints
			# commented below is for debugging purposes
			#question_string = '' 
			# for category_q in cat.questions: 
			# 	linkString = ''
			# 	for link in category_q.graphicLinks:
			# 		linkString += link + ", "
			# 	question_string += "Question Name: " + category_q.name + " Student Answer: " + category_q.studentAnswer + " Correct Answer: " + category_q.correctAnswer + " Points Given: " + str(category_q.pointsGiven) + " Links: " + linkString + "\n"
			# #print "CategoryName: ", cat.name, " CategoryNumQ: ", cat.numQuestions, " Total Points: ", cat.totalPoints, "Percentage", cat.correctPercentage, " Questions\n", question_string, 	 
		
		google_execution.main('setFinalScore', [gradeID, student_row, totalCorrect, totalQuestions]) # modifies grade spreadsheet
		google_execution.main('setResponseAsGraded', [gradeID, student_row])

		templateLoader = FileSystemLoader(searchpath="./templates")
		templateEnv = Environment(loader=templateLoader)
		template = templateEnv.get_template("index.html")
		outputText = template.render(name=name, final_score=totalCorrect, total_questions=totalQuestions, categories=categories) # renders HTML template for each result
		
		if master_data[gradeID][7].lower().strip(' ') == 'email': 
			google_sender.run(response_data[student_row][2], ('Your Grade Report for the quiz: ' + name), outputText)
		elif master_data[gradeID][7].lower().strip(' ') == 'id':
			print 'Posting result to website'
			url = 'http://localhost:5000/quiz/%s/'%(master_data[gradeID][8])
			rel_id = int(response_data[student_row][2])
			grade_response = requests.post(url=url, json={'body': outputText, 'relational_id': rel_id}) #posts specific result to quiz with correct global ID

option = raw_input("Enter what you wish to do (send, create, view, grade)\n")

if option == 'send':	
	templateLoader = FileSystemLoader(searchpath="./templates")
	templateEnv = Environment(loader=templateLoader)
	template = templateEnv.get_template("quiz_send.html")
	quiz_list = google_execution.main('getSendList', None)
	print "Here are your quizzes that can be sent out. If the quiz you wish to send out isn't here, make sure to fill out the master Google Sheet with the required information (recipients and form links)"
	for index in range(len(quiz_list)):
		print index+1, "- " + quiz_list[index]
	sendID = input("Enter the quiz number ")
	if sendID not in range(1, len(quiz_list)+1):
		print "Sorry, there is no quiz with that ID"
		exit()
	send_info = google_execution.main('getSendInfo', [sendID]) 
	matrix, link, description, name = send_info['respondents'], send_info['formUrl'], send_info['description'], send_info['title']	
	master_data = google_execution.main('getMasterData', None)
	del matrix[0]
	print 'Sending...'
	for email_row in matrix:
		response_id = None
		if master_data[sendID][7].lower().strip(' ') == "id":
			template_data = google_execution.main('getTemplateData', [sendID])
			last_id = template_data[1][10]
			if str(last_id).strip(' ') == '':
				response_id = 1
			else: 
				response_id = int(last_id) + 1 
		google_execution.main('addIDToTemplate', [sendID, response_id])
		
		
		results_url = master_data[sendID][9]
		outputText = template.render(name=name, description=description, id=response_id, link=link, results_url=results_url)
		google_sender.run(email_row[0], "Google Quiz Invitation via QuizApp", outputText)	

elif option == 'create' or option == 'view':
	create_list = google_execution.main('getCreateList', None)
	print "Here are the current quizzes you can view and create"
	for index in range(len(create_list)):
		print index+1, "- " + create_list[index]
	viewID = input("Enter the number of the corresponding quiz")	
	if viewID not in range(1, len(create_list)+1):
		print "Sorry, there is no quiz with that ID"
		exit()
	print 'Creating quiz... please wait'	
	quiz_info = google_execution.main('readFromSheet', [viewID])	
	print "Published Link:", quiz_info[0], "\nEdit Link:", quiz_info[1]
	#post quiz to website
	master_data = google_execution.main('getMasterData', None)
	if master_data[viewID][7].lower().strip(' ') == 'id':
		quiz_name = str(master_data[viewID][0])
		req_response = requests.post(url='http://localhost:5000/quiz/', json={'name': quiz_name})
		quiz_url = 'http://localhost:5000/quiz/'+str(req_response.text)+'/'
		google_execution.main('setResultsPage', [quiz_url, quiz_info[1], viewID])
		global_id = int(req_response.text)
		google_execution.main('setGlobalIDForQuiz', [viewID, global_id])
		print 'Published Quiz to Website'

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
