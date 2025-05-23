import tkinter as tk
import tkinter.font as tkFont
from tkinter import scrolledtext
from tkinter import filedialog
import shutil
import os
import threading
import sys

# Corrigir o problema do diretório lib
try:
    import llama_cpp
except (ImportError, FileNotFoundError) as e:
    # Criar a pasta lib se não existir
    lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_internal", "llama_cpp", "lib")
    if not os.path.exists(lib_dir):
        os.makedirs(lib_dir, exist_ok=True)
    import llama_cpp

# Importar llama_index (opcional, para usar o arquivo VERSION)

from llama_cpp import Llama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader

# Função para obter o caminho do recurso, seja no executável ou no sistema de arquivos
def resource_path(relative_path):
    """ Obter caminho absoluto para recursos, funciona para dev e para PyInstaller """
    try:
        # PyInstaller cria um diretório temporário e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class App:
    txtPromp= 0
    txtChat= 0
    pdfList= 0

    # Usar resource_path para localizar o modelo
    model_path = resource_path("DeepSeek-R1-Distill-Llama-8B-Q8_0.gguf")
    
    llm = Llama(model_path=model_path,
        n_ctx=2048,
        n_threads=16,
        n_batch=512,
        temperature=0.7,
        top_p=0.9,
        verbose=False
        )
    vectorstore=0

    def load_documents(directory_path):
    # Carregador para ficheiros de texto no diretório especificado
      loader = DirectoryLoader(
        directory_path,
        glob="**/*.txt",
        loader_cls=TextLoader
      )
      documents = loader.load()
    
    # Dividir documentos em chunks menores
      text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
      )
      texts = text_splitter.split_documents(documents)
      # Apagar ficheiros após carregamento
      # Apagar todos os ficheiros na pasta documents após carregamento
      for filename in os.listdir(directory_path):
          file_path = os.path.join(directory_path, filename)
          try:
              if os.path.isfile(file_path):
                  os.remove(file_path)
          except Exception as e:
              print(f"Erro ao apagar ficheiro {file_path}: {e}")
      return texts

    def create_vectorstore(texts):
    # Usar embeddings do HuggingFace (modelo mais leve)
      embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Criar base de dados vectorial
      vectorstore = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory="./chroma_db"
      )
      return vectorstore
    def update_vectorstore(self, texts):
        # Usar embeddings do HuggingFace (modelo mais leve)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Carregar vectorstore existente
        if os.path.exists("./chroma_db"):
            vectorstore = Chroma(
                persist_directory="./chroma_db",
                embedding_function=embeddings
            )
            
          
            # Adicionar novos documentos
            vectorstore.add_documents(texts)
            vectorstore.persist()
            self.vectorstore = vectorstore
            return vectorstore
        else:
            # Se não existir, criar novo
            self.vectorstore = self.create_vectorstore(texts)
            return self.vectorstore
        
    # Função para pesquisar documentos relevantes no vectorstore
    def retrieve_context(self, query, k=3):
                        
        try:
            # Buscar documentos similares à query
            docs = self.vectorstore.similarity_search(query, k=k)
            if not docs:
                return ""
                
            # Formatar os documentos encontrados
            context_text = "\n".join([doc.page_content for doc in docs])
            return context_text
        except Exception as e:
            print(f"Erro ao recuperar contexto: {e}")
            return ""
        
    def __init__(self, root):

        #setting title
        root.title("🎓NzoLearn- Chat with pdf")
        #setting window size
        width=600
        height=520
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
        #pdfList["justify"] = "center"
        pdfList.place(x=440,y=50,width=152,height=322)
        #pdfList.insert(tk.END, "test")
        self.pdfList = pdfList

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
        buttonSendPrompt["text"] = "Enviar Prompt"
        buttonSendPrompt.place(x=440,y=400,width=152,height=84)
        buttonSendPrompt["command"] = self.buttonSendPrompt_command
        self.buttonSendPrompt = buttonSendPrompt  # Guardar referência ao botão

        #textChat=tk.Entry(root, height=10 )
        textChat= scrolledtext.ScrolledText(root, height=10)
        textChat["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=12)
        textChat["font"] = ft
        textChat["fg"] = "#333333"
        #textChat["justify"] = "left"
        #textChat["text"] = "Olá eu sou o NzoLearn, seu assistente de estudos."
        textChat.place(x=0,y=20,width=431,height=356)
        textChat.insert(tk.END, "\n Olá eu sou o 🎓NzoLearn, seu assistente de estudos.\n") 
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
        
        # Adicionar label abaixo do campo de texto
        promptLabel = tk.Label(root)
        promptLabel["font"] = tkFont.Font(family='Times',size=8)
        promptLabel["fg"] = "#666666"
        promptLabel["text"] = "Digite sua pergunta aqui..."
        promptLabel.place(x=10,y=484,width=422,height=15)
        self.promptLabel = promptLabel
        # Adicionar label de creditod
        creditsLabel = tk.Label(root)
        creditsLabel["font"] = tkFont.Font(family='Times',size=12)
        creditsLabel["fg"] = "#666666"
        creditsLabel["text"] = "Feito Por Cássio Neto"
        creditsLabel.place(x=10,y=500,width=422,height=15)
        self.promptLabel = promptLabel

        # Adicionar eventos para o campo de texto
        def on_entry_focus_in(event):
            self.promptLabel.config(fg="#cccccc")
            
        def on_entry_focus_out(event):
            if not self.txtPromp.get():
                self.promptLabel.config(fg="#666666")
                
        textPrompt.bind("<FocusIn>", on_entry_focus_in)
        textPrompt.bind("<FocusOut>", on_entry_focus_out)
        
    def buttonAddPdf_command(self):
        # Abrir janela de seleção de ficheiro
        filename = filedialog.askopenfilename(
            title="Selecionar Documento",
            filetypes=[
                ("Documentos", "*.pdf *.txt"),
                ("Ficheiros PDF", "*.pdf"),
                ("Ficheiros TXT", "*.txt")
            ]
        )
        
        if not filename:
            return  # Utilizador cancelou a seleção
            
        # Verificar a extensão do ficheiro usando os três últimos caracteres
        nome_ficheiro = os.path.basename(filename)
        extensao = nome_ficheiro[-4:].lower() if len(nome_ficheiro) >= 4 else ""
        
        if not (extensao.endswith('.pdf') or extensao.endswith('.txt')):
            self.txtChat.insert(tk.END, "\n❌ Erro: Apenas ficheiros PDF e TXT são suportados.\n")
            self.txtChat.see(tk.END)
            return
        
        # Criar pasta 'documents' se não existir
        if not os.path.exists("documents"):
            os.makedirs("documents")
       
        # Copiar ficheiro para a pasta documents
        destino = os.path.join("./documents", nome_ficheiro)
        shutil.copy2(filename, destino)
        
        # Adicionar nome do ficheiro à lista
        self.pdfList.insert(tk.END, nome_ficheiro)
        self.txtChat.insert(tk.END, "\n🛠️Carregado: " + nome_ficheiro + "\n")
        self.txtChat.see(tk.END) 
        
        # Processar o documento
        texts = self.load_documents("./documents")  # Pasta com os documentos
        vectorstore = self.update_vectorstore(texts)
        print("Documento carregado com sucesso")


    def buttonSendPrompt_command(self):
        prompt_text = self.txtPromp.get()
        if not prompt_text:
            return
            
        self.txtChat.insert(tk.END, "\n 🤵🏾‍♂️Eu: " + prompt_text)
        self.txtChat.see(tk.END)  # Auto-scroll para ver a nova mensagem
        
        # Limpar o campo de entrada
        self.txtPromp.delete(0, tk.END)
        
        # Desativar o botão de envio enquanto processa
        self.buttonSendPrompt.config(state="disabled", text="A processar...")
        
        # Mostrar mensagem de processamento
        self.txtChat.insert(tk.END, "\\n 🎓NzoLearn: A processar resposta...")
        self.txtChat.see(tk.END)
        
        # Função para processar a resposta em thread separada
        def process_response():
            try:
                # Recuperar contexto relevante do vectorstore
                context = self.retrieve_context(prompt_text)
                #self.txtChat.insert(tk.END, "contexto:"+ context+ "\n cc \n")
                # Formato de prompt RAG com contexto e instruções claras
                if context:
                    formatted_prompt = f"""
Com base nos seguintes documentos:

{context}

Responda à seguinte pergunta do utilizador de forma clara, útil e concisa.
Se a resposta não estiver nos documentos, diga claramente que não tem essa informação.

Pergunta: {prompt_text}

Resposta:"""
                else:
                    # Fallback para quando não há contexto disponível
                    formatted_prompt = f"""
A seguir está uma pergunta do utilizador. Responda de forma clara, útil e concisa.

Pergunta: {prompt_text}

Resposta:"""
                
                # Gerar resposta com parâmetros melhores
                output = self.llm(formatted_prompt, 
                                max_tokens=512,  # Aumentar tokens para respostas mais completas
                                stop=["Pergunta:", "\n\n"],  # Parar em novas perguntas
                                echo=False)
                
                response_text = output["choices"][0]["text"].strip()
                
                # Atualizar a UI na thread principal
                root.after(0, self.update_chat_with_response, response_text)
            except Exception as e:
                # Em caso de erro, mostrar mensagem na thread principal
                root.after(0, self.handle_response_error, str(e))
            finally:
                # Reativar o botão na thread principal quando terminar
                root.after(0, lambda: self.buttonSendPrompt.config(state="normal", text="Enviar Prompt"))
        
        # Iniciar thread para processar resposta
        response_thread = threading.Thread(target=process_response)
        response_thread.daemon = True  # Thread será encerrada quando o programa principal terminar
        response_thread.start()
    
    def update_chat_with_response(self, response_text):
        # Remover mensagem de processamento
        self.txtChat.delete("end-1c linestart", "end")
        # Adicionar resposta real
        self.txtChat.insert(tk.END, "\n 🎓NzoLearn: " + response_text + "\n")
        self.txtChat.see(tk.END)  # Auto-scroll para ver a resposta
    
    def handle_response_error(self, error_message):
        # Remover mensagem de processamento
        self.txtChat.delete("end-1c linestart", "end")
        # Mostrar mensagem de erro
        self.txtChat.insert(tk.END, "\n ❌ Erro ao processar resposta: " + error_message + "\n")
        self.txtChat.see(tk.END)


if __name__ == "__main__":
    # Apagar a pasta "documents" ao iniciar, se existir
    if os.path.exists("documents"):
        try:
            shutil.rmtree("documents")
            print("Pasta documents apagada com sucesso")
        except Exception as e:
            print(f"Erro ao apagar a pasta documents: {e}")
    
    root = tk.Tk()
    app = App(root)
    root.mainloop()