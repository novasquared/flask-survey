from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get("/")
def show_survey_details():
    """Shows survey title and instructions and includes a button to start survey"""
    # dont need these since survey already passes use survey = survey in render and change html
    # survey_title = survey.title
    # survey_instructions = survey.instructions
    return render_template(
        "survey_start.html",
        survey_title=survey_title, 
        survey_instructions = survey_instructions)

@app.post("/begin")
def start_survey():
    """Redirects user to the first question"""
    session["responses"] = []
    return redirect("/questions/0")

@app.get("/questions/<int:question_number_counter>")
def show_question(question_number_counter):
    """Shows question and choices"""
    responses = session["responses"]
    if question_number_counter != len(responses):
        flash("You are trying to access an invalid question.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[question_number_counter].question
    choices = survey.questions[question_number_counter].choices
    # same ideas as show_survey details
    return render_template(
        "question.html",
        question = question,
        choices = choices
    )

@app.post("/answer")
def handle_response():
    """Posts the response, redirects to next question or to 'thank you' message if survey is finished"""
    # Get the response
    #breakpoint()
    response = request.form["answer"]

    # Append response of question to responses list
    responses = session["responses"]
    responses.append(response)
    session["responses"] = responses

    # Check if this is the last question. If not, increment counter and redirect to next question
    if len(responses) < len(survey.questions):
        question_number_counter = len(responses)
        return redirect(f"/questions/{question_number_counter}") #need to replace counter with something dynamic
    #If yes, redirect to 'thank you' page
    else:
        return redirect("/thank-you")

@app.get("/thank-you")
def show_thank_you_message():
    """Shows 'thank you' message"""
    return render_template(
        "completion.html"
    )

