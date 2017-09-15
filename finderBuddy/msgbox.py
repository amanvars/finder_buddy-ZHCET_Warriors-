import mp3play
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging
from Tkinter import *
import pyttsx
import speech_recognition as sr
from time import ctime
import time
import pyaudio
import os
from gtts import gTTS


global threshold
engine=''


def record_audio():
    r=sr.Recognizer()
    #engine=pyttsx.init()
    #global data
    with sr.Microphone() as source:
        #engine.say("Yes-please say something")
        #engine.runAndWait()
        #r.dynamic_energy_threshold=False
        r.adjust_for_ambient_noise(source)
        try:
            audio=r.listen(source,timeout=5, phrase_time_limit=None)
        except sr.WaitTimeoutError:
            print "Timeout"    
    
    data=''
    try:
        data=r.recognize_google(audio)
        for k in data:
            if (k in ['zero','one','two','three','four','five','six','seven','eight','nine']):
                if(k=='zero'):
                    k=str(0)
                elif (k=='one'):
                    k=str(1)
                elif (k=='two'):
                    k=str(2)
                elif (k=='three'):
                    k=str(3)
                elif (k=='four'):
                    k=str(4)
                elif (k=='five'):
                    k=str(5)
                elif (k=='six'):
                    k=str(6)
                elif (k=='seven'):
                    k=str(7)
                elif (k=='eight'):
                    k=str(8)
                elif (k=='nine'):
                    k=str(9)
                                                        
        print data
    except sr.UnknownValueError:
        data="NIL"
        print("Google Speech Recognition could not understand audio")
        #engine.say("Sorry-I couldn't understand what you just said.You can try repeating your order or just type it in")
    except sr.RequestError as e:
        data="NIL"
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        #engine.say("Sorry-I couldn't understand what you just said.You can try repeating your order or just type it in")
    if not(data=="NIL"):
        data=data.lower()
 
    return data



def bot_init():
    # Uncomment the following line to enable verbose logging
    #logging.basicConfig(level=logging.INFO)
    global engine
    engine=pyttsx.init()
   
    #str=record_audio()   
    bot = ChatBot("finder_Buddy",
        storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
         logic_adapters=[
            "chatterbot.logic.InventoryAdapter",
            "chatterbot.logic.BestMatch",
            "chatterbot.logic.FindDealAdapter",
            "chatterbot.logic.LanguageAdapter",
            "chatterbot.logic.ChoiceAdapter"
        ],
         filters=[
             'chatterbot.filters.RepetitiveResponseFilter'
         ],
        output_adapter="chatterbot.output.TerminalAdapter",
        database="database"
    )

    root.update()
    return bot

def bot_rep(bot,str):
    # Create a new instance of a ChatBot

    bot.set_trainer(ChatterBotCorpusTrainer)

    bot.train(
        "chatterbot.corpus.english"
    )
    root.update()
    #str=record_audio()
    bot_input = bot.get_response(str)
        #print bot_input
    print_bot(bot_input)
    engine.say(bot_input)
    engine.runAndWait()
    #return bot_input

def input_man():
    # it take input as string from entry box.
    str = entry.get()
    root.update()
    return str


def setText(*args):
 # it set text in user interface
    f = mp3play.load('bot.mp3')
    f.play()
    str=input_man()
    #str=""

    """ChatLog.config(state=NORMAL)
    ChatLog.insert(END,"\nYou: "+str)
    ChatLog.see("end")
    ChatLog.config(state=DISABLED)"""

    boti = bot_init()
    #str=record_audio()
    ChatLog.config(state=NORMAL)
    ChatLog.insert(END,"\nYou: "+str)
    ChatLog.see("end")
    ChatLog.config(state=DISABLED)
    #boti=bot_init()

    #str=""
    bot_rep(boti,str)
    #return str

def toSpeak():
 # it set text in user interface
    
    str=""

    """ChatLog.config(state=NORMAL)
    ChatLog.insert(END,"\nYou: "+str)
    ChatLog.see("end")
    ChatLog.config(state=DISABLED)"""

    boti = bot_init()
    str=record_audio()
    ChatLog.config(state=NORMAL)
    ChatLog.insert(END,"\nYou: "+str)
    ChatLog.see("end")
    ChatLog.config(state=DISABLED)
    #boti=bot_init()

    #str=""
    bot_rep(boti,str)
    #return str
def print_bot(str_bot):
# to print bot answer in user interface
    f = mp3play.load('bot.mp3')
    f.play()

    ChatLog.config(state=NORMAL)
    ChatLog.insert(END,"\nBot: "+str_bot)
    #ChatLog.delete(0,END)
    ChatLog.see("end")
    entry.delete(0,END)
    ChatLog.config(state=DISABLED)




root = Tk()

root.iconbitmap('icon.ico')
root.title("finderBuddy")

w = 820 # width for the Tk root
h = 650 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
#root.geometry("1080x625+400+60")

root.resizable(width=FALSE,height=FALSE)
topFrame = Frame(root)
topFrame.pack()
botFrame = Frame(root)
botFrame.pack(side=TOP)

img = PhotoImage(file = "infofb.gif")
label  = Label(topFrame,image=img)
label.pack()



ChatLog = Text(botFrame, bg="#80CBC4", height="22", width="80",fg="#37474F")

#Bind a scrollbar to the Chat window
scrollbar = Scrollbar(botFrame, command=ChatLog.yview, cursor="circle")
scrollbar.grid(row=0, column=3, sticky='nsew')
ChatLog['yscrollcommand'] = scrollbar.set
#ChatLog.pack()

ChatLog.config(state=NORMAL)
#ChatLog.insert(END,chat)


#ChatLog.see("end")
 

ChatLog.insert(END,"\nBot: Hola,My name is FinderBuddy and I'm a procurement bot\nI'm here to help you to easily acquire all items that you need in your job\nYou can know more about how to use me by typing #help or simply help or by a simple how-to query\nOne more tip---use of lower case is recommended while chatting with me.")
ChatLog.config(font=("Verdana",11),wrap=WORD)
ChatLog.config(state=DISABLED)

send = Label(botFrame,text="Enter your Message:",font="Verdana",fg="#5D4037")
entry = Entry(botFrame,bd=3,width=111)


send_btn = Button(botFrame,width=12,text="Send!",fg="black",bg="#BDBDBD",command=setText)
speak_btn = Button(botFrame,width=12,text="Speak!",fg="black",bg="#BDBDBD",command=toSpeak)

entry.bind("<Return>", setText)


ChatLog.grid(row=0,rowspan = 1,columnspan = 4,sticky = N)
send.grid(row=1,columnspan=5,sticky=W)
entry.grid(row=3,column=0,columnspan=1,sticky = W+S)
send_btn.grid(row=3,column=1,columnspan=3,sticky = E+S)
speak_btn.grid(row=5,column=1,columnspan=3,sticky = E+S)

engine=pyttsx.init()
engine.say("Hi I am FinderBuddy-your very own procurement bot.Feel free to either type or say aloud what you need")
engine.runAndWait()

threshold=100


root.mainloop()
