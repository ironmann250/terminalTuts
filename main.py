#-*-coding:utf8;-*-
#login or register
#-l stats or quiz
#-q disp name, cur score, cur quiz, quiz
# keypoints
#-----------
#- main program with alternating functions
#- efficient looping and memory retention by recursively calling a function
#- security using exec
#- catching system standard input and output
#- a minimal modern command line text editor
#- making it cross platform with appropriate linux and windows commands
#- a continuous loop made with functions
#- match answers with regular expression patterns

import shelve, sys, re, os, sys, contextlib, editor
from book import questions
from io import StringIO

#global vars
db=shelve.open('database.db',flag='c',writeback=True)
cur_user=None

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield (stdout)
    sys.stdout = old

def executor(code):
    with stdoutIO() as s:
        exec (code)
    return s.getvalue()

def textEditor(init=''):
    return editor.editor(box=True,inittext=init, win_location=(0, 0))

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
    
def register() :
    global db
    cls()
    print ('#'*5,'  TERMINAL TUTS | REGISTER','#'*5)
    username=input('username >')
    if username not in db.keys():
        db[username]=[0,0]#score,cur quiz
        db.sync()
        login()
    else:
        print ('account already registered') 
        login() 


def login():
    global db
    global cur_user
    cls()
    print ('#'*5,'  TERMINAL TUTS | LOGIN ','#'*5)
    username=input('username >')
    if username not in db.keys():
        print ('register account first')
        register()
    else:
        cur_user=username
        funcs()

def is_logged():
    global cur_user
    if cur_user:
        return 1
    else:
        login()
        
def stats():
    global db
    global cur_user
    is_logged()
    cls()
    print ('#'*5,'  TERMINAL TUTS | STATISTICS ','#'*5)
    print ('- user    :',cur_user)
    print ('- score   :',db[cur_user][0])
    print ('- on quiz :',db[cur_user][1]+1)
    input('press enter to continue...')
    funcs()

def quiz(id,initt=''):
    global db
    global cur_user
    try:
        question=questions[id]
    except:
        question=None #proc to show end of tuts
    if question:
        cls()
        tmp=db[cur_user]
        db[cur_user]=[tmp[0],id]
        db.sync()
        print ('#'*5,'  TERMINAL TUTS | CHALLENGE ','#'*5,'\n')
        print ('CHALLENGE',id+1,':',question[0],'\n')
        print ('INSTRUCTIONS: Ctrl+X to save and execute')
        input('press enter to solve it...')
        try:
            code=textEditor(init=initt)
            answer=executor(code)
        except Exception as e:
            print ('#'*5,'  TERMINAL TUTS | ERROR ','#'*5)
            print (e)
            input('press enter to continue...')
            quiz(id,code)
        if len(re.findall(question[1],answer))>0:
            print ('result: ',answer)
            input('press enter for the next one...')
            tmp=db[cur_user]
            db[cur_user]=[tmp[0]+10,tmp[1]]
            db.sync()
            quiz(id+1)
        else:
            cls()
            print ('#'*5,'  TERMINAL TUTS ','#'*5)
            print ('result: ',answer)
            input ('please retry again ...')
            quiz(id)
    else:
        print ('#'*5,'  TERMINAL TUTS | FAREWELL ','#'*5)
        print ('thank you for your time come back next time')

def start():
    cls()
    print ('#'*5,'  TERMINAL TUTS | HOME','#'*5)
    choice1=input('Select:\n1. Login \n2. Register\n3. Quit\n choice> ')
    if choice1=='1':
        cls()
        login()
    elif choice1=='2':
        cls()
        register()

    

def funcs():
    global db
    global cur_user
    cls()
    print ('#'*5,'  TERMINAL TUTS | MAIN ','#'*5)
    choice1=input('Select:\n1. stats \n2. quiz\n3. Quit\n choice> ')
    if choice1=='1':
        cls()
        stats()
    elif choice1=='2':
        cls()
        quiz(db[cur_user][1])
        
start() 
