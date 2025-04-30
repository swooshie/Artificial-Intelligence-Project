import asyncio
import httpx
from typing import List, Dict, Optional
from pydantic import BaseModel
import json

# Configuration
OPENROUTER_API_KEY = "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"  # Replace with your actual API key
OPENROUTER_API_URL = "https://openrouter.ai/api/v1"

# Models
class LLM(BaseModel):
    id: str
    name: str
    provider: str
    capabilities: List[str]
    cost_prompt: float  # $ per 1k tokens
    cost_completion: float  # $ per 1k tokens

class Request(BaseModel):
    id: str
    required_capability: str
    prompt: str
    max_tokens: int

class OpenRouterClient:
    def __init__(self):
        self.session = httpx.AsyncClient()
        self.headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        self.available_llms = self._initialize_llms()

    def _initialize_llms(self) -> List[LLM]:
        """Initialize with some popular LLMs available on OpenRouter"""
        return [
            LLM(
                id="openai/gpt-4",
                name="GPT-4",
                provider="OpenAI",
                capabilities=["coding", "multilingual", "long-context", "general"],
                cost_prompt=0.03,
                cost_completion=0.06
            ),
            LLM(
                id="anthropic/claude-3-opus",
                name="Claude 3 Opus",
                provider="Anthropic",
                capabilities=["coding", "multilingual", "safe-content", "long-context"],
                cost_prompt=0.015,
                cost_completion=0.075
            ),
            LLM(
                id="google/gemini-pro",
                name="Gemini Pro",
                provider="Google",
                capabilities=["coding", "multilingual", "general"],
                cost_prompt=0.0005,
                cost_completion=0.0015
            ),
            LLM(
                id="meta-llama/llama-3-70b-instruct",
                name="Llama 3 70B",
                provider="Meta",
                capabilities=["coding", "general", "open-source"],
                cost_prompt=0.0009,
                cost_completion=0.0009
            )
        ]

    async def get_available_llms(self) -> List[LLM]:
        """Get available LLMs from OpenRouter API"""
        try:
            response = await self.session.get(
                f"{OPENROUTER_API_URL}/models",
                headers=self.headers
            )
            response.raise_for_status()
            return self.available_llms  # Using our initialized list for simplicity
        except Exception as e:
            print(f"Error fetching LLMs: {e}")
            return self.available_llms  # Fallback to our initialized list

    async def route_request(self, request: Request, budget: float) -> Optional[Dict]:
        """Route a request to the most suitable LLM within budget"""
        suitable_llms = [
            llm for llm in self.available_llms
            if request.required_capability in llm.capabilities
        ]

        if not suitable_llms:
            print(f"No LLMs available with capability: {request.required_capability}")
            return None

        # Estimate token counts (simplified - in reality you'd use a tokenizer)
        prompt_tokens = len(request.prompt.split())  # Approximate
        completion_tokens = min(request.max_tokens, 1000)  # Cap estimation

        # Calculate costs for each suitable LLM
        for llm in suitable_llms:
            cost = (
                (prompt_tokens / 1000 * llm.cost_prompt) +
                (completion_tokens / 1000 * llm.cost_completion)
            )
            if cost <= budget:
                # Found a suitable LLM within budget
                return await self._send_to_llm(llm, request, cost)

        print(f"No LLMs available within budget (${budget:.2f})")
        return None

    async def _send_to_llm(self, llm: LLM, request: Request, estimated_cost: float) -> Dict:
        """Send the request to the selected LLM"""
        print(f"Routing request {request.id} to {llm.name} (estimated cost: ${estimated_cost:.4f})")
        
        payload = {
            "model": llm.id,
            "messages": [{"role": "user", "content": request.prompt}],
            "max_tokens": request.max_tokens
        }

        try:
            response = await self.session.post(
                f"{OPENROUTER_API_URL}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            
            result = response.json()
            actual_usage = result.get("usage", {})
            actual_prompt_tokens = actual_usage.get("prompt_tokens", 0)
            actual_completion_tokens = actual_usage.get("completion_tokens", 0)
            
            actual_cost = (
                (actual_prompt_tokens / 1000 * llm.cost_prompt) +
                (actual_completion_tokens / 1000 * llm.cost_completion)
            )
            
            return {
                "llm": llm.name,
                "response": result["choices"][0]["message"]["content"],
                "cost": actual_cost,
                "prompt_tokens": actual_prompt_tokens,
                "completion_tokens": actual_completion_tokens
            }
        except Exception as e:
            print(f"Error calling LLM {llm.name}: {e}")
            return None

async def main():
    client = OpenRouterClient()
    
    # Example requests with different requirements
    requests = [
        Request(
            id="req1",
            required_capability="coding",
            prompt="Write a Python function to calculate Fibonacci sequence",
            max_tokens=500
        ),
        Request(
            id="req2",
            required_capability="multilingual",
            prompt="Translate this to French: 'Hello, how are you?'",
            max_tokens=100
        ),
        Request(
            id="req3",
            required_capability="safe-content",
            prompt="Explain quantum physics to a 5 year old",
            max_tokens=300
        )
    ]
    
    # Process each request with a $0.10 budget
    for request in requests:
        print(f"\nProcessing request {request.id} ({request.required_capability})...")
        result = await client.route_request(request, budget=0.10)
        
        if result:
            print(f"Response from {result['llm']}:")
            print(result['response'][:200] + "...")  # Print first 200 chars
            print(f"Cost: ${result['cost']:.4f}")
            print(f"Tokens used: {result['prompt_tokens']} prompt, {result['completion_tokens']} completion")
        else:
            print("Failed to route request")

if __name__ == "__main__":
    asyncio.run(main())