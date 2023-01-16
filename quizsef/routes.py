from quizsef import db, app
from flask import render_template, session, request, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from quizsef.utils import login_required, apology, result

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]

        # If user is teacher
        isteacher = db.execute("SELECT isteacher FROM users WHERE id = ?", session["user_id"])[0]["isteacher"]
        
        if isteacher == 1:
            # Store rows of exams table
            exams = db.execute("SELECT * FROM exams WHERE user_id = ?", session["user_id"])
            
            return render_template("teacherindex.html", exams=exams, isteacher=isteacher, username=username)
        
        # If user is student
        else:
            # Store rows of exams table
            exams = db.execute("SELECT * FROM exams")
            
            # Add exam's teacher name to "exams"
            for i, exam in enumerate(exams):
                exams[i]["teacher"] = db.execute("SELECT username FROM users WHERE id = ?", exam["user_id"])[0]["username"]
            
            return render_template("studentindex.html", exams=exams, username=username)
        
    # Handle deletion of exams
    else:
        db.execute("BEGIN TRANSACTION")
        
        examname = request.form.get("delete")
        examid = db.execute("SELECT id FROM exams WHERE user_id = ? AND name = ?", (session["user_id"]), (examname))[0]["id"]
        nquestions = db.execute("SELECT nquestions FROM exams WHERE id = ?", (examid))[0]["nquestions"]
        questions = db.execute("SELECT id FROM questions WHERE examid = ?", (examid))
        
        # Delete exam, questions and answers
        db.execute("DELETE FROM exams WHERE id = ?", (examid))
        db.execute("DELETE FROM questions WHERE examid = ?", (examid))
        for q in range(nquestions):
            questionid = questions[q]["id"]
            db.execute("DELETE FROM answers WHERE questionid = ?", (questionid))
            
        db.execute("COMMIT TRANSACTION")
        
        return redirect("/")

@app.route("/makeexam", methods=["GET", "POST"])
@login_required
def make_exam():
    
    # User reaches route via POST
    if request.method == "POST":
        
        # Ensure all fields are filled
        
        if not request.form.get("examname"):
            return apology("must provide a name for the exam")
        
        for name in db.execute("SELECT name FROM exams WHERE user_id = ?", session["user_id"]):
            if request.form.get('examname') == name["name"]:
                return apology("exam name already exists")
        
        # Ensure number of questions is entered and is between 1 and 25
        if not request.form.get("nquestions"):
            return apology("must provide number of questions (a positive integer)", 403)

        try:
            if int(request.form.get("nquestions")) < 1 or int(request.form.get("nquestions")) > 25:
                return apology("must provide a positive integer between (1-25)", 403)
        except (TypeError, ValueError):
            return apology("number of questions must be an integer number (1-25)", 403)

        # Ensure deadline time is entered
        if not request.form.get("deadlinedate") or not request.form.get("deadlinetime"):
            return apology("must provide puplish and deadline dates and times", 403)

        # Store examdata, to transfer it to questions page
        examdata = {
            "userid": session["user_id"],
            "examname": request.form.get("examname"),
            "nquestions": request.form.get("nquestions"),
            "puplishdate": request.form.get("puplishdate"),
            "puplishtime": request.form.get("puplishtime"),
            "deadlinedate": request.form.get("deadlinedate"),
            "deadlinetime": request.form.get("deadlinetime")
            }
        session["examdata"] = examdata
                
        # Go to make question page after submitting
        return render_template("makequestions.html", nquestions=int(examdata["nquestions"]))
        
    # User reaches route via GET
    else:
        # Check if user is teacher or not
        if db.execute("SELECT isteacher FROM users WHERE id = ?", session["user_id"])[0]["isteacher"] == 1:
            return render_template("makeexam.html")
        else:
            return apology("You must be a teacher to make an exam")
    
    
    
