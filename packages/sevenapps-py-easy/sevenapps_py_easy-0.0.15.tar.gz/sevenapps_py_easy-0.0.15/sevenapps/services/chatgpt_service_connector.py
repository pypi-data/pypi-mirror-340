import requests

class ChatGPTConnector:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = 'https://api.openai.com/v1/chat/completions'  # URL correcta para modelos de chat
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
        }

    # Método para generar texto con ChatGPT usando un prompt
    def generate_text(self, prompt: str, model: str = 'gpt-3.5-turbo', max_tokens: int = 150) -> str:
        try:
            payload = {
                'model': model,
                'messages': [{'role': 'user', 'content': prompt}],  # Convertir el prompt en un mensaje de usuario
                'max_tokens': max_tokens,
                'temperature': 0.7,  # Puedes ajustar la temperatura para creatividad
            }
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            generated_text = response.json()['choices'][0]['message']['content'].strip()
            return generated_text
        except requests.exceptions.RequestException as e:
            print(f'Error generating text: {e}')
            raise Exception('Failed to generate text from ChatGPT')

    # Método para obtener información sobre los modelos disponibles
    def get_models(self) -> dict:
        try:
            response = requests.get('https://api.openai.com/v1/models', headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Error fetching models: {e}')
            raise Exception('Failed to fetch models')

    # Método para obtener el estado de la API
    def get_api_status(self) -> dict:
        try:
            response = requests.get('https://api.openai.com/v1/health', headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Error fetching API status: {e}')
            raise Exception('Failed to fetch API status')

    # Método para crear una conversación con instrucciones previas
    def create_chat(self, messages: list[dict], model: str = 'gpt-4') -> str:
        try:
            payload = {
                'model': model,
                'messages': messages,
                'max_tokens': 500,  # número de tokens máximos por respuesta
                'temperature': 0.7,  # puedes ajustar la temperatura para controlar la creatividad
            }
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            generated_text = response.json()['choices'][0]['message']['content'].strip()
            return generated_text
        except requests.exceptions.RequestException as e:
            print(f'Error generating text: {e}')
            raise Exception('Failed to generate text from ChatGPT')
