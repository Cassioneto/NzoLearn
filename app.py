from llama_cpp import Llama
llm = Llama(model_path="/home/vm-dev/Transferências/llama-2-7b-guanaco-qlora.Q2_K.gguf")
output = llm("Q: Name the planets in the solar system? A: ", max_tokens=32, stop=["Q:", "\n"], echo=false)