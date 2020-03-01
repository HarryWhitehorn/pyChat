#pyChat - interface
import tkinter as tk

class Window:
    def __init__(self,title="tk"):
        self.root = tk.Tk()
        self.root.title(title)
        self.out = Out(self.root)
        self.inp = Inp(self.root,output=self.send)
        #pack
        self.out.frame.grid(row=0, column=0, sticky="NSEW")
        self.inp.frame.grid(row=1, column=0, sticky="SEW")
        self.root.grid_columnconfigure(0,weight=1)
        self.root.grid_rowconfigure(0,weight=100)
        self.root.grid_rowconfigure(1,weight=1)
        #data
        self.sending = False
        self.data = None
        
    def send(self,message):
        self.data = message #bytes(message,"utf-8")
        self.sending = True

    def receive(self,message):
        if type(message) == "bytes":
            message = message.decode("utf-8")
        self.out.text.config(text=message)
    
class Out:
    def __init__(self,master,text="out"):
        self.frame = tk.LabelFrame(master,text=text)
        self.text = tk.Label(self.frame,text="test",anchor='w', justify='left')
        #pack
        self.text.pack(anchor='w')
        

class Inp:
    def __init__(self,master,text="in",output=None):
        self.frame = tk.LabelFrame(master,text=text)
        self.output = output
        self.entry = tk.Entry(self.frame)
        self.button = tk.Button(self.frame,text="send",command=self.click)
        #grid
        self.entry.grid(row=0, column=0,sticky="NSEW")
        self.button.grid(row=0, column=1,sticky="NSW")
        self.frame.grid_columnconfigure(0,weight=1)
        self.frame.grid_rowconfigure(0,weight=1)
        self.frame.grid_columnconfigure(1,weight=1)


    def click(self):
        if self.output == None: 
            print(self.entry.get())
        else:
            self.output(self.entry.get())
        self.entry.delete(0, 'end')

if __name__ == "__main__":
    window = Window("Client")
    while True:
        if window.sending:
            window.receive(window.data)
            window.sending = False
        window.root.update() 