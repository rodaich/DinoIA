import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import AsyncOpenAI
import uvicorn

app = FastAPI()

# A chave da API será pega das variáveis de ambiente do Google Cloud
client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    user_input: str
    agent_id: str = "agent_2b602f38211a4003a4e8798a81221d8d5e67e8351f484fe49d"

@app.get("/")
async def root():
    return {"status": "DinoIA Online"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # 1. Cria uma thread (conversa) para o aluno
        thread = await client.beta.threads.create()

        # 2. Adiciona a mensagem do aluno à thread
        await client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=request.user_input
        )

        # 3. Executa o agente (Run)
        run = await client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=request.agent_id
        )

        if run.status == 'completed':
            # 4. Recupera a última mensagem do agente
            messages = await client.beta.threads.messages.list(thread_id=thread.id)
            return {"response": messages.data[0].content[0].text.value}
        else:
            return {"error": f"Run status: {run.status}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
