'''
REFERNECES:
BACKGROUND :https://www.vectorstock.com/royalty-free-vector/abstract-geometric-shapes-on-a-purple-background-vector-22911171

NETWOKRING BASICS LEARNED FROM :
https://www.youtube.com/watch?v=3QiPPX-KeSc&t=2407s


DATABASES +TKINTER BASICS LEARNED FROM :
https://www.youtube.com/watch?v=YXPyB4XeYLA&t=12851s


'''
# OneDrive\سطح المكتب\Term Project\TP3\Project Codebase


from tkinter import *
from PIL import ImageTk,Image
import sqlite3
import os
import string
import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog


# MAIN CLASS THAT RUNS THE PROGRAM
# THE FUNCTIONS IN THIS CLASS ARE EITHER FRAME FUNCTIONS
# OR HELPER F(X) S TO HANDLE THE PROGRAM
class kviz:
    
    # CONSTRUCTOR FOR ROOT AND NEEDED VARIABLES
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x742")
        self.score = 0
        self.questionPlayed = -1 # because quiz played f(x) will skip 0th qs
        self.messg = ''
        self.correctAns = 0
        self.quizNameChecked = False
        self.answer1Color = 'white'
        self.answer2Color = 'white'
        self.answer3Color = 'white'
        self.answer4Color = 'white'
        self.gui_done = False
        self.running = False
        self.quizPlayed = 0
        self.qNames = list()
        self.answer_chsn =False
        self.otherQuizName = ''
        
        self.login()
        
        
    #MAIN LOGIN FUNCTION
    def login(self):
         # Code to delete previous frame
        for i in self.root.winfo_children():
            i.destroy()
            
        self.frame1 = Frame(self.root,bg='#C8BFE7',relief=SUNKEN)
        self.frame1.pack(fill='x')
        
        # Uploading Image
        self.frame1.picture = PhotoImage(file="bg01.png")
        self.frame1.label = Label(self.frame1, image=self.frame1.picture,width=0)
        self.frame1.label.pack(fill='x')

        self.u_name = Entry(self.frame1, width=30)
        self.u_name.place(x=1000//2 - 150,y=742//2)

        self.u_passw = Entry(self.frame1, width=30,show='*')
        self.u_passw.place(x=1000//2 - 150,y=800//2)


        #Creating Usernames and passwords widgets
        u_name_label = Label(self.frame1, text='Username',bg='#7300bf')
        u_name_label.place(x=1000//2 - 250 ,y=742//2)
        
        u_passw_label = Label(self.frame1,text='Password',bg='#7300bf')
        u_passw_label.place(x=1000//2 - 250,y=800//2)

        #Create a sumbit button'
        reg_btn = Button(self.frame1,text='Register',width=50, command= self.sumbit)
        reg_btn.place(x=1000//4,y=800*2//3 )


        login_btn = Button(self.frame1, text='Login',width=50 , command=self.authenticate)
        login_btn.place(x=1000//4 ,y=800*2//3 - 50)
        
    #FUNCTION RESPOSIBLE TO AUHTENTICATE USER
    def authenticate(self):
        
        autheticated = False
        #Creating a datatbase / connect to one'
        conn = sqlite3.connect('users.db')
        
        #create a crusor'
        c = conn.cursor()
        
        c.execute("SELECT *,oid FROM user")
        records = c.fetchall()
        for details in records:
            if self.u_name.get() in details and self.u_passw.get() in details :
                autheticated = True
                
        
        if autheticated == True:
            self.nickname = self.u_name.get()
            self.profile()
        else:
            msg = Label(self.frame1,text='''Username/Password does not exsist!
You Should Register First''',bg='red')
            
            msg.place(x=1000//2 - 150,y=800//2 +30)
        
            
            
            
    # FUNCTION TO MANAGE USER PROFILE     
    def profile(self):
        
        for i in self.root.winfo_children():
            i.destroy()
            
            
        self.frame2 = Frame(self.root,bg='#C8BFE7',relief=SUNKEN)
        self.frame2.pack(fill='x')

        self.frame2.picture = PhotoImage(file="bg01.png")
        self.frame2.label = Label(self.frame2, image=self.frame2.picture,width=0)
        self.frame2.label.pack(fill='x')

        #Button to create a quiz
        create_btn = Button(self.frame2,text='Create Quiz',fg="purple",width=50,command=self.createQuiz)
        create_btn.place(x=1000//2 - 200,y=800//2)
    
        #DISABLED AS USER HAS NOT CREATED A QUIZ
        play_btn = Button(self.frame2,text='Play a Quiz',fg="purple",width=50,state='disabled')
        play_btn.place(x=1000//2 - 200,y=800//2 + 50)
        
        chroom_btn = Button(self.frame2,text='Chat Venue',fg="purple",width=50,command=self.startChat)
        chroom_btn.place(x=1000//2 - 200,y=800//2 + 100)
        
        accessallQuizzes_btn = Button(self.frame2,text='Play Other Quizzes',fg="purple",width=50,command= self.viewAllQuizzes)
        accessallQuizzes_btn.place(x=1000//2 - 200,y=800//2 + 150)
        
#     FUNCTION TO START THE CHAT
    def startChat(self):
            
            HOST = '127.0.0.1'
            PORT = 9090
            client = self.client(HOST,PORT)
#        FUNCTION THAT HANDLES CONNECTING TO SERVER     
    def client(self,host,port):
            
            for i in self.root.winfo_children():
                i.destroy()
                
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.connect((host,port))
            
            
            self.gui_done = False
            
            self.running = True
                        
            gui_thread = threading.Thread(target=self.gui_loop)
            receive_thread = threading.Thread(target=self.receive)
            
            gui_thread.start()
            receive_thread.start()

#         FUNCTION THAT BUILDS CHAT GUI
    def gui_loop(self):
        
        self.frame7 = Frame(self.root,bg='#C8BFE7',relief=SUNKEN)
        self.frame7.pack(fill='x')
        self.frame7.picture = PhotoImage(file="bg03.png")
        self.frame7.label = Label(self.frame7, image=self.frame7.picture,width=0)
        self.frame7.label.pack(fill='x')
                    
        self.text_area = tkinter.scrolledtext.ScrolledText(self.frame7,height=5)
        self.text_area.place(x=100,y=400)
        self.text_area.config(state='disabled')
        
        self.input_label = tkinter.Label(self.frame7, text='Type your Message Here')
        self.input_label.place(x=100,y=520)
        
        self.input_area = tkinter.Text(self.frame7, height=2,bg='#7300BF',fg='white' )
        self.input_area.place(x=100,y=550)
        
        self.send_button = tkinter.Button(self.frame7,text='Send',command=self.write)
        self.send_button.place(x=800,y=600)
        
        
        go_back_btn =Button(self.frame7,text='  Go Back to Profile  ',bg='white',command =  self.profile)
        go_back_btn.place(x=766,y=700)
        
        self.sock.send(f'{self.nickname}'.encode('utf-8'))
        self.gui_done = True
        
# FUNCTION THAT SENDS TO THE SERVER THE USER'S MESSG
    def write(self):
             
        message =f"{self.nickname}:{self.input_area.get('1.0','end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0','end')
        
# FUNCTION THAT RECIEVES WHAT THE SERVER SENDS / MSSG FROM OTHER CLIENTS
    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                if message =='NICK':
                    self.sock.send('[A USER JOINED THE CHAT]'.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end',message)
                        self.text_area.yview('end')
                        self.text_area.config(state = 'disabled')
                        
            except ConnectionAbortedError:
                break
            except:
                print('ERROR!')
                message =f"{self.nickname} Left the Chat..."
                self.sock.send(message.encode('utf-8'))
                self.sock.close()
                break
            
    
    # FUNCTION TO SUMBIT USER INFO TO REGISTER
    def sumbit(self):
        
        
        #Creating a datatbase / connect to one'
        conn = sqlite3.connect('users.db')
        
        #create a crusor'
        c = conn.cursor()
 
        c.execute("INSERT INTO user VALUES (:u_name, :u_passw)",
        
            {
                'u_name': self.u_name.get(),
                'u_passw': self.u_passw.get()
                
                }
                  )
        #Clear the text boxes'
        self.u_name.delete(0,END)
        self.u_passw.delete(0,END)
        
        conn.commit()
        conn.close()
        self.login()
        
        
# FUNCTION TO CHECK IF QUIZ NAME IS LEGAL
    def checkQuizName(self):
        if self.quizNameChecked == False:
#             print('[CHECKING QUIZ NAME....]')
            
            conn = sqlite3.connect('quizNames.db')
            c = conn.cursor()
            quizName = self.quizName.get().replace(' ','_')
            c = conn.cursor()        
            c.execute(f"SELECT *,oid FROM quizName ")
            records = c.fetchall()
            qNames = list()

            for name in records:
                qNames.append(list(name)[0])
                
#             print('quizName',quizName)
#             print('qNames',qNames)
#             print(quizName not in qNames)
            if quizName not in qNames:
                c.execute(f'INSERT INTO quizName VALUES (:name)',
                        {
                            'name':str(quizName),
                            
                            })        
                conn.commit()
                conn.close()
                self.quizNameChecked = True
                
                self.saveQuestion()
                
                
            else:

                self.messg = 'Sorry! This Quiz Name is already used'
                self.createQuiz()
            
            
    
            
    #F(X) TO CREATE QUIZ
    def createQuiz(self):
            # DESTORY PREVIOUS FRAME       
            for i in self.root.winfo_children():
                i.destroy()
            #CREATING NEW FRAME FOR TRANSITINING
            self.frame3 = Frame(self.root,bg='#C8BFE7',relief=SUNKEN)
            self.frame3.pack(fill='x')

            self.frame3.picture = PhotoImage(file="qmbg.png")
            self.frame3.label = Label(self.frame3, image=self.frame3.picture,width=0)
            self.frame3.label.pack(fill='x')
            
            if self.quizNameChecked == True:
                self.messg =''
            
            #Code for labels and their Enteries
            self.quizName= Entry(self.frame3,width=30)
            self.quizName.place(x=176,y=293)
            quizName_label = Label(self.frame3, text='QuizName:',bg='#7300bf')
            quizName_label.place(x=89,y=293)
            
            #QUESTION LABEL AND ENTRY BOX'
            self.question= Entry(self.frame3, width=30)
            self.question.place(x=176,y=353)
            question_label = Label(self.frame3, text='Question:',bg='#7300bf')
            question_label.place(x=89,y=353)
            
            #ANSWER 1 LABEL AND ENTRY BOX'
            self.answer1= Entry(self.frame3, width=30)
            self.answer1.place(x=176,y=393)
            answer1_label = Label(self.frame3, text='Answer1 :',bg='#7300bf')
            answer1_label.place(x=89,y=393)


            #ANSWER 2 LABEL AND ENTRY BOX'
            self.answer2= Entry(self.frame3, width=30)
            self.answer2.place(x=176,y=433)
            answer2_label =Label(self.frame3, text='Answer2 :',bg='#7300bf')
            answer2_label.place(x=89,y=433)


            #ANSWER 3 LABEL AND ENTRY BOX'
            self.answer3= Entry(self.frame3, width=30)
            self.answer3.place(x=176,y=473)
            answer3_label = Label(self.frame3, text='Answer3 :',bg='#7300bf')
            answer3_label.place(x=89,y=473)


            #ANSWER 4 LABEL AND ENTRY BOX'
            self.answer4 = Entry(self.frame3, width=30)
            self.answer4.place(x=176,y=513)
            answer4_label = Label(self.frame3, text='Answer4 :',bg='#7300bf')
            answer4_label.place(x=89,y=513)

              
            #COMMAND TO SAVE QUESTION'
            save_btn = Button(self.frame3,text='Save',command=self.saveQuestion,width=10)
            save_btn.place(x=206,y=593)
            
            #COMMAND TO UNSAVE QUESTION'
            unsave_btn = Button(self.frame3,text='Unsave',command=self.unsaveQuestion,width=10)
            unsave_btn.place(x=306,y=593)
            
            #COMMAND TO SAVE QUIZ'
            saveQuiz_btn = Button(self.frame3,text='Play Quiz',command=self.quizReady,width=10)
            saveQuiz_btn.place(x=206,y=653)
            
            #COMMAND TO UNSAVE QUIZ'
            discardQuiz_btn = Button(self.frame3,text='Discard Quiz',command=self.unsaveQuizz)
            discardQuiz_btn.place(x=306,y=653)
        
            #BUTTONS TO CHOOSE RIGHT ANSWER
            
            btn_1 = Button(self.frame3,text='Answer 1',bg='white',command = self.rightAns1)
            btn_1 .place(x=616,y=353,width=100)
            
            btn_2 = Button(self.frame3,text='Answer 2',bg='white',command = self.rightAns2)
            btn_2 .place(x=766,y=353,width=100)
            
            btn_3 = Button(self.frame3,text='Answer 3',bg='white',command = self.rightAns3)
            btn_3 .place(x=616,y=420,width=100)
            
            btn_4 = Button(self.frame3,text='Answer 4',bg='white',command = self.rightAns4)
            btn_4 .place(x=766,y=420,width=100)
            
            messg =Label(self.frame3,text=self.messg,fg='white',bg='red')
            if self.messg != '':
                messg.place(x=89,y=243)
            go_back_btn =Button(self.frame3,text='  Go Back to Profile  ',bg='white',command =  self.profile)
            go_back_btn.place(x=766,y=620)
            
            
            
            
    # FUNCTIONs TO SET RIGHT ANSWER1        
    def rightAns1(self):
        self.correctAns = 1
        btn_1 = Button(self.frame3,text='Answer 1',bg='green')
        btn_1 .place(x=616,y=353,width=100)
        btn_2 = Button(self.frame3,text='Answer 2',bg='white',command = self.rightAns2)
        btn_2 .place(x=766,y=353,width=100)
        btn_3 = Button(self.frame3,text='Answer 3',bg='white',command = self.rightAns3)
        btn_3 .place(x=616,y=420,width=100)    
        btn_4 = Button(self.frame3,text='Answer 4',bg='white',command = self.rightAns4)
        btn_4 .place(x=766,y=420,width=100)
            
        

    # FUNCTIONs TO SET RIGHT ANSWER2  
    def rightAns2(self):
        self.correctAns = 2
        btn_2 = Button(self.frame3,text='Answer 2',bg='green')
        btn_2 .place(x=766,y=353,width=100)
        btn_1 = Button(self.frame3,text='Answer 1',bg='white',command = self.rightAns1)
        btn_1 .place(x=616,y=353,width=100)
        btn_3 = Button(self.frame3,text='Answer 3',bg='white',command = self.rightAns3)
        btn_3 .place(x=616,y=420,width=100)
        btn_4 = Button(self.frame3,text='Answer 4',bg='white',command = self.rightAns4)
        btn_4 .place(x=766,y=420,width=100)
        
            
           
     # FUNCTIONs TO SET RIGHT ANSWER3   
    def rightAns3(self):
        self.correctAns = 3
        btn_3 = Button(self.frame3,text='Answer 3',bg='green')
        btn_3 .place(x=616,y=420,width=100)
        btn_1 = Button(self.frame3,text='Answer 1',bg='white',command = self.rightAns1)
        btn_1 .place(x=616,y=353,width=100)    
        btn_2 = Button(self.frame3,text='Answer 2',bg='white',command = self.rightAns2)
        btn_2 .place(x=766,y=353,width=100)    
        btn_4 = Button(self.frame3,text='Answer 4',bg='white',command = self.rightAns4)
        btn_4 .place(x=766,y=420,width=100)
            
            
    # FUNCTIONs TO SET RIGHT ANSWER4 
    def rightAns4(self):
        self.correctAns = 4
        btn_1 = Button(self.frame3,text='Answer 1',bg='white',command = self.rightAns1)
        btn_1 .place(x=616,y=353,width=100)
        btn_2 = Button(self.frame3,text='Answer 2',bg='white',command = self.rightAns2)
        btn_2 .place(x=766,y=353,width=100)    
        btn_3 = Button(self.frame3,text='Answer 3',bg='white',command = self.rightAns3)
        btn_3 .place(x=616,y=420,width=100)  
        btn_4 = Button(self.frame3,text='Answer 4',bg='green',command = self.rightAns4)
        btn_4 .place(x=766,y=420,width=100)
        
        
    #F(X) TO SAVE QUESTION
    def saveQuestion(self):
        if self.quizNameChecked == False:
            self.checkQuizName()
        else:
            quizName = self.quizName.get().replace(' ','_')
            try:
                conn = sqlite3.connect(f'{quizName}.db')
                #2.create a crusor'
                c = conn.cursor()

                c.execute(f"""CREATE TABLE {quizName}(
                    question text,
                    answer1 text,
                    answer2 text,
                    answer3 text,
                    answer4 text,
                    correct integer
                    )""")
                conn.commit()
                conn.close()
            
            except:
                
                conn = sqlite3.connect(f'{quizName}.db')
                c = conn.cursor()
                c.execute(f'INSERT INTO {quizName} VALUES (:question, :answer1,:answer2,:answer3,:answer4,:correct)',
                    {
                        'question':str(self.question.get()),
                        'answer1':str(self.answer1.get()),
                        'answer2':str(self.answer2.get()),
                        'answer3':str(self.answer3.get()),
                        'answer4':str(self.answer4.get()),
                        'correct':self.correctAns,
                        
                        })
                #print(self.correctAns)
                self.question.delete(0,END)
                self.answer1.delete(0,END)
                self.answer2.delete(0,END)
                self.answer3.delete(0,END)
                self.answer4.delete(0,END)
                self.correctAns = 0                 
                conn.commit()
                conn.close()
            self.messg =''
            btn_1 = Button(self.frame3,text='Answer 1',bg='white',command = self.rightAns1)
            btn_1 .place(x=616,y=353,width=100)
            
            btn_2 = Button(self.frame3,text='Answer 2',bg='white',command = self.rightAns2)
            btn_2 .place(x=766,y=353,width=100)
            
            btn_3 = Button(self.frame3,text='Answer 3',bg='white',command = self.rightAns3)
            btn_3 .place(x=616,y=420,width=100)
            
            btn_4 = Button(self.frame3,text='Answer 4',bg='white',command = self.rightAns4)
            btn_4 .place(x=766,y=420,width=100)
            
            
    #F(X) TO UNSAVE QUESTION'
    def unsaveQuestion(self):
        
        #Clear the text boxes
        self.question.delete(0,END)
        self.answer1.delete(0,END)
        self.answer2.delete(0,END)
        self.answer3.delete(0,END)
        self.answer4.delete(0,END)
        btn_1 = Button(self.frame3,text='Answer 1',bg='white',command = self.rightAns1)
        btn_1 .place(x=616,y=353,width=100)
        btn_2 = Button(self.frame3,text='Answer 2',bg='white',command = self.rightAns2)
        btn_2 .place(x=766,y=353,width=100)
        btn_3 = Button(self.frame3,text='Answer 3',bg='white',command = self.rightAns3)
        btn_3 .place(x=616,y=420,width=100)
        btn_4 = Button(self.frame3,text='Answer 4',bg='white',command = self.rightAns4)
        btn_4 .place(x=766,y=420,width=100)
        self.correctAns = 0
        
        
    #F(X) TO UNSAVE QUIZ'
    def unsaveQuizz(self):
        quizName = self.quizName.get().replace(' ','_')
        conn = sqlite3.connect(f'{quizName}.db')
        c = conn.cursor()
        self.quizName.delete(0,END)
        self.question.delete(0,END)
        self.answer1.delete(0,END)
        self.answer2.delete(0,END)
        self.answer3.delete(0,END)
        self.answer4.delete(0,END)
        self.correctAns = 0
        conn.close()
        
        os.remove(f'{quizName}.db')
        self.profile()
        

        
                
    #F(X) TO FINISH MAKING QUIZ
    def quizReady(self):
        try :
            quizName = self.quizName.get().replace(' ','_')
        except:
            quizName = self.otherQuizName
            
            
        conn = sqlite3.connect(f'{quizName}.db')
        c = conn.cursor()
        c.execute(f"SELECT *,oid FROM {quizName} ")
        records = c.fetchall()
        
        self.questions = []
        self.answers = []
        self.correctAnswers =[]
        
        for element in records :
            self.questions.append(element[0])
            self.answers.append(element[1:-2])
            self.correctAnswers.append(element[-2])
        
        print('Questions:',self.questions)
        print('Answers:',self.answers)
        print('Correct Answers:',self.correctAnswers)
        
        conn.commit()
        conn.close()
        self.playQuiz()
        
# F(X) TO CONTROL THE QUESTION AND ANSWERS SHOWN 
    def playQuiz(self):
        self.answer_chsn = False
        self.questionPlayed += 1
        if self.questionPlayed <= len(self.questions)-1:
            self.showQuestion(self.questions[self.questionPlayed],
                                  self.answers[self.questionPlayed],
                                  self.correctAnswers[self.questionPlayed])
        else:
            self.quizOver()
            
# F(X) TO SHOW QUESTION AND ANSWER BUTTONS 
    def showQuestion(self, ques , ans ,cAns):
        
        for i in self.root.winfo_children():
                i.destroy()                
        #CREATING NEW FRAME FOR TRANSITINING
        self.frame4 = Frame(self.root,bg='#C8BFE7',relief=SUNKEN)
        self.frame4.pack(fill='x')

        self.frame4.picture = PhotoImage(file="bg02.png")
        self.frame4.label = Label(self.frame4, image=self.frame4.picture,width=0)
        self.frame4.label.pack(fill='x')
        
        question = Label (self.frame4, text=ques,bg='#7300bf',fg='white')
        question.config(font=20)
        question.place(x=390,y=270)
        self.q = ques
        self.a = ans
        self.ca = cAns
        
        answer1_Button=Button(self.frame4, text=f'''              
              {ans[0]}              ''',bg=self.answer1Color,fg='black',command=self.answerCh1)
        answer1_Button.place(x=180,y=453)
        
        answer2_Button =Button(self.frame4, text=f'''             
              {ans[1]}               ''',bg=self.answer2Color,fg='black',command=self.answerCh2)
        answer2_Button.place(x=400,y=453)
        
        answer3_Button =Button(self.frame4, text=f'''             
              {ans[2]}               ''',bg=self.answer3Color,fg='black',command=self.answerCh3)
        answer3_Button.place(x=180,y=600)
        
        answer4_Button =Button(self.frame4, text=f'''            
              {ans[3]}               ''',bg=self.answer4Color,fg='black',command=self.answerCh4)
        answer4_Button.place(x=400,y=600)
        
        score = Label (self.frame4, text=str(self.score),bg='#7300bf',fg='white')
        score.config(font=40)
        score.place(x=830,y=450)
       
    # FUNCTION TO ACCESS RECENT QUIZZES MADE
    def viewAllQuizzes(self):
        
        conn = sqlite3.connect('quizNames.db')
        c = conn.cursor()
        c.execute(f"SELECT *,oid FROM quizName ")
        records = c.fetchall()
        self.qNames = list()

        for name in records:
            self.qNames.append(list(name)[0])
            
            
        for i in self.root.winfo_children():
                i.destroy()                
        #CREATING NEW FRAME FOR TRANSITINING
        self.frame6 = Frame(self.root,bg='#C8BFE7',relief=SUNKEN)
        self.frame6.pack(fill='x')

        self.frame6.picture = PhotoImage(file="bg04.png")
        self.frame6.label = Label(self.frame6, image=self.frame6.picture,width=0)
        self.frame6.label.pack(fill='x')
        
        recent_quizz_label = Label (self.frame6, text='The Recent Quizzes Created:',bg='#7300bf',fg='white')
        recent_quizz_label.place(x=320,y=390)
        
        q1_Button=Button(self.frame6, text=f'  {self.qNames[-1]}  ',bg=self.answer1Color,fg='black',command=self.quizChsn1)
        q1_Button.place(x=200,y=453)
        
        q2_Button =Button(self.frame6, text=f'  {self.qNames[-2]}  ',bg=self.answer2Color,fg='black',command=self.quizChsn2)
        q2_Button.place(x=430,y=453)
        
        q3_Button =Button(self.frame6, text=f' {self.qNames[-3]}  ',bg=self.answer3Color,fg='black',command=self.quizChsn3)
        q3_Button.place(x=600,y=453)
        
    # FUNCTIONs SELECT QUIZ TO PLAY
    def quizChsn1(self):
        self.otherQuizName = self.qNames[-1]
        self.quizReady()
        
    def quizChsn2(self):
        self.otherQuizName = self.qNames[-2]
        self.quizReady()
        
    def quizChsn3(self):
        self.otherQuizName = self.qNames[-3]
        self.quizReady()
        
        
 
#SERIES OF F(X)s TO SET ANS CHOOSEN 
    def answerCh1(self):
        if self.answer_chsn == False:
            self.answerChoosen = 1
            if self.answerChoosen == self.ca:
                answer1_Button =Button(self.frame4, text=f'''          
                {self.a[0]}               ''',bg='green',fg='black')
                answer1_Button.place(x=180,y=453)
            else:
                answer1_Button =Button(self.frame4, text=f'''             
                {self.a[0]}               ''',bg='red',fg='black')
                answer1_Button.place(x=180,y=453)
            self.answer_chsn = True
            self.answerCorrect()

        
    def answerCh2(self):
       if self.answer_chsn == False: 
            self.answerChoosen = 2
            if self.answerChoosen == self.ca:
                answer2_Button =Button(self.frame4, text=f'''             
                {self.a[1]}               ''',bg='green',fg='black')
                answer2_Button.place(x=400,y=453)
            else:
                answer2_Button =Button(self.frame4, text=f'''             
                {self.a[1]}               ''',bg='red',fg='black')
                answer2_Button.place(x=400,y=453)
            self.answer_chsn = True
            self.answerCorrect()
        
    def answerCh3(self):
        if self.answer_chsn == False: 
            self.answerChoosen = 3
            if self.answerChoosen == self.ca:
                answer3_Button =Button(self.frame4, text=f'''             
                {self.a[2]}               ''',bg='green',fg='black')
                answer3_Button.place(x=180,y=600)
            else:
                answer3_Button =Button(self.frame4, text=f'''             
                {self.a[2]}               ''',bg='red',fg='black')
                answer3_Button.place(x=180,y=600)
            self.answer_chsn = True
            self.answerCorrect()
        
    def answerCh4(self):
         if self.answer_chsn == False: 
            self.answerChoosen = 4
            if self.answerChoosen == self.ca:
                answer4_Button =Button(self.frame4, text=f'''             
                {self.a[3]}               ''',bg='green',fg='black')
                answer4_Button.place(x=400,y=600)
            else:
                answer4_Button =Button(self.frame4, text=f'''             
                {self.a[3]}               ''',bg='red',fg='black')
                answer4_Button.place(x=400,y=600)

            self.answer_chsn = True
            self.answerCorrect()
            
    # FUNCTIONs TO GO TO NEXT QUESTION
    def goToNextQ(self):
        next_Btn = Button(self.frame4, text=f'  Go to next Question  ',bg='#7300bf',fg='white',command=self.playQuiz)
        next_Btn.place(x=830,y=550)


# F(X) TO CHECK IF ANS IS CORRECT AND DECIDE OF QUIZ IS OVER
    def answerCorrect(self):
        
        if self.answerChoosen == self.ca:
            self.score += 10
                
        if self.questionPlayed > len(self.questions) - 1:
            self.answer_chsn = False
            self.quizOver()
        else:
            self.goToNextQ()

        
# QUIZ IS OVER FUNCTION THAT TAKES BACK TO PROFILE PG
    def quizOver(self):
        for i in self.root.winfo_children():
                i.destroy()
                
        self.frame5 = Frame(self.root,bg='#C8BFE7',relief=SUNKEN)
        self.frame5.pack(fill='x')
        
        # Uploading Image
        self.frame5.picture = PhotoImage(file="bg01.png")
        self.frame5.label = Label(self.frame5, image=self.frame5.picture,width=0)
        self.frame5.label.pack(fill='x')
        
        questions_corr = self.score//10
        
        # Handeling Message for user based on comments
        if questions_corr  < len(self.questions)//2:
            mssg = Label (self.frame5, text=f'''You Got {questions_corr}/{len(self.questions)} correct...
            Better Luck next time ''',bg='#7300bf',fg='white')
        elif questions_corr  == len(self.questions)//2:
            mssg = Label (self.frame5, text=f'''You Got {questions_corr}/{len(self.questions)} correct, 
                    that is Good! ''',bg='#7300bf',fg='white')
                    
        else:
             mssg = Label (self.frame5, text=f'''You Got {questions_corr}/{len(self.questions)} Questions correct, 
                    Awseome!! ''',bg='#7300bf',fg='white')
        mssg.place(x=390,y=270)
        

        #Button to create a quiz
        create_btn = Button(self.frame5,text='Create Quiz',fg="purple",width=50,command=self.createQuiz)
        create_btn.place(x=1000//2 - 200,y=800//2)
    
        #DISABLED AS USER HAS NOT CREATED A QUIZ
        play_btn = Button(self.frame5,text='Play a Quiz',fg="purple",width=50,state='disabled')
        play_btn.place(x=1000//2 - 200,y=800//2 + 50)
        
        chroom_btn = Button(self.frame5,text='Chat Venue',fg="purple",width=50,command=self.startChat)
        chroom_btn.place(x=1000//2 - 200,y=800//2 + 100)
        
        accessallQuizzes_btn = Button(self.frame5,text='Play Other Quizzes',fg="purple",width=50,command= self.viewAllQuizzes)
        accessallQuizzes_btn.place(x=1000//2 - 200,y=800//2 + 150)
        
        self.score = 0
        self.questionPlayed = -1 # because quiz played f(x) will skip 0th qs
        self.messg = ''
        self.correctAns = 0
        self.quizNameChecked = False
        self.answer1Color = 'white'
        self.answer2Color = 'white'
        self.answer3Color = 'white'
        self.answer4Color = 'white'
        self.gui_done = False
        self.running = False
        self.quizPlayed = 0
        self.qNames = list()
        self.answer_chsn =False
        
        self.otherQuizName = ''
        
        
        print('Quiz is over!')

        
root = Tk()
root.title('KVIZ')
kviz(root)
root.mainloop()

