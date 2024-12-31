from flask import Flask, request, render_template, redirect, url_for
import google.generativeai as genai
from datetime import datetime

app = Flask(__name__)

# Initialize GenAI with API key
genai.configure(api_key="YOUR-API-KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Collect form data
    salary = request.form['salary']
    salary_date = request.form['salary_date']
    groceries = request.form['groceries']
    streaming = request.form['streaming']
    shopping = request.form['shopping']
    electricity_bill = request.form['electricity_bill']
    water_bill = request.form['water_bill']
    school_fee = request.form['school_fee']
    currency = request.form['currency']
    todaydate = datetime.today().strftime('%Y-%m-%d')
    general_date_of_event = request.form['general_date_event'] 
    event = request.form['event'] 
    eventestimatedamount=request.form['eventestimatedamount'] 

    # Collect dynamic custom questions and answers
    custom_questions = request.form.getlist('custom_question[]')
    custom_answers = request.form.getlist('custom_answer[]')

    # Build the custom questions and answers section for the advice
    custom_advice = ""
    for question, answer in zip(custom_questions, custom_answers):
        custom_advice += f"{question} {answer}\n"
    
    # Create the advice message with the dynamic content
    prompt = f"You are a financial advisor of a person whose salary is {salary},the currency {currency}, they get their salary on {salary_date}, today date is {todaydate}. The person's expenses are groceries: {groceries}, streaming services: {streaming}, personal shopping: {shopping}, electricity bill: {electricity_bill}, water bill: {water_bill}, school fees: {school_fee}. Here are some of their additional expenses:\n{custom_advice}\nThey are planning these events around the date {general_date_of_event} the is {event} and the estimated amout for the even is {eventestimatedamount}.If there it no event tell them how they can save money for investment. Tell them if they need to cut their expenses to attend the events,if they need to then tell them how they can cut their expences with alternatives like using YouTube instead of spending money on streaming. Calculate how much they will save and how to save it.Don't try to manage their expences if they are able to afford their trip.write your plan clearly in a paragraph keep it brief around 350 words."
    rawresponse = model.generate_content(prompt)

    response = rawresponse.text
    advice = response

    # Pass advice to a new page or render it on the same page
    return render_template('final_advice.html', advice=advice)

@app.route('/planning', methods=['POST'])
def planning():
    # Additional questions for event planning
    planning_question = request.form['planning_question']
    # Generate response for event planning question
    planning_response = "Your event planning advice here."
    return render_template('planning.html', planning_response=planning_response)

if __name__ == '__main__':
    app.run(debug=True)
