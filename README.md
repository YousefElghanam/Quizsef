# QUIZSEF
#### Video Demo: 
#### Description:

Quizsef is a web-based quiz application made for teachers and students. Teachers can use Quizsef to make exams
for students to answer, and view student submissions of each of their exams. Students can use QUizsef to browse
all available exams and submit answers for any of these exams.

The following files can be found inside of the main directory:

==> run.py

	This file is used to run the application, that is by running flask.
	It imports app variable from __init__.py inside the app's package.


==> /quizsef >> This folder contains quizsef package.
	||
	||
	||
	|_> /static >> Contains appplication icon(favicon.ico) and CSS styling file(styles.css).
	||	||
	||	||
	||	|_> /styles.css:
	||
	||		Contains styling for the navigation bar
	||		Contains styling for answer fields in makeexam page.
	||		Contains styling for other layout elements.
	||		Contains styling for horizontal scroll bar.
	||
	||
	|_> /templates >> Contains all pages html files.
	||	||
	||	||
	||	|_> /apology.html:
	||
	||	||	This page shows an image (of a cat) with appropriate error message.
	||	||
	||	||
	||	|_> /exam.html:
	||
	||	||	This page shows an exam containing a number of questions and answers for each question to
	||	||	choose from.
	||	||
	||	||
	||	|_> /history.html:
	||
	||	||	This page shows a table of history of student submissions for currently logged in teacher.
	||	||
	||	||
	||	|_> /layout.html:
	||
	||	||	This page has all the main layout elements found in all other html pages, navigation bar,
	||	||	navigation bar, navigation bar elements, application name, Made by Yousef Elghanam and
	||	||	Hi message.
	||	||
	||	||
	||	|_> /login.html:
	||
	||	||	This page shows the login form.
	||	||
	||	||
	||	|_> /makeexam.html:
	||
	||	|| 	This page can be accessed by a teacher, and it shows a form to enter exam name, number of
	||	||	questions, puplish time and deadline time. It also has a button to continue making
	||	||	questions for this exam.
	||	||
	||	||
	||	|_> /makequestions.html:
	||
	||	||	This page can be accessed after entering correct input in makeexam page. It shows a form
	||	||	of fields to enter questions and 4 answers and a right answer for each question.
	||	||
	||	||
	||	|_> /register.html:
	||
	||	||	This page shows a form to register for an account.
	||	||
	||	||
	||	|_> /result.html:
	||
	||	||	This page shows an image (of a happy cat) with the result of submitted answers.
	||	||
	||	||
	||	|_> /settings.html:
	||
	||	||	This page shows password reset form.
	||	||
	||	||
	||	|_> /studentindex.html:
	||
	||	||	This page is the homepage for students. It shows a table of all available exams, their
	||	||	puplish and deadline times and buttons to start them.
	||	||
	||	||
	||	|_> /teacherindex.html:
	||
	||		This page is the homepage for teachers. It shows the teachers available exams, their
	||		puplish and deadline times. It also has button in navigation bar linking to make exam page
	||		and history page.
	||
	||
	||
	|_> /__init__.py:

	||	This file contains flask's app configuration, session settings and type, database configuration.
	||
	||
	|_> /quizsef.db:

	||	Database file.
	||
	||
	|_> /utils.py:

	||	This file contains 3 helper methods,
	||	( apology ):
	||		This method is responsible for rendering apology templates.
	||	( result ):
	||		This method is responsible for rendering result template.
	||	( login_required ):
	||		This decorator is called before routes methods to require login.
	||
	||
	|_> /routes.py:
	
	||	This is the main file