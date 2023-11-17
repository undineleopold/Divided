from random import randint
import json

success=['Sehr schön!','Weiter so!', 'Komplett richtig!', 'Super!', 'Gut gemacht!', 'Es geht voran!', 'Na, auf den Geschmack gekommen?', 'Toll! Bereit für die nächste Herausforderung?', 'Schon wieder fertig? Viel Spaß bei der nächsten Frage!','Tada! Ob du die nächste Aufgabe auch schaffst?']

error=['Leider nicht richtig!', 'Da hat sich ein Fehler eingeschlichen.', 'Lieber nochmal nachrechnen.']

class Question:
    def __init__(self,skill=1):
        if skill==1:
            quotient=randint(11,19)
        elif skill==2:
            quotient=randint(11,29)
        elif skill==3:
            quotient=randint(11,49)
        else:
            quotient=randint(11,99)
        self.divisor=randint(2,9)
        remainder=randint(0,self.divisor-1)
        self.dividend=quotient*self.divisor+remainder
        self.answer=(quotient,remainder)
        self.hint=[]
            

def generate_division_question(skill=1):
    q=Question(skill)
    return {"dividend":q.dividend, "divisor":q.divisor, "answer":q.answer}

def generate_division_correction():
    pass
    #return correction

def success_message():
    return success[randint(0,len(success)-1)]
    #return message


def error_message():
    return error[randint(0,len(error)-1)]
    #return message

def level_up_message():
    pass
    #return message

def strtoint(user_input:str):
    if user_input=='':
        return 0
    else:
        return int(user_input)
