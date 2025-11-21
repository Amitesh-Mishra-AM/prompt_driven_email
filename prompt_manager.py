import json
import os
class PromptManager:
    def __init__(self, filepath="prompts.json"):
        self.filepath=filepath
        self.default_prompts = {
            "categorization_prompt": "Categorize the following email into one of these categories: Important, Newsletter, Spam, To-Do. To-Do emails must include a direct request requiring user action. Return only the category name.",
            "action_extraction_prompt": "Analyze the email content. Extract any actionable tasks and their deadlines. Return the output strictly in JSON format: {\"task\": \"task description\", \"deadline\": \"date/time or None\"}. If there are no tasks, return {\"task\": null, \"deadline\": null}.",
            "auto_reply_prompt": "You are a helpful email assistant. If the email is a meeting request, draft a polite reply asking for an agenda. If it is a task, confirm receipt. Keep the tone professional and concise."
        }
        self.prompts=self._load_prompts()

    def _load_prompts(self):
            if not os.path.exists(self.filepath):
                self._save_to_file(self.default_prompts)
                return self.default_prompts
            
            try:
                with open(self.filepath, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self.default_prompts

    def _save_to_file(self, data):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=4)

    def get_prompt(self, key):
        return self.prompts.get(key, self.default_prompts.get(key, ""))

    def update_prompt(self, key, new_text):
        if key in self.prompts:
            self.prompts[key] = new_text
            self._save_to_file(self.prompts)

    def reset_defaults(self):
        self.prompts = self.default_prompts
        self._save_to_file(self.prompts)
        return self.prompts
