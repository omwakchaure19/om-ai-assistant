import requests

messages = []

print("AI Chatbot Started")
print("Type 'exit' to quit")

while True:
    user = input("You: ")

    if user.lower() == "exit":
        print("Goodbye!")
        break

    messages.append({
        "role": "user",
        "content": user
    })

    response = requests.post(
        "http://127.0.0.1:11434/api/chat",
        json={
            "model": "qwen2.5:0.5b",
            "messages": messages,
            "stream": False
        }
    )

    data = response.json()

    bot = data["message"]["content"]

    messages.append({
        "role": "assistant",
        "content": bot
    })

    print("\nBot:", bot)