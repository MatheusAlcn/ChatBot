import google.generativeai as chat # type: ignore
import os

# Substitua pela sua chave da API
GOOGLE_GEMINI_API__KEY = "GOOGLE_GEMINI_API__KEY "
chat.configure(api_key=GOOGLE_GEMINI_API__KEY)

# Inicializa o modelo do Google Gemini uma única vez
chat_instance = chat.GenerativeModel("gemini-1.5-pro-latest").start_chat(history=[])

# Dicionário com informações básicas sobre algumas plantas.
plantas_info = {
    "tomate cereja": (
        "Tomates cereja são plantas de crescimento rápido que precisam de muita luz solar. "
        "Eles devem ser plantados em solo bem drenado e regados regularmente, mas evite encharcar. "
        "Fertilize a cada duas semanas durante a estação de crescimento."
    ),
    "morango": (
        "Morangos são plantas perenes que preferem solo rico e bem drenado. "
        "Devem receber luz direta por pelo menos 6 horas por dia. Regue regularmente, mas evite deixar o solo muito encharcado."
    ),
    "espinafre da nova zelândia": (
        "O espinafre da Nova Zelândia é uma planta que cresce melhor em clima fresco e é resistente ao calor. "
        "Prefere solo bem drenado e precisa de bastante luz solar. Regue regularmente e colha as folhas quando estiverem grandes."
    )
}

# Personalização do comportamento do assistente.
personalizacao = """
Você é um assistente inteligente e amigável. Responda de forma clara e concisa sobre cuidados com plantas.
"""

# Inicializa a lista de mensagens com a personalização do assistente.
lista_mensagens = [{"role": "system", "content": personalizacao}]
MAX_MENSAGENS = 10  # Define o número máximo de mensagens a serem mantidas na lista

# Inicia o loop de interação com o usuário.
while True:
    texto = input("Escreva aqui sua mensagem (ou 'sair' para encerrar): ")
    
    if texto.lower() == "sair":
        print("Fim da conversa.")
        break
    else:
        # Respostas pré-definidas para plantas
        if "tomate cereja" in texto.lower():
            resposta = plantas_info["tomate cereja"]
        elif "morango" in texto.lower():
            resposta = plantas_info["morango"]
        elif "espinafre da nova zelândia" in texto.lower():
            resposta = plantas_info["espinafre da nova zelândia"]
        else:
            try:
                # Usar o modelo do Google Gemini para outras perguntas
                response = chat_instance.send_message(texto)
                resposta = response.text if response else "Desculpe, não foi possível obter uma resposta."
            except Exception as e:
                print(f"Erro ao enviar mensagem para o modelo: {e}")
                resposta = "Desculpe, houve um erro ao tentar obter uma resposta."

        # Exibe a resposta do chatbot ou a informação específica sobre plantas.
        print(f"ChatBot: {resposta}")

        # Adiciona a resposta à lista de mensagens.
        lista_mensagens.append({"role": "assistant", "content": resposta})

        # Limitar o número de mensagens
        if len(lista_mensagens) > MAX_MENSAGENS:
            lista_mensagens = lista_mensagens[-MAX_MENSAGENS:]

# Coleta feedback do usuário ao encerrar a conversa
feedback = input("Você achou essa conversa útil? (sim/não): ")
if feedback.lower() == "sim":
    print("Ótimo! Fico feliz em ajudar.")
else:
    print("Sinto muito. Vou tentar melhorar!")