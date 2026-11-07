import ollama


class OllamaChatClient:
    def __init__(self, model_name="llama3.2"):
        self.model_name = model_name

    def send(self, prompt):
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt.strip()}]
            )
            message = (
                response.get("message", {})
                if isinstance(response, dict)
                else getattr(response, "message", None)
            )
            content = (
                message.get("content")
                if isinstance(message, dict)
                else getattr(message, "content", None)
            )
            if not isinstance(content, str) or not content.strip():
                raise RuntimeError("AI returned an empty response.")
            return content.strip()
        except RuntimeError:
            raise
        except Exception as e:
            raise RuntimeError(
                f"Ollama service unavailable or failed: {e}"
            ) from e
