import Tkinter as tk
from PIL import Image, ImageTk

import multiprocessing
import signal
from time import sleep

import fnlp
import ftexttospeech
import fspeechtotext
import frecord
import ftoarduino
import unknown_user
import fintro

PATH= '/home/ramesha/PycharmProjects/live'
audio_file='newfile.raw'
nlp_out = ''
flag1 = 0

class receptionistApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageName, PageQuery, PageAutoDetect, PageTest):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def enable_auto(self, cont):
        frame= self.frames[cont]
        frame.tkraise()
        ftexttospeech.texttospeech("Auto detection is enabled")
        global flag1
        flag1 =1

    def disable_auto(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        ftexttospeech.texttospeech("Auto detection is disabled")
        global flag1
        flag1 = 0

    def enter_name(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        ftexttospeech.texttospeech("Please enter your name and stand on the cross")


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.init_window(controller)

    def init_window(self, controller):
        image = Image.open("img1.JPG")
        photo = ImageTk.PhotoImage(image)
        w = tk.Label(self, image=photo, height=100, width=800, bg="blue")
        w.photo = photo
        #w.pack()
        w.place(x=0, y=0)

        welcome = tk.Label(self, text="Welcome to ENTC", fg="blue", font=("Times", 32))
        welcome.place(x=250, y=105)

        bName = tk.Button(self, text="Enter name", font=("Helvetica", 20), bg="black", fg="white",
                          command=lambda: controller.enter_name(PageName))
        bName.place(x=100, y=200)

        bQ = tk.Button(self, text="Ask a question", font=("Helvetica", 20), bg="black", fg="white",
                       command=lambda: controller.show_frame(PageQuery))
        bQ.place(x=500, y=200)

        bAuto = tk.Button(self, text="Enable auto detection", font=("Helvetica", 20), bg="black", fg="white",
                       command=lambda: controller.enable_auto(PageAutoDetect))
        bAuto.place(x=250, y=300)

        bTest = tk.Button(self, text="Test gestures", font=("Helvetica", 20), bg="black", fg="white",
                          command=lambda: controller.show_frame(PageTest))
        bTest.place(x=90, y=400)

        bIntro = tk.Button(self, text="Introduction", font=("Helvetica", 20), bg="black", fg="white",
                          command=lambda: intro())
        bIntro.place(x=510, y=400)

        def intro():
            ftoarduino.introd()
            fintro.intros()

class PageAutoDetect(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.init_window(controller)

    def init_window(self, controller):

        image = Image.open("img1.JPG")
        photo = ImageTk.PhotoImage(image)
        w = tk.Label(self, image=photo, height=100, width=800, bg="blue")
        w.photo = photo
        #w.pack()
        w.place(x=0, y=0)

        lb1 = tk.Label(self, text="Auto detection is enabled", fg="blue", font=("Times", 32))
        lb1.place(x=195, y=200)

        lb2 = tk.Label(self, text="Please ask the questions", fg="blue", font=("Times", 32))
        lb2.place(x=200, y=300)

        bDisable = tk.Button(self, text="Disable auto detection", font=("Helvetica", 20), bg="black", fg="white",
                          command=lambda: controller.disable_auto(StartPage))
        bDisable.place(x=250, y=400)

class PageTest(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.init_window(controller)

    def init_window(self, controller):

        image = Image.open("img1.JPG")
        photo = ImageTk.PhotoImage(image)
        w = tk.Label(self, image=photo, height=100, width=800, bg="blue")
        w.photo = photo
        #w.pack()
        w.place(x=0, y=0)

        lb1 = tk.Label(self, text="Test the gestures", fg="blue", font=("Times", 32))
        lb1.place(x=250, y=105)


        bGreet = tk.Button(self, text="Greet", font=("Helvetica", 20), bg="black", fg="white",width=8,
                           command=lambda: greetcom())
        bGreet.place(x=300, y=200)

        bLeft = tk.Button(self, text="Show left", font=("Helvetica", 20), bg="black", fg="white", width=8,
                           command=lambda: showleftcom())
        bLeft.place(x=300, y=250)

        bRight = tk.Button(self, text="Show right", font=("Helvetica", 20), bg="black", fg="white",width=8,
                           command=lambda: showrightcom())
        bRight.place(x=300, y=300)

        bStart = tk.Button(self, text="Start Page", font=("Helvetica", 20), bg="black", fg="white", width=8,
                           command=lambda: controller.show_frame(StartPage))
        bStart.place(x=300, y=400)

        def greetcom():

            ftoarduino.greet()
            #sleep(5)
            ftexttospeech.texttospeech("Greeting command")

        def showleftcom():

            ftoarduino.showleft()
            #sleep(10)
            ftexttospeech.texttospeech("Showing left direction")

        def showrightcom():

            ftoarduino.showright()
            #sleep(10)
            ftexttospeech.texttospeech("Showing right direction")


class PageName(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def select(value):
            if value == "back":
                entry2 = entry.get()
                p = len(entry2)
                entry.delete(p - 1, tk.END)
            elif value == " Space ":
                entry.insert(tk.END, ' ')

            elif value == " Tab ":
                entry.insert(tk.END, '    ')

            else:
                entry.insert(tk.END, value)

        buttons = [
            'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'back', '7', '8', '9', '-',
            'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '[', ']', '4', '5', '6', '+',
            'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '?', '@', '1', '2', '3', '/',
            ' Space ',
        ]
        lName = tk.Label(self, font=("Helvetica", 16), text='Please enter your name').grid(row=0, columnspan=14)
        entry = tk.Entry(self, width=90)
        entry.grid(row=2, columnspan=20)

        varRow = 3
        varColumn = 0

        for button in buttons:

            command = lambda x=button: select(x)
            if button != " Space ":
                tk.Button(self, text=button, width=4, bg="#000000", fg="#ffffff",
                          activebackground="#ffffff", activeforeground="#000000", relief='raised', padx=4,
                          pady=4, bd=4, command=command).grid(row=varRow, column=varColumn)
            if button == " Space ":
                tk.Button(self, text=button, width=60, bg="#000000", fg="#ffffff",
                          activebackground="#ffffff", activeforeground="#000000", relief='raised', padx=4,
                          pady=4, bd=4, command=command).grid(row=6, columnspan=16)

            varColumn += 1
            if varColumn > 14 and varRow == 3:
                varColumn = 0
                varRow += 1
            if varColumn > 14 and varRow == 4:
                varColumn = 0
                varRow += 1

        bSend = tk.Button(self, font=("Helvetica", 16), text='Send name', command=lambda: sendName(entry.get())).grid(
            row=7, columnspan=16)
        bStart = tk.Button(self, font=("Helvetica", 16), text='Start page', command=lambda: goBack()).grid(row=8,
                                                                                                               columnspan=16)

        image = Image.open("img1.JPG")
        photo = ImageTk.PhotoImage(image)
        w = tk.Label(self, image=photo, height=300, width=800, bg="blue")
        w.photo = photo
        #w.pack()
        w.place(x=0, y=300)

        ans = tk.StringVar()
        ans.set('')
        answer = tk.Label(self, font=("Helvetica", 16), textvariable=ans).grid(row=9, columnspan=16)

        def sendName(name):
            # sentence = 'My name is ' + name
            # answ = fnlp.nlpcall(sentence)
            # ans.set(answ)
            answ= "Please stand on the cross and look at my eyes "+ name
            ans.set(answ)
            ftexttospeech.texttospeech(answ)
            unknown_user.saveface(name)
            answ = "Your name was saved and now you may ask questions."
            ftexttospeech.texttospeech(answ)


        def goBack():
            controller.show_frame(StartPage)
            entry.delete(0, 'end')


class PageQuery(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def select(value):
            if value == "back":
                entry2 = entry.get()
                p = len(entry2)
                entry.delete(p - 1, tk.END)
            elif value == " Space ":
                entry.insert(tk.END, ' ')

            elif value == " Tab ":
                entry.insert(tk.END, '    ')

            else:
                entry.insert(tk.END, value)

        buttons = [
            'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'back', '7', '8', '9', '-',
            'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '[', ']', '4', '5', '6', '+',
            'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '?', '@', '1', '2', '3', '/',
            ' Space ',
        ]
        lName = tk.Label(self, font=("Helvetica", 16), text='Please enter your question').grid(row=0, columnspan=14)
        entry = tk.Entry(self, width=90)
        entry.grid(row=2, columnspan=20)

        varRow = 3
        varColumn = 0

        for button in buttons:

            command = lambda x=button: select(x)
            if button != " Space ":
                tk.Button(self, text=button, width=4, bg="#000000", fg="#ffffff",
                          activebackground="#ffffff", activeforeground="#000000", relief='raised', padx=4,
                          pady=4, bd=4, command=command).grid(row=varRow, column=varColumn)
            if button == " Space ":
                tk.Button(self, text=button, width=60, bg="#000000", fg="#ffffff",
                          activebackground="#ffffff", activeforeground="#000000", relief='raised', padx=4,
                          pady=4, bd=4, command=command).grid(row=6, columnspan=16)

            varColumn += 1
            if varColumn > 14 and varRow == 3:
                varColumn = 0
                varRow += 1
            if varColumn > 14 and varRow == 4:
                varColumn = 0
                varRow += 1

        bSend = tk.Button(self, font=("Helvetica", 16), text='Send text question', command=lambda: sendQ(entry.get())).grid(
            row=7, columnspan=16)
        bStart = tk.Button(self, font=("Helvetica", 16), text='Start Page', command=lambda: goBack()).grid(row=9,
                                                                                                           columnspan=16)
        bRecord = tk.Button(self, font=("Helvetica", 16), text='Audio question', command=lambda: audioQ()).grid(
            row=8, columnspan=16)
        bEnd = tk.Button(self, font=("Helvetica", 16), text='End conversation', command=lambda: convoE()).grid(
            row=10, columnspan=16)


        image = Image.open("img1.JPG")
        photo = ImageTk.PhotoImage(image)
        w = tk.Label(self, image=photo, height=300, width=800, bg="blue")
        w.photo = photo
        #w.pack()
        w.place(x=0, y=350)

        ans = tk.StringVar()
        ans.set('')
        answer = tk.Label(self, font=("Helvetica", 16), textvariable=ans).grid(row=11, columnspan=16)

        def convoE():
            print "end convo"
            ftoarduino.endConv()

        def sendQ(question):
            answ= fnlp.nlpcall(question)
            ans.set(answ)

            ftoarduino.toarduino(answ)
            #sleep(5)
            ftexttospeech.texttospeech(answ)
            print "end"

        def goBack():
            controller.show_frame(StartPage)
            ans.set('')
            entry.delete(0, 'end')

        def audioQ():
            flag=0
            nlp_out=''
            frecord.record()

            # text_out = fspeechtotext.speechtotext(audio_file, PATH)
            # nlp_out = fnlp.nlpcall(text_out)
            # ans.set(nlp_out)
            # ftexttospeech.texttospeech(nlp_out)
            #ftoarduino.toarduino(nlp_out)

            signal.signal(signal.SIGALRM, handler)
            signal.alarm(20)
            try:
                text_out = fspeechtotext.speechtotext(audio_file, PATH)
            except Exception, exc:
                print exc
                text_out="Timeout. Please try again"
                ans.set("Timeout. Please try again")
                ftexttospeech.texttospeech(text_out)
            else:
                print text_out
                nlp_out = fnlp.nlpcall(text_out)
                ans.set(nlp_out)
                # ftexttospeech.texttospeech(nlp_out)
                flag=1
            signal.alarm(0)

            print "to arduino"
            if flag==1:
                ftoarduino.toarduino(nlp_out)
                #sleep(5)
                ftexttospeech.texttospeech(nlp_out)
                print "end"

        def handler(signum, frame):
            print "Timeout! Please try again"
            raise Exception("end of time")

        #     audi = multiprocessing.Process(target=audioprocess)
        #
        #     audi.start()
        #     audi.join(25)
        #
        #     if audi.is_alive():
        #         global nlp_out
        #         nlp_out= "Timeout. Please try again"
        #         print nlp_out
        #             # Terminate
        #         audi.terminate()
        #         audi.join()
        #         ans.set(nlp_out)
        #         ftexttospeech.texttospeech(nlp_out)
        #
        #     else:
        #         global nlp_out
        #         ans.set(nlp_out)
        #         ftexttospeech.texttospeech(nlp_out)
        #         ftoarduino.toarduino(nlp_out)
        #     print "end"
        #
        # def audioprocess():
        #     global nlp_out
        #     text_out = fspeechtotext.speechtotext(audio_file, PATH)
        #     nlp_out = fnlp.nlpcall(text_out)
        #     # ans.set(nlp_out)
        #     # ftexttospeech.texttospeech(nlp_out)
        #     # ftoarduino.toarduino(nlp_out)
        #     # print "end"





# app = receptionistApp()
# app.geometry("800x480")
# app.title("ENTC Robot Receptionist")
# app.mainloop()