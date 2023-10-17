import tkinter as tk
import tkinter.font as tkFont
from tkinter import scrolledtext
from llama_cpp import Llama


class App:
    txtPromp= 0;
    txtChat= 0;1
    llm = Llama(model_path="/home/vm-dev/Transferências/ll.guff")

    def __init__(self, root):
        #setting title
        root.title("NzoLearn- Chat with pdf")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        pdfList=tk.Listbox(root)
        pdfList["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        pdfList["font"] = ft
        pdfList["fg"] = "#333333"
        pdfList["justify"] = "center"
        pdfList.place(x=440,y=50,width=152,height=322)

        buttonAddPdf=tk.Button(root)
        buttonAddPdf["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        buttonAddPdf["font"] = ft
        buttonAddPdf["fg"] = "#000000"
        buttonAddPdf["justify"] = "center"
        buttonAddPdf["text"] = "Adicionar PDF"
        buttonAddPdf.place(x=440,y=20,width=154,height=30)
        buttonAddPdf["command"] = self.buttonAddPdf_command

        buttonSendPrompt=tk.Button(root)
        buttonSendPrompt["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        buttonSendPrompt["font"] = ft
        buttonSendPrompt["fg"] = "#000000"
        buttonSendPrompt["justify"] = "center"
        buttonSendPrompt["text"] = "Enviar Pront"
        buttonSendPrompt.place(x=440,y=400,width=152,height=84)
        buttonSendPrompt["command"] = self.buttonSendPrompt_command

        #textChat=tk.Entry(root, height=10 )
        textChat= scrolledtext.ScrolledText(root, height=10)
        #textChat["borderwidth"] = "1px"
        #ft = tkFont.Font(family='Times',size=10)
        #textChat["font"] = ft
        #textChat["fg"] = "#333333"
        #textChat["justify"] = "center"
        #textChat["text"] = "Olá eu sou o NzoLearn, seu assistente de estudos."
        textChat.place(x=0,y=20,width=431,height=356)
        textChat.insert(tk.END, "\n Olá eu sou o NzoLearn, seu assistente de estudos.") 
        self.txtChat = textChat
        
        textPrompt=tk.Entry(root)
        
        textPrompt["borderwidth"] = "2px"
        ft = tkFont.Font(family='Times',size=12)
        textPrompt["font"] = ft
        textPrompt["fg"] = "#333333"
        textPrompt["justify"] = "center"
        textPrompt["text"] = ""
        textPrompt.place(x=10,y=400,width=422,height=84)
        self.txtPromp = textPrompt
        
    def buttonAddPdf_command(self):
        print("command")


    def buttonSendPrompt_command(self):
        output = app.llm(" "+app.txtPromp.get(), max_tokens=1, stop=["Q:", "\n"], echo=False)
        app.txtChat.insert(tk.END, "\n Eu: "+app.txtPromp.get())
        app.txtChat.insert(tk.END, "\n -Nzo:"+ output["choices"][0]["text"])        
        app.txtPromp["text"] = ""
        


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    app.txtChat.insert(tk.END, "\n Olá eu sou o NzoLearn, seu assistente de estudos.")
