import os
from tkinter import *
import pandas as pd




# UI set up
root = Tk()


root.title("Zoom Automator")
scroll = Scrollbar(root)
canvas = Canvas(root, width = 350, height = 350)
canvas.grid(columnspan = 7, rowspan = 7)
left_margin = Label(root, text = "  ", padx = 7)
left_margin.grid(row = 0, column = 0)
bottom_margin = Label(root, text = "  ", pady = 7)
bottom_margin.grid(row = 7, column = 0)
right_margin = Label(root, text = "  ", padx = 7)
right_margin.grid(row = 0, column = 7)
top_margin = Label(root, text = "  ", padx = 7)
top_margin.grid(row = 0, column = 3)

r = IntVar()
link_id_label = Label(root, text = "Link or ID", font = ("TkDefaultFont", 10))
passw_label = Label(root, text = "Password", font = ("TkDefaultFont", 10))
join_time = Label(root, text = "Start Time", font = ("TkDefaultFont", 10))
leave_time = Label(root, text = "Leave Time", font = ("TkDefaultFont", 10))
nick_name = Label(root, text = "Nickname", font = ("TkDefaultFont", 10))
check_btn = Checkbutton(root, variable=r, onvalue = 1, offvalue = 0)

link_id_label.grid(row = 1, column = 1)
passw_label.grid(row = 2, column = 1)
join_time.grid(row = 3, column = 1)
leave_time.grid(row = 4, column = 1)
nick_name.grid(row = 5, column = 1)
check_btn.grid(row = 6, column = 1)


entry1 = Entry(root, width = 20)
entry1.grid(row = 1, column = 2)
entry2 = Entry(root, width = 20)
entry2.grid(row = 2, column = 2)
entry3 = Entry(root, width = 20)
entry3.grid(row = 3, column = 2)
entry4 = Entry(root, width = 20)
entry4.grid(row = 4, column = 2)
entry5 = Entry(root, width = 20)
entry5.grid(row = 5, column = 2)
check_text = Label(root, text = "Leave zoom when 80%\nof participants have left")
check_text.grid(row = 6, column = 2)

divider = Label(root, text = "  ", padx = 20)
divider.grid(row = 1, column = 3)

text_box = Text(root, height = 15, width = 30, state = DISABLED, pady = 0)
text_box.grid(row = 2, column = 4, rowspan = 4, columnspan = 2, sticky = N+S+E+W, pady = 20)
text_box.configure(yscrollcommand=scroll.set)


# Interaction setup for Add and Clear button
listZoom = []

def clickClear():
    # Clears textbox and exits
    listZoom.clear()
    text_box.config(state = NORMAL)
    text_box.delete("1.0", "end")
    text_box.config(state = DISABLED)
    
    # Display tutorial
    #... to be implemented
    
    # Clears CSV
    df = pd.read_csv("C:\\Users\\giang\\zoom_auto2\\references\\record.csv")
    colNames = df.columns
    df_new = pd.DataFrame(data=[], columns=colNames)
    df_new.to_csv("C:\\Users\\giang\\zoom_auto2\\references\\record.csv", index=False)
    
    # Enabled buttons again
    add_btn.config(state = NORMAL)
    start_btn.config(state = NORMAL)
    
    #os._exit(1)
    os.system("taskkill /im ZoomAuto.exe")

clear_btn = Button(root, text = "CLEAR", font = ("TkDefaultFont", 10), padx = 22, borderwidth = 3, command = clickClear)
clear_btn.grid(row = 6, column = 4, columnspan = 2, pady = 0)



def clickAdd():
    # Get the entries and create new zoom object
    if (r.get() == 1):
        autoL = "True"
    else: 
        autoL = "False"
    print("r = " + str(r))
    newZoom = [entry1.get(), entry2.get(), entry3.get(), entry4.get(), autoL, entry5.get()]
    
    # Clear textboxes
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    
    
    # Add to listZoom and input data into textbox
    listZoom.append(newZoom)
    text_box.config(state = NORMAL)
    text_box.delete("1.0", "end")
    for i in listZoom:
        text_box.insert(END, i[5] + " (S)" + i[2] + " (L)" + i[3] + "\n")
    text_box.config(state = DISABLED)
        
add_btn = Button(root, text = "ADD", font = ("TkDefaultFont", 10), padx = 30, borderwidth = 3, command = clickAdd)
add_btn.grid(row = 1, column = 4, pady = 15)              
                

def clickStart():
    # sets add button and start button to disabled
    start_btn.config(state = DISABLED)
    add_btn.config(state = DISABLED)
    
    # Adds elements of listZoom onto CSV
    for i in listZoom:
        df_old = pd.read_csv("C:\\Users\\giang\\zoom_auto2\\references\\record.csv")
        newData = [[i[0],i[1],i[2],i[3],i[4],i[5]]]
        colNames = df_old.columns
        df_new = pd.DataFrame(data=newData, columns=colNames)
        df_complete = pd.concat([df_old, df_new], axis = 0)
        df_complete.to_csv("C:\\Users\\giang\\zoom_auto2\\references\\record.csv", index=False)  
    print("data appended")
    
    #Start ZoomAuto.exe
    os.startfile("C:\\Users\\giang\\zoom_auto2\\dist\\ZoomAuto\\ZoomAuto.exe")
    print("exe launched")
        
        
start_btn = Button(root, text = "START", font = ("TkDefaultFont", 10), padx = 22, borderwidth = 3, command = clickStart)
start_btn.grid(row = 1, column = 5, pady = 0)

root.mainloop()




