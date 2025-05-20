## Instruções para utilizar o ficheiro `gui.py`

1. **Certifique-se de que tem o Python instalado**  
   O `gui.py` requer o Python 3.6 ou superior. Pode verificar a sua versão de Python executando:
   ```
   python --version
   ```
   ou
   ```
   python3 --version
   ```

2. **Instale as dependências necessárias**  
   Se o `gui.py` requer bibliotecas externas (por exemplo, `llama-cpp-python`, `langchain-community`, etc.), instale-as utilizando o `pip`. Por exemplo:
   ```
   pip install -r requirements.txt
   ```
   ou instale manualmente:
   ```
   pip install nome_da_biblioteca
   ```
3. **Baixe um llm LLAMA**  
    Baixe um modelo de llm llama de sua preferencia,
    como por exemplo o `DeepSeek-R1-Distill-Llama-8B-Q8_0.gguf`  
    Copie para o mesmo diretorio de `gui.py` 
    reve e atualize o nome na linha 45 de `gui.py` 
4. **Execute o ficheiro `gui.py`**  
   No terminal, navegue até à pasta onde se encontra o `gui.py` e execute:
   ```
   python gui.py
   ```
   ou
   ```
   python3 gui.py
   ```

5. **Utilize a interface gráfica**  
   Após executar o comando acima, a interface gráfica será aberta. Siga as instruções apresentadas na janela para utilizar a aplicação.

6. **Resolução de problemas**  
   - Se receber um erro sobre módulos em falta, instale-os com o `pip`.
   - Certifique-se de que está a utilizar a versão correta do Python.
   - Consulte a documentação ou contacte o autor em caso de dúvidas adicionais.

Bom uso e contribua no projeto!