@app.route("/makequestions", methods=["GET", "POST"])
@login_required
def makequestions():
    # User reaches route via POST
    if request.method == "POST":
        
        examdata = session["examdata"]
        
        nquestions = int(examdata["nquestions"])
        
        db.execute("BEGIN TRANSACTION")
        # variable to make line 127 excute only once per exam
        executed = False
        # Loop through questions
        for q in range(1, nquestions + 1):
            
            # Ensure question was entered
            if not request.form.get("question{}".format(q)):
                return apology("Must fill all question fields", 403)
            
            # Ensure the right answer was entered
            if not request.form.get("rightanswer{}".format(q)):
                return apology("Must fill all right answer fields", 403)
            else:
                rightanswer = request.form.get("rightanswer{}".format(q))

            # Ensure answers were entered
            mysterious_flag = True
            for ans in range(1, 5):
                if not request.form.get("answer{}-{}".format(q, ans)):
                    return apology("Must fill all answer fields at once", 403)
                # Ensure the right answer matches one of the answers
                if request.form.get("answer{}-{}".format(q, ans)) == request.form.get("rightanswer{}".format(q)):
                    mysterious_flag = False
            if mysterious_flag:
                return apology("The right answer of question-{} doesn't match any of the answers".format(q))
                
            # Store exam in DB ( exams, questions, answers )
            
            # Insert into exams
            if not executed:
                db.execute("INSERT INTO 'exams' ('user_id', 'name', 'nquestions', 'deadlinedate', 'deadlinetime') VALUES (?, ?, ?, ?, ?)",
                        (examdata["userid"]), (examdata["examname"]), (examdata["nquestions"]), (examdata["deadlinedate"]), (examdata["deadlinetime"]))
                executed = True
                # Remember last inserted exam id
                examid = db.execute("SELECT last_insert_rowid()")[0]["last_insert_rowid()"]

            # Insert into questions
            db.execute("INSERT INTO 'questions' ('examid', 'question_number', 'question') VALUES (?, ?, ?)", (examid), 
                       (q), (request.form.get("question{}".format(q))))
            
            # Remember last inserted question id
            questionid = db.execute("SELECT last_insert_rowid()")[0]["last_insert_rowid()"]
            #db.execute("SELECT id FROM questions WHERE examid = ?", examid)[q - 1]["id"]
            
            # Loop through answers
            for ans in range(1, 5):
                # Store answer in DB
                db.execute("INSERT INTO 'answers' ('questionid', 'answer') VALUES (?, ?)", (questionid),
                        (request.form.get("answer{}-{}".format(q, ans))))
                
                ansid = db.execute("SELECT last_insert_rowid()")[0]["last_insert_rowid()"]
                #db.execute("SELECT MAX(id) FROM answers")[0]["MAX(id)"]
                if rightanswer == request.form.get("answer{}-{}".format(q, ans)):
                    db.execute("UPDATE answers SET isright = 1 WHERE id = ?", ansid)
        db.execute("COMMIT TRANSACTION")
                    
        return redirect("/")
    
    # User reaches route via GET
    else:
        return apology("Continue to questions from Make exam page")
        # examid = session["examid"]
        # nquestions = db.execute("SELECT nquestions FROM exams WHERE id = ?", examid)[0]["nquestions"]
        # return render_template("makequestions.html", nquestions=nquestions)


@app.route("/<teacherid>/<examname>", methods=["GET", "POST"])
@login_required
def exam(teacherid, examname):
    # Check if user is not student
    if db.execute("SELECT isteacher FROM users WHERE id = ?", session["user_id"])[0]["isteacher"] == 1:
        return apology("Only students can submit exam answers")
    if request.method == "POST":
        # Get student name
        studentname = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        # Get teacher name
        teachername = db.execute("SELECT username FROM users WHERE id = ?", teacherid)[0]["username"]
        # Get exam id
        examid = db.execute("SELECT id FROM exams WHERE user_id = ? AND name = ?", (teacherid), (examname))[0]["id"]
        # Get exam's number of questions
        nquestions = db.execute("SELECT nquestions FROM exams WHERE id = ?", examid)[0]["nquestions"]
        # Number of right answers
        count = 0
        # Loop through questions
        for i in range(nquestions):
            # Ensure all fields were filled
            if not request.form.get("rightanswer{}".format(i+1)):
                return apology("Must answer all questions", 403)
            question = request.form.get("question{}".format(i+1))
            questionid = db.execute("SELECT id FROM questions WHERE question = ?", (question))[0]["id"]
            # Count right answers
            ans = request.form.get("rightanswer{}".format(i+1))
            if db.execute("SELECT isright FROM answers WHERE answer = ? AND questionid = ?", (ans), (questionid))[0]["isright"] == 1:
                count += 1
        # Record submission to history
        db.execute("INSERT INTO 'history' ('teacher_name', 'exam_name', 'student_name', 'nquestions', 'correct_answers') VALUES (?, ?, ?, ?, ?)",
                   (teachername), (examname), (studentname), (nquestions), (count))

        return result("Yew answeored {} queostions ceorrectly".format(count), count)
    
    else:
        # Get teacher name
        teachername = db.execute("SELECT username FROM users WHERE id = ?", teacherid)[0]["username"]
        # Get student name
        studentname = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        if db.execute("SELECT * FROM history WHERE teacher_name = ? AND exam_name = ? AND student_name = ?",
                      (teachername), (examname), (studentname) ):
            return apology("You submitted this exam before")
        
        # Store rows of exams table
        exams = db.execute("SELECT * FROM exams WHERE user_id = ? AND name = ?", (teacherid), (examname))
        
        # Add exam's teacher name to "exams"
        for i, exam in enumerate(exams):
            exams[i]["questions"] = []
            exams[i]["answers"] = {}
            exams[i]["teacher"] = db.execute("SELECT username FROM users WHERE id = ?", exams[i]["user_id"])[0]["username"]
            # Append questions to "exams"'s "questions" key as strings
            for n in range(exams[i]["nquestions"]):
                exams[i]["questions"].append(db.execute("SELECT question FROM questions WHERE examid = ?", exams[i]["id"])[n]["question"])
            # Add answers to "answers" dictionary
            for q, qu in enumerate(exams[i]["questions"]):
                exams[i]["answers"][qu] = []
                for x in range(4):
                    exams[i]["answers"][qu].append(db.execute("SELECT answer FROM answers WHERE questionid = ?",
                               (db.execute("SELECT id FROM questions WHERE examid = ?",
                                           (db.execute("SELECT id FROM exams WHERE user_id = ? AND name = ?",
                                                       (teacherid), (examname))[0]["id"]))[q]["id"]))[x]["answer"])
        
        return render_template("exam.html", exam=exams, teacherid=teacherid, examname=examname)


