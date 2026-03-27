```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import torch.nn as nn
from transformers import AutoModelForCausalLM, AutoTokenizer

app = FastAPI(title="Latent Protocol API - Encoder")

# 1. Define the Bridge architecture to receive the saved weights
class LatentBridge(nn.Module):
    def __init__(self, hidden_dim):
        super().__init__()
        self.projection = nn.Linear(hidden_dim, hidden_dim)

    def forward(self, x):
        return self.projection(x)

# 2. State management for the frozen models
class MLState:
    agent_a = None
    tokenizer = None
    bridge = None
    device = "cuda" if torch.cuda.is_available() else "cpu"

state = MLState()

# 3. Initialization (Runs once on server startup)
@app.on_event("startup")
async def load_artifacts():
    print("Mounting artifacts to VRAM...")
    
    # In production, point this to your saved 'agent_a_v1' directory
    model_path = "Qwen/Qwen2.5-0.5B" 
    
    state.tokenizer = AutoTokenizer.from_pretrained(model_path)
    state.agent_a = AutoModelForCausalLM.from_pretrained(
        model_path, 
        torch_dtype=torch.bfloat16
    ).to(state.device)
    
    # Freeze Agent A to prevent accidental belief updates
    state.agent_a.eval()
    for param in state.agent_a.parameters():
        param.requires_grad = False
        
    hidden_dim = state.agent_a.config.hidden_size
    state.bridge = LatentBridge(hidden_dim).to(state.device).to(torch.bfloat16)
    
    # Load the specific mathematical transformation discovered by the autoresearch loop
    # state.bridge.load_state_dict(torch.load("bridge_v1.pt"))
    state.bridge.eval()
    
    print("System armed and ready.")

# 4. Define the API schema
class EncodeRequest(BaseModel):
    text: str

class EncodeResponse(BaseModel):
    latent_vector: list[float]
    dimensions: int

# 5. The Execution Endpoint
@app.post("/encode_latent", response_model=EncodeResponse)
async def encode_latent(request: EncodeRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text payload required.")
        
    try:
        inputs = state.tokenizer(request.text, return_tensors="pt").to(state.device)
        
        # Execute the forward pass mathematically (no gradient tracking)
        with torch.no_grad():
            outputs = state.agent_a(**inputs, output_hidden_states=True)
            message_vector = outputs.hidden_states[-1][:, -1:, :]
            
            latent_coordinate = state.bridge(message_vector)
            
        # Serialize the tensor into a standard JSON array
        vector_list = latent_coordinate.squeeze().cpu().tolist()
        
        return EncodeResponse(
            latent_vector=vector_list,
            dimensions=len(vector_list)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

```
