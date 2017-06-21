# Instructor Guide for QuizApp
As an instructor, the process to create a quiz (Steps 1-3), send it to students, and grade feedback is as follows
** Note: I assume here that you have finished the steps in configuration.md to setup the project **

1. Google Drive Setup
	* A recommended file layout for QuizApp is as follows - A master folder called "Quizzes" will contain the sheet "QuizSheetMaster" and several folders for every Quiz you make. Each Quiz folder will contain a Graphics directory, the quiz creator sheet, the quiz recipients sheet, and the quiz response sheet (which is made after the quiz is created by the script). *A sample project layout will be provided to you*
	* To start the quiz maker process, columns A and B of a new row must be filled with the QuizTitle and template link respectively
2. QuizApp run
	* Navigating to the QuizApp directory in your computer on Terminal/Command Prompt, run `python test.py create` and select the number of the Quiz you wish to create
	* After about a minute, the program will output the form link and edit link to the console and save these links to the "QuizSheetMaster" Google Sheet
3. Google Quiz Setup
	* Once you have the Quiz Edit Link, open a browser and paste the edit link to get to the Quiz Creator's console. 
	* To complete the setup process, 2 settings need to be manually adjusted
	* Under Settings->Quizzes, set `Release Grade` to `Immediately after each submission` and check the three boxes at the bottom (Missed Questions, Correct Answers, Point Values) and save
	* Under Responses (in the same bar as Questions), click on the green spreadsheet logo and create a new response spreadsheet. Copy this link to the "QuizSheetMaster" in the ResponsesLink column
4. 	Sending the sheet to students
	* In your Quiz-x folder, create a Google Sheet containing the emails of the intended recipients of the sheet and paste this link the the corresponding row of "QuizSheetMaster" under "RecipientsSheetLink"
	* Navigating back to the QuizApp directory in your console, run `python test.py send` and select the number of the Quiz you want to send. Message IDs will be outputted to the console
5. Grading (TBA)	

