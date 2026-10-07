import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama # Biblioteca do Ollama
import uvicorn

app = FastAPI()

# URL do seu servidor Ollama (Ex: http://seu-ip:11434)
# Se o Ollama estiver na mesma máquina do código, use http://localhost:11434
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.environ.get("OLLAMA_MODEL", "llama3") # Ou mistral, phi3, etc.

# A PERSONA DO DINOIA (O Prompt de Sistema)
SYSTEM_PROMPT = """Crie um sistema de consultoria fitness para um aplicativo com as seguintes funcionalidades:
- Substituir exercícios por outros semelhantes do mesmo grupo muscular.
- Montar treinos e dietas personalizados.
- Realizar avaliações musculares e posturais a partir de fotos.
- Coletar contexto completo (água, dieta, treino, resultados).
- Fornecer análise detalhada e sugestões para o personal trainer.

Siga estas etapas para cada resposta:
1. Liste e descreva todos os dados analisados.
2. Realize a análise detalhada justificando cada observação.
3. Elabore sugestões personalizadas para treino e dieta.
4. Conclua com sugestões técnicas para o personal trainer.

Formato de saída: Relatório organizado ou JSON se solicitado.
Responda sempre em português."""

class ChatRequest(BaseModel):
    user_input: str

@app.get("/")
async def root():
    return {"status": "DinoIA com Ollama Online"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Configura o cliente do Ollama para apontar para o host correto
        client = ollama.Client(host=OLLAMA_HOST)
        
        response = client.chat(model=MODEL_NAME, messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': request.user_input},
        ])
        
        return {"response": response['message']['content']}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no Ollama: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
