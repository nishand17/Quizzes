import google_sender
import google_execution

option = raw_input("Enter what you wish to do (send, create, view, grade)\n")

if option == 'send':	
	# TODO validate form info
	quiz_list = google_execution.main('getSendList', None)
	print "Here are your quizzes that can be sent out. If the quiz you wish to send out is no"
	for index in range(len(quiz_list)):
		print index+1, "- " + quiz_list[index]
	sendID = input("Enter the quiz number ")
	if sendID not in range(1, len(quiz_list)+1):
		print "Sorry, there is no quiz with that ID"
		exit()

	send_info = google_execution.main('getSendInfo', [sendID]) #TODO add parameter support
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
		google_sender.run("nishand@gmail.com", email_row[0], "Google Quiz Invitation v2", message)		
elif option == 'create' or option == 'view':
	create_list = google_execution.main('getCreateList', None)
	print "Here are the current lists you can view and create"
	for index in range(len(create_list)):
		print index+1, "- " + create_list[index]
	viewID = input("Enter the number of the corresponding quiz")	
	if viewID not in range(1, len(create_list)+1):
		print "Sorry, there is no quiz with that ID"
		exit()
	quiz_info = google_execution.main('readFromSheet', [viewID])	
	print "Published Link:", quiz_info[0], "\nEdit Link:", quiz_info[1]

	