import google_sender

message = """\
		<html>
		  <head></head>
		  <body>
		    <p>Hi!<br>
		       How are you?<br>
		       Here is the <a href="http://www.python.org">link</a> you wanted.
		    </p>
		  </body>
		</html>
		"""

google_sender.run("nishand@gmail.com", "nishandsouza@sfhs.com", "Wow", message)		