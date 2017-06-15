import google_sender
import google_execution

send_info = google_execution.main('getSendInfo')
matrix, link, description, name = send_info['respondents'], send_info['formUrl'], send_info['description'], send_info['title']
#matrix = [row for row in matrix if row[0][0] is not 'Emails'] - smarter way to delete Emails row
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
	