@app.route("/history")
@login_required
def history():
    """Show history of submissions of your exams"""
    
    teachername = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    
    isteacher = db.execute("SELECT isteacher FROM users WHERE id = ?", session["user_id"])[0]["isteacher"]
    # If user is a teacher
    if isteacher == 1:
        # Store rows of history table
        history = db.execute("SELECT * FROM history WHERE teacher_name = ?", teachername)
        
        return render_template("history.html", history=history)
    # If user is a student
    else:
        return apology("go back, loser")
        """Show history of student's submissions"""

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        
        # Store input
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        usertype = request.form.get("usertype")
        
        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure email was submitted
        elif not email:
            return apology("must provide email", 400)

        # Ensure username does not already exist
        elif len(db.execute("SELECT * FROM users WHERE username = ?", username)) == 1:
            return apology("username already exists", 400)

        elif len(db.execute("SELECT * FROM users WHERE email = ?", email)) == 1:
            return apology("email already exists", 400)

        # Ensure password and confirmation were submitted
        elif not password:
            return apology("must provide password", 400)

        elif not confirmation:
            return apology("must provide confirmation", 400)

        # Ensure password and confirmation match
        elif not password == confirmation:
            return apology("Confirmation does not match Password", 400)
        
        elif not usertype:
            return apology("please choose student or teacher")

        # Add user to database
        db.execute("INSERT INTO 'users' ('username','email','hash','isteacher') VALUES (?,?,?,?)",
                   (username), (email),
                    generate_password_hash(password=password, method='pbkdf2:sha256', salt_length=8), (1 if usertype=="teacher" else None))

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """ Edit settings and change password """

    # At submission
    if request.method == "POST":

        # Query database for user id
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        # Ensure old password was submitted
        if not request.form.get("old_password"):
            return apology("must provide old password", 403)

        # Ensure old password is correct
        elif not check_password_hash(rows[0]["hash"], request.form.get("old_password")):
            return apology("Wrong old password")

        # Ensure new password and its confirmation were submitted
        elif not request.form.get("new_password") or not request.form.get("confirmation"):
            return apology("must provide new password and confirmation", 403)

        # Ensure new and old passwords don't match
        elif request.form.get("new_password") == request.form.get("old_password"):
            return apology("Really ? Choose a NEW password, please")

        # Ensure password and confirmation match
        elif not request.form.get("new_password") == request.form.get("confirmation"):
            return apology("Confirmation does not match New Password", 403)

        # Update users' table with new password
        db.execute("UPDATE users SET hash = ? WHERE id = ? ",
                   generate_password_hash(password=request.form.get("new_password"), method='pbkdf2:sha256', salt_length=8),
                   session["user_id"])

        # Redirect to home page
        return redirect("/")

    # On visiting "/settings"
    else:
        # If user is teacher
        isteacher = db.execute("SELECT isteacher FROM users WHERE id = ?", session["user_id"])[0]["isteacher"]
        
        return render_template("settings.html", isteacher=isteacher)