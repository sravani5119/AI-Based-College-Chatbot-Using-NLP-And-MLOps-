from pipeline.chatbot_engine import ChatbotEngine

bot = ChatbotEngine()

print("Chatbot started. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    result = bot.get_response(user_input)

    print("Intent:", result["intent"])
    print("Entities:", result["entities"])
    print("Confidence:", result["confidence"])
    print("Bot:", result["response"])
    print()
