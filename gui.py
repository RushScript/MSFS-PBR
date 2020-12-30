from tkinter import * 

# Button 1 function
def btnClickFunction():
    btn1 = Button(root, text='Auto-Push Back (NO DATA FOUND)', state=DISABLED, bg='white', fg="white", font=('arial', 10, 'normal'), command=btnClickFunction).place(x=5, y=12)
    print('Auto Push Back')


# Button 2 function
def btnClickFunction2():
    btn2 = Button(root, text='Starting Push Back...', state=DISABLED, bg='white', fg="white", font=('arial', 10, 'normal'), command=btnClickFunction2).place(x=5, y=52)
    print('Start Push Back')


# Button 3 function
def btnClickFunction3():
    btn3 = Button(root, text='Recording Push Back...', state=DISABLED, bg='red', fg="black", font=('arial', 10, 'normal'), command=btnClickFunction3).place(x=5, y=92)
    print('Record Push Back')

root = Tk()

# This is the section of code which creates the main window
root.geometry('395x390')
root.configure(background='#6B6B6B')
root.title('Push Back Recorder')
root.resizable(width=False, height=False)
root.attributes('-topmost', True)
root.update()


# GUI Buttons
btn1 = Button(root, text='Auto-Push Back', bg='#6B6B6B', fg="white", font=('arial', 10, 'normal'), command=btnClickFunction).place(x=5, y=12)
btn2 = Button(root, text='Start Push Back', bg='#6B6B6B', fg="white", font=('arial', 10, 'normal'), command=btnClickFunction2).place(x=5, y=52)
btn3 = Button(root, text='Record Push Back', bg='#6B6B6B', fg="white", font=('arial', 10, 'normal'), command=btnClickFunction3).place(x=5, y=92)


# GUI Canvas images
HowToImg= Canvas(root, height=190, width=380, bd=0, highlightthickness=0, relief='ridge')
picture_file = PhotoImage(file = 'howto.gif')
HowToImg.create_image(380, 0, anchor=NE, image=picture_file)
HowToImg.place(x=5, y=152)

Logo= Canvas(root, height=100, width=100, bd=0, highlightthickness=0, relief='ridge')
picture_fileL = PhotoImage(file = 'logo.gif')  
Logo.create_image(100, 0, anchor=NE, image=picture_fileL)
Logo.place(x=285, y=0)


# GUI Labels
lbl1 = Label(root, text='* Remember to keep this window focused while using manual/record push back', bg='#6B6B6B', fg="#ffc000", font=('arial', 7, 'normal')).place(x=5, y=362)
lbl2 = Label(root, text='SimConnect: Not linked', bg='#6B6B6B', fg="#ffc000", font=('arial', 9, 'normal')).place(x=250, y=83)

root.mainloop()


