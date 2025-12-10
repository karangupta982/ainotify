# """Shared LLM setup for all agents with Gemini-first + Groq fallback."""

# import json
# import os
# from abc import ABC
# from typing import Optional, Type

# import google.generativeai as genai
# from dotenv import load_dotenv
# from groq import Groq
# from pydantic import BaseModel

# load_dotenv()


# class BaseAgent(ABC):
#     """
#     Base class that wires up Gemini (primary) with Groq (fallback).
#     Each agent calls `generate_structured_output` to get a Pydantic-parsed result.
#     """

#     def __init__(self, model: str):
#         # Groq client (fallback)
#         self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
#         self.model = model

#         # Gemini client (primary)
#         # Prefer the latest flash; fall back to the older -001 if needed.
#         # self.gemini_model_candidates = [
#         #     os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest"),
#         #     "gemini-1.5-flash-001",
#         # ]
#         # self.gemini_model_candidates = [
#         #     os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
#         #     "gemini-1.5-pro",
#         # ]

#         self.gemini_model_candidates = [
#             os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),  # safe default
#             "gemini-1.5-pro",  # fallback
#         ]
#         self.gemini_client = None
#         gemini_key = os.getenv("GEMINI_API_KEY")
#         if gemini_key:
#             try:
#                 genai.configure(api_key=gemini_key)
#                 # Just keep the name list; instantiate per call so we can iterate candidates.
#                 self.gemini_client = True  # sentinel meaning gemini is configured
#             except Exception as exc:  # pragma: no cover - defensive
#                 print(f"Failed to configure Gemini: {exc}")
#                 self.gemini_client = None

#     @staticmethod
#     def _strip_json(text: str) -> str:
#         """Remove code fences/backticks and trim whitespace so JSON can be parsed."""
#         cleaned = text.strip()
#         if cleaned.startswith("```"):
#             # Drop leading ```json or ``` and trailing ```
#             cleaned = cleaned.lstrip("`")
#             if cleaned.lower().startswith("json"):
#                 cleaned = cleaned[4:]
#             if cleaned.endswith("```"):
#                 cleaned = cleaned[:-3]
#         return cleaned.strip()

#     def _build_json_prompt(self, instructions: str, user_prompt: str, schema_model: Type[BaseModel]) -> str:
#         """Compose a prompt that forces a strict JSON object for Pydantic parsing."""
#         schema = json.dumps(schema_model.model_json_schema(), indent=2)
#         fields = ", ".join(schema_model.model_fields.keys())
#         return (
#             f"{instructions}\n\n"
#             f"Return a single JSON object with fields: {fields}.\n"
#             f"JSON schema (for reference):\n{schema}\n\n"
#             "Rules:\n"
#             "- Respond with JSON only. No prose, no code fences.\n"
#             "- Include all required fields.\n"
#             "- Keep text concise and on-topic.\n\n"
#             f"User request:\n{user_prompt}\n"
#         )

#     def _try_gemini(
#         self,
#         full_prompt: str,
#         schema_model: Type[BaseModel],
#         temperature: float,
#     ) -> Optional[BaseModel]:
#         if not self.gemini_client:
#             return None

#         for candidate in self.gemini_model_candidates:
#             try:
#                 model = genai.GenerativeModel(candidate)
#                 resp = model.generate_content(
#                     full_prompt,
#                     generation_config={
#                         "temperature": temperature,
#                         "response_mime_type": "application/json",
#                     },
#                 )
#                 text = resp.text or ""
#                 parsed = schema_model.model_validate_json(self._strip_json(text))
#                 return parsed
#             except Exception as exc:
#                 print(f"Gemini generation failed for {candidate}: {exc}")
#                 continue
#         return None

