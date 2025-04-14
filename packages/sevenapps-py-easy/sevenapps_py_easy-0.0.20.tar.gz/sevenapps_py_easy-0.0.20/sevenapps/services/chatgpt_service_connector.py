
from openai import OpenAI

class ChatGPTConnector:
    def __init__(self, api_key: str):
        # Inicializa el cliente con la clave de la API
        self.client = OpenAI(api_key=api_key)

    # Metodo para generar texto con ChatGPT usando un prompt
    def generate_text(self, prompt: str, model: str = 'gpt-4', max_tokens: int = 150) -> str:
        try:
            # Usamos el nuevo metodo para generar texto
            response = self.client.responses.create(
                model=model,
                input=prompt
            )
            # Accedemos al contenido de la respuesta
            return response.output_text.strip()
        except Exception as e:
            print(f'Error generating text: {e}')
            raise Exception('Failed to generate text from ChatGPT')

    # Metodo para obtener información sobre los modelos disponibles
    def get_models(self) -> dict:
        try:
            # Lista los modelos disponibles
            response = self.client.responses.create(
                model='gpt-4',  # Puedes hacer una llamada a un modelo para obtener información
                input="List the available models."
            )
            return response.output_text
        except Exception as e:
            print(f'Error fetching models: {e}')
            raise Exception('Failed to fetch models')

    # Metodo para obtener el estado de la API
    def get_api_status(self) -> dict:
        try:
            # Verifica el estado de la API (puedes hacer una llamada simple)
            response = self.client.responses.create(
                model='gpt-4',
                input="Check the status of the API."
            )
            return {'status': 'ok'} if response else {'status': 'error'}
        except Exception as e:
            print(f'Error fetching API status: {e}')
            raise Exception('Failed to fetch API status')

    # Metodo para crear una conversación con instrucciones previas
    def create_chat(self, messages: list, model: str = 'gpt-4o') -> str:
        try:
            # Crear una conversación con un historial de mensajes
            response = self.client.responses.create(
                model=model,
                input=messages
            )
            return response.output_text.strip()
        except Exception as e:
            print(f'Error generating chat: {e}')
            raise Exception('Failed to generate chat from ChatGPT')
