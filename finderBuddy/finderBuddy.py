# create a splash screen, 80% of display screen size, centered,
# displaying a GIF image with needed info, disappearing after 5 seconds
import os
from Tkinter import *
import ttk

from Tkconstants import HORIZONTAL

root = Tk()
# show no frame
root.overrideredirect(True)
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry('%dx%d+%d+%d' % (width*0.5, height*0.4, width*0.25, height*0.3))


image_file = "fbsplash.gif"
#assert os.path.exists(image_file)
# use Tkinter's PhotoImage for .gif files
image = PhotoImage(file=image_file)
canvas = Canvas(root, height=height*0.35, width=width*0.5, bg="grey")
canvas.create_image(width*0.5/2, height*0.35/2, image=image)
canvas.pack()

progressbar = ttk.Progressbar(orient=HORIZONTAL, length=700, mode='determinate')
#label.pack(side=TOP)
progressbar.pack(side=BOTTOM)#
progressbar.start()


# show the splash screen for 5000 milliseconds then destroy
root.after(2000, root.destroy)
#progressbar.stop()
root.mainloop()
# your console program can start here ...heya

import msgbox

#os.system('msgbox.py')
#print "How did you like my informative splash screen?"