#     def _try_groq(
#         self,
#         instructions: str,
#         user_prompt: str,
#         schema_model: Type[BaseModel],
#         temperature: float,
#     ) -> Optional[BaseModel]:
#         try:
#             resp = self.groq_client.chat.completions.create(
#                 model=self.model,
#                 temperature=temperature,
#                 messages=[
#                     {"role": "system", "content": instructions},
#                     {
#                         "role": "user",
#                         "content": (
#                             f"{user_prompt}\n\n"
#                             "Respond with JSON only (no code fences)."
#                         ),
#                     },
#                 ],
#             )
#             content = resp.choices[0].message.content
#             parsed = schema_model.model_validate_json(self._strip_json(content))
#             return parsed
#         except Exception as exc:
#             print(f"Groq generation failed: {exc}")
#             return None

#     def generate_structured_output(
#         self,
#         instructions: str,
#         user_prompt: str,
#         schema_model: Type[BaseModel],
#         temperature: float = 0.7,
#     ) -> Optional[BaseModel]:
#         """
#         Try Gemini first; if it fails, fall back to Groq.
#         Returns a Pydantic model instance or None if both fail.
#         """
#         full_prompt = self._build_json_prompt(instructions, user_prompt, schema_model)

#         # Primary: Gemini
#         result = self._try_gemini(full_prompt, schema_model, temperature)
#         if result:
#             return result

#         # Fallback: Groq
#         return self._try_groq(instructions, user_prompt, schema_model, temperature)








"""Shared LLM setup for all agents with Groq-only JSON structured output."""

import json
import os
from abc import ABC
from typing import Optional, Type

from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv()


class BaseAgent(ABC):
    """
    Base class that now uses ONLY Groq for structured JSON output.
    """

    def __init__(self, model: str):
        self.model = model

        # -------------------------------
        # Groq Client
        # -------------------------------
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # ----------------------------------------------------
    # Helpers
    # ----------------------------------------------------
    @staticmethod
    def _strip_json(text: str) -> str:
        """Remove accidental code fences and leading/trailing whitespace."""
        if not text:
            return text

        cleaned = text.strip()

        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:].strip()

        return cleaned.strip()

    def _build_json_prompt(self, instructions: str, user_prompt: str, schema_model: Type[BaseModel]) -> str:
        """Compose a prompt that forces strict JSON output."""
        schema = json.dumps(schema_model.model_json_schema(), indent=2)
        fields = ", ".join(schema_model.model_fields.keys())

        return (
            f"{instructions}\n\n"
            f"Return a SINGLE JSON object with the following fields: {fields}.\n\n"
            f"JSON schema:\n{schema}\n\n"
            "REQUIREMENTS:\n"
            "- Respond with JSON only (NO code fences, NO explanations).\n"
            "- Use EXACT field names.\n"
            "- Include all required fields.\n\n"
            f"User request:\n{user_prompt}\n"
        )

    # ----------------------------------------------------
    # Groq Invocation (only engine)
    # ----------------------------------------------------
    def _try_groq(
        self,
        instructions: str,
        user_prompt: str,
        schema_model: Type[BaseModel],
        temperature: float,
    ) -> Optional[BaseModel]:

        schema = json.dumps(schema_model.model_json_schema(), indent=2)

        groq_user_prompt = (
            f"{user_prompt}\n\n"
            "You MUST output ONLY valid JSON.\n"
            "The JSON MUST match EXACTLY the schema below.\n"
            "Do not add fields or rename fields.\n"
            "Do NOT output text outside the JSON.\n\n"
            f"JSON schema:\n{schema}\n"
        )

        try:
            resp = self.groq_client.chat.completions.create(
                model=self.model,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": groq_user_prompt},
                ],
            )

            content = resp.choices[0].message.content
            cleaned = self._strip_json(content)

            return schema_model.model_validate_json(cleaned)

        except Exception as exc:
            print(f"Groq generation failed: {exc}")
            return None

    # ----------------------------------------------------
    # Public API
    # ----------------------------------------------------
    def generate_structured_output(
        self,
        instructions: str,
        user_prompt: str,
        schema_model: Type[BaseModel],
        temperature: float = 0.7,
    ) -> Optional[BaseModel]:

        full_prompt = self._build_json_prompt(instructions, user_prompt, schema_model)

        # Groq is now the only engine
        return self._try_groq(instructions, user_prompt, schema_model, temperature)
