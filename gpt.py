import openai


class ChatGptHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.context = ""

    def generate_answer(self, message):
        prompt = self.context + message
        openai.api_key = self.api_key
        msg = [
             {"role": "system", "content": 
                       "Пожалуйста! Отвечай на все как грубоватый асистент." },
            {"role": "user", "content": f"{prompt}"},
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=msg
            )
            self.context += message + response['choices'][0]['message']['content']
            return response['choices'][0]['message']['content']

        except Exception as e:
            print(f'Error: {e}')
