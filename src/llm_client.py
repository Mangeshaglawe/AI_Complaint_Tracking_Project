import os
import json

import openai


class LLMClient:
    def __init__(self, model: str | None = None):
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY environment variable not set")
        openai.api_key = key
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    def _call(self, messages, temperature: float = 0.0) -> str:
        resp = openai.ChatCompletion.create(model=self.model, messages=messages, temperature=temperature)
        return resp["choices"][0]["message"]["content"]

    def extract_structured(self, text: str) -> dict:
        from .prompts import extraction_prompt

        messages = [
            {"role": "system", "content": "You extract structured JSON from complaint text."},
            {"role": "user", "content": extraction_prompt.format(text=text)},
        ]
        content = self._call(messages, temperature=0.0)

        # find JSON object in response
        import re

        m = re.search(r"(\{.*\})", content, re.S)
        json_text = m.group(1) if m else content
        return json.loads(json_text)

    def generate_email(self, structured: dict) -> str:
        from .prompts import email_prompt

        messages = [
            {"role": "system", "content": "Write professional customer response emails."},
            {"role": "user", "content": email_prompt.format(**structured)},
        ]
        return self._call(messages, temperature=0.2)

    def generate_summary(self, structured: dict) -> str:
        from .prompts import summary_prompt

        messages = [
            {"role": "system", "content": "Write concise internal case summaries."},
            {"role": "user", "content": summary_prompt.format(**structured)},
        ]
        return self._call(messages, temperature=0.2)
