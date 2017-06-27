import google_sender
import google_execution

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
	categories = []
	for student_row in range(1, len(response_data)):
		for index, place in zip(question_indices, range(3, 3+len(question_indices))):
			if template_data[index][5].split(',')[0] == 'checkbox':
				points_per_check = float(1)/len(template_data[index][6].split(','))
				student_answer_list = response_data[student_row][place].split(',')
				student_answers = [x.strip(' ') for x in student_answer_list]
				print student_answer_list
				continue



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
			  	<table bordercolor="#c29df9" frame="box" bgcolor="#EDE7F6" style="border-collapse: separate; border-spacing: 30px">
			  		<th><h1>Fill out "%s"</h1></th>
			  		<tr>
			  			<td align="center">I've invited you to fill out my form: %s</td>
			  		</tr>
			  		<tr>
			  			<td align="center">Click the button below to complete the form</td>
			  		</tr>
			  		<tr>
			  			<td align="center"><a href=%s><button style="background-color: #673AB7; border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px">Complete Form</button></a></td>
			  		</tr>
			  	</table>	
			  	</center>   
			  </body>
			</html>
			"""%(name, description, link)

	for email_row in matrix:
		google_sender.run("nishand@sfhs.com", email_row[0], "Google Quiz Invitation v2", message)		
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


	