import mp3play
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging
from Tkinter import *



def bot_init():
    # Uncomment the following line to enable verbose logging
    #logging.basicConfig(level=logging.INFO)
    bot = ChatBot("finder_Buddy",
        storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
         logic_adapters=[
            "chatterbot.logic.InventoryAdapter",
            "chatterbot.logic.BestMatch",
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
    bot_input = bot.get_response(str)

    print_bot(bot_input)
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

    ChatLog.config(state=NORMAL)
    ChatLog.insert(END,"\nYou: "+str)
    ChatLog.see("end")
    ChatLog.config(state=DISABLED)

    boti = bot_init()
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
h = 621 # height for the Tk root

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
ChatLog.insert(END,"\nBot: Welcome User")
ChatLog.config(font=("Verdana",11),wrap=WORD)
ChatLog.config(state=DISABLED)

send = Label(botFrame,text="Enter your Message:",font="Verdana",fg="#5D4037")
entry = Entry(botFrame,bd=3,width=111)


send_btn = Button(botFrame,width=12,text="Send!",fg="black",bg="#BDBDBD",command=setText)
entry.bind("<Return>", setText)


ChatLog.grid(row=0,rowspan = 1,columnspan = 4,sticky = N)
send.grid(row=1,columnspan=5,sticky=W)
entry.grid(row=3,column=0,columnspan=1,sticky = W+S)
send_btn.grid(row=3,column=1,columnspan=3,sticky = E+S)


root.mainloop()
