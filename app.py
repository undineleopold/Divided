import os
import re
import json
from flask import Flask,render_template,request,url_for,redirect,flash
from questions import *
from markupsafe import escape

#create a new Flask application
app = Flask(__name__)


#landing page (static)
@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':#form has been submitted
        action=request.form['action']
        return redirect(url_for('calculate',action=action))
    else:
        return render_template('home.html')      

#Info page (static)
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

#Calculations (form submission)
@app.route('/calculate/<action>', methods=['POST','GET'])
def calculate(action):
    enable_btn=''
    message=''
    score=0
    clear=True
    skill=1
    if request.method=='POST': #form has been submitted
        new=request.form.get('new')
        ans=request.form.get('ans')
        hlp=request.form.get('help')
        score=int(request.form.get('score'))
        skill_new=min(4,1+score//50)
        if skill_new>skill:
            #flash("Ab jetzt wird es schwieriger. Du schaffst das!")
            skill=skill_new
        if new: #new is not None
            question=generate_division_question(skill)
        else:
            #use cookie rather than hidden input?
            question=eval(request.form.get('question'))#need to use eval bc jinja2 returns
            #repr of the python object
            #check the partial and complete answers given
            whole, coarse, partial_coarse, fine, partial_fine = 0, 0, 0, 0, 0
            clear=False
            length=len(str(question['dividend']))
            def get_input(var,name,length):
                for i in range(length):
                    var*=10
                    var+=strtoint(request.form.get(name+'_'+str(i)))
                return var
                
            whole=get_input(whole,'whole',length)
            rem=strtoint(request.form.get('rem'))
            coarse=get_input(coarse,'coarse',length)
            partial_coarse=get_input(partial_coarse,'partial_coarse',length)
            fine=get_input(fine,'fine',length)
            partial_fine=get_input(partial_fine,'partial_fine',length)
            fine_rem=strtoint(request.form.get('fine_rem'))

            if hlp: #help/hint requested
                message="Finde eine möglichst große Zahl kleiner gleich "+str(question['dividend'])\
                         +" die leicht durch "+str(question['divisor'])+" zu teilen geht (das Grobe). \
                         Dann kümmere dich um das Verbleibende (das Feine). Zum Schluss rechne die \
                         Quotienten zusammen und übertrage den Rest in die erste Zeile."
            elif ans: #answer submitted
                if whole==question['answer'][0] and rem==question['answer'][1]:#top line answer is correct
                    if coarse+fine==question['dividend'] and partial_coarse+partial_fine==whole and \
                    fine_rem==rem and partial_coarse*question['divisor']==coarse:
                        message=success_message()
                        score+=4
                        enable_btn='disabled'
                    elif (coarse,fine,partial_coarse,partial_fine,fine_rem)==(0,0,0,0,0): #empty detailed calculation
                        message=success_message()
                        message+=" Beim nächsten Mal zeige den Rechenweg für mehr Punkte."
                        score+=2
                        enable_btn='disabled'
                    else: #detailed calculation is wrong instead of empty
                        message="Wie kommst du mit deinem Rechenweg zum Endergebnis? Berichtige mal."
                else:
                    message=error_message()
    else:
        question=generate_division_question()
    return render_template('calculate.html',question=question, message=message, enable_btn=enable_btn, score=score, clear=clear)

app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True) #tell development server to listen on all interfaces
