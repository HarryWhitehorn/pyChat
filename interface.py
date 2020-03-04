#pyChat - interface
import tkinter as tk
import tkinter.messagebox as messagebox
import encrypt

class Error:
    def __init__(self,title="Error 404",message="Error Not Found"):
        messagebox.showerror(title=title,message=message)


class EntryPlaceholder:
    def __init__(self,master,text="",password=False):
        self.root = master
        self.text = text
        if password:
            self.entry = tk.Entry(self.root,show="*")
        else:
            self.entry = tk.Entry(self.root)
        self.ghostColor = "grey"
        self.textColor = "black"
        #bind
        self.entry.bind("<FocusIn>", self.ghostBust)
        self.root.bind("<FocusOut>", self.ghost)
        #g
        self.ghost()
    
    def ghost(self,*args):
        if self.entry.get() == "":
            self.entry.config(foreground=self.ghostColor)
            self.entry.insert(0,self.text)

    def ghostBust(self,*args):
        if self.entry.get() == self.text:
            self.entry.config(foreground=self.textColor)
            self.entry.delete('0', 'end')
    
    def get(self):
        return(self.entry.get())


class LabelEntry:
    def __init__(self,master,labelText="",defaultText="",password=False):
        self.root = master
        self.frame = tk.Frame(self.root)
        #elements
        self.label = tk.Label(self.frame,text=labelText)
        self.entry = EntryPlaceholder(self.frame,defaultText,password=password)
        #packing
        self.label.grid(row=0,column=0)
        self.entry.entry.grid(row=0,column=1)

    def get(self):
        return(self.entry.get())

    def pack(self):
        self.frame.pack()

    def grid(self,row,column):
        self.frame.grid(row=row,column=column)
        

class LoginWindow:
    def __init__(self,master=None):
        if master == None: master = tk.Tk()
        self.root = master
        self.root.title("Login")
        #self.root.geometry("500x500")
        #user
        self.userFrame = tk.LabelFrame(master,text="User")
        self.entryName = LabelEntry(self.userFrame,"Username:")
        self.entryPassword = LabelEntry(self.userFrame,"Password:",password=True)
        self.entryName.grid(row=0,column=0)
        self.entryPassword.grid(row=0,column=1)
        #sever
        self.severFrame = tk.LabelFrame(master,text="Server:")
        self.entryAddr = LabelEntry(self.severFrame,"Address:","127.0.0.1")
        self.entryPort = LabelEntry(self.severFrame,"Port:","8080")
        self.entryAddr.grid(row=0,column=0)
        self.entryPort.grid(row=0,column=1)
        #Go
        self.goButton = tk.Button(self.root,text="Go",command=self.click)
        self.root.bind('<Return>', self.click)
        #pack
        self.userFrame.grid(row=0,column=0)
        self.severFrame.grid(row=1,column=0)
        self.goButton.grid(row=2,column=0)

    def click(self,*args):
        self.data = {
        "username":self.entryName.get().replace("!","."),
        "password":encrypt.encrypt(self.entryPassword.get()),
        "addr":self.entryAddr.get(),
        "port":int(self.entryPort.get())
        }
        self.root.destroy()


class ChatWindow:
    def __init__(self,title="tk"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("500x500")
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
        self.root.bind('<Return>', self.inp.click)
           
    def send(self,message):
        self.data = message.replace("|","¦") #bytes(message,"utf-8")
        self.sending = True

    def receive(self,message):
        if type(message) == "bytes":
            message = message.decode("utf-8")
        self.out.text.insert(tk.END, str(message))
        """
        if type(message) == "bytes":
            message = message.decode("utf-8")
        self.out.text.config(text=message)
        """


class Out:
    def __init__(self,master,text="out"):
        self.frame = tk.LabelFrame(master,text=text)
        self.text = tk.Listbox(self.frame)
        #self.text = tk.Label(self.frame,text="test\n\n\n\n\n\n\nhello",anchor='w', justify='left')
        self.scroll = tk.Scrollbar(self.frame,command=self.text.yview)
        #pack
        self.text.grid(row=0, column=0, sticky="NSWE")
        self.scroll.grid(row=0, column=1, sticky="NSE")
        self.frame.grid_columnconfigure(0,weight=100)
        self.frame.grid_columnconfigure(1,weight=1)
        self.frame.grid_rowconfigure(0,weight=1)


class Inp:
    def __init__(self,master,text="in",output=None):
        self.frame = tk.LabelFrame(master,text=text)
        self.output = output
        self.entry = tk.Entry(self.frame)
        self.button = tk.Button(self.frame,text="send",command=self.click)
        #grid
        self.entry.grid(row=0, column=0,sticky="NSEW")
        self.button.grid(row=0, column=1,sticky="NSW")
        self.frame.grid_columnconfigure(0,weight=100)
        self.frame.grid_columnconfigure(1,weight=1)

    def click(self,*args):
        if self.output == None: 
            print(self.entry.get())
        else:
            self.output(self.entry.get())
        self.entry.delete(0, 'end')


if __name__ == "__main__":
    #new = Error("ConnectionResetError")
    root = tk.Tk()
    login = LoginWindow(root)
    login.root.mainloop()
    """
    window = ChatWindow("Client")
    while True:
        if window.sending:
            window.receive(window.data)
            window.sending = False
        window.root.update() 
    """