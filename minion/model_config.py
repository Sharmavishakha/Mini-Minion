"""Custom model configuration with retry logic for rate limits."""

import time
import asyncio
from google.adk.models.google_llm import Gemini


class RateLimitedGemini(Gemini):
    """Gemini model with automatic backoff on rate limits."""
    
    async def generate_content_async(self, *args, **kwargs):
        max_retries = 5
        base_delay = 15  # Wait 15s between retries (free tier resets every minute)
        
        for attempt in range(max_retries):
            try:
                async for response in super().generate_content_async(*args, **kwargs):
                    yield response
                return
            except Exception as e:
                if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                    if attempt < max_retries - 1:
                        wait = base_delay * (attempt + 1)
                        print(f"⏳ Rate limit hit. Waiting {wait}s before retry {attempt + 1}/{max_retries}...")
                        await asyncio.sleep(wait)
                        continue
                raise