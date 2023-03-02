from base.scripts.ChatBot.chat_botANN import Chatbot


def function(request):
    print("HELLO")
    if request.method == 'POST':
        chaty = Chatbot()
        chat = (Chatbot.Talking(chaty,"podemos intercambiar mi auto mas nuevo que hay?"))
        tree = "Green"
        return  tree