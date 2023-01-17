# QUIZSEF
#### Video Demo: 
#### Description:

Quizsef is a web-based quiz application made for teachers and students. Teachers can use Quizsef to make exams
for students to answer, and view student submissions of each of their exams. Students can use QUizsef to browse
all available exams and submit answers for any of those exams.

Technologies used:
	Python: Main programming language for handling authentication, sessions, correctness of submitted
			forms, storing information in the database, rendering templates, redirects and more.
			The decision to choose python was easy for me, the main deciding factor was that I worked with
			python in the previous CS50 Problem Set, using the Flask framework, other reasons may include
			simplicity of python code and it being beginner friendly, Flask itself and others.

	Flask: The main framework used for making the web application.
	
	HTML, CSS: You know.
	
	VSCode: Easy to use editor, many extensions to choose from and make my code writing experience much easier.

	Google Chrome: Google Chrome.

	Windows 11: It's what I have 🤷.


Websites that hepled me:
	w3schools.com: A really good source to learn different languages, with examples and a built-in compiler.
	
	palletsprojects.com/p/flask: Flasks' documentation.

	stackoverflow.com: Search google for help when you have errors or bugs in your code, and you'll probably
					end up here with a very specific answer.

The following files can be found inside of the main directory:

==> run.py

	This file is used to run the application, that is by running flask.
	It imports app variable from __init__.py inside the app's package.
	Run this file to start the application.


==> /quizsef >> This folder contains quizsef package.
	||
	||
	||
	|_> /static >> Contains appplication icon(favicon.ico) and CSS styling file(styles.css).
		||
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
		||
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
	||		Tables:
	||			answers:	id -- questionid -- answer -- isright
	||
	||			exams:	id -- user_id -- name -- nquestions -- unique_submissions -- puplishdate
	||					puplishtime -- deadlinedate -- deadlinetime
	||
	||			history:	id -- teacher_name -- exam_name -- student_name -- nqiestions --
	||					correct_answers -- date -- time
	||
	||			questions: id -- examid -- question_number -- question
	||
	||			users:	id -- username -- email -- hash -- isteacher
	||			
	||
	||
	|_> /utils.py:

	||	This file contains 3 helper methods,
	||	( apology ):
	||		This method is responsible for rendering apology templates.
	||	( result ):
	||		This method is responsible for rendering result template.
	||	( login_required ):
	||		This decorator is called before routes methods to require login. If user calls the decorated
	||		URL without being loggd in, he is redirected to login page
	||
	||
	|_> /routes.py:
	
		This is the main file that contains most of the work. It contains routes for all urls.
		The code that is written in this file is pretty much self explanatory. and is filled
		with helping comments.
		
		( "/" ), login_required:
		POST	 GET
		 ||	 ||
		 ||	 |_> renders: "teacherindex.html"
		 ||			  "studentindex.html"
		 ||		
		 |_> handles deletion, redirects to: "/"
	
			
		( "/makeexam" ), login_required:
		POST	 GET
		 ||	 ||
		 ||	 |_> renders: "makeexam.html"
		 ||
		 |_> handles correctness of submitted exam, renders: "makequestions.html"
	
	
		( "/makequestions" ), login_required:
		POST	 GET
		 ||	 ||
		 ||	 |_> renders: apology(), you can only reach here from "/makeexma"
		 ||
		 |_> handles correctness of submitted questions, redirects to: "/"
	
	
		( "/<teacherid>/<examname>" ), login_required:
		POST	 GET
		 ||	 ||
		 ||	 |_> handles storage of specified exam data, renders: "exam.html"
		 ||
		 |_> handles correctness of submitted answers, renders: result(), with the number of
			correct answers
	
	
		( "/history" ), login_required:
			 GET
		 	 ||
			 |_> handles storage of submitted answers history, renders: "history.html"
	
	
		( "/login" ):
		POST	 GET
		 ||	 ||
		 ||	 |_> renders: "login.html"
		 ||
		 |_> handles correctness of submitted login credentials, redirects to: "/"


		( "logout" ):
			 GET
			 ||
			 |_> clears session, redirects to: "/"


		( "/register" ):
		POST	 GET
		 ||	 ||
		 ||	 |_> renders: "register.html"
		 ||
		 |_> handles correctness of submitted register credentials, stores user in DB,
		 	redirects to: "/"


		( "/settings" ), login_required:
		POST	 GET
		 ||	 ||
		 ||	 |_> renders: "settings.html"
		 ||
		 |_> handles correctness of submitted reset password form, updates password in Db,
			redirects to: "/"
		 

==> README.md: ( THIS FILE )





return render_template("THIS_WAS_CS50.html")