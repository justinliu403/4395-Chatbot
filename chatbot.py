from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer


if __name__ == '__main__':
    chatbot = ChatBot(name ="NFL Bot")
    corpus_trainer = ChatterBotCorpusTrainer(chatbot)
    corpus_trainer.train('chatterbot.corpus.english')
    trainer = ListTrainer(chatbot)
    wants_to_talk = True
    print("Hi my name is NFL Bot! If at any time you want to stop, just enter * \nWhat is your name?")
    user_in = input()
    print("Hello,", user_in)



    while wants_to_talk:
        user_in = input()
        if user_in == "*":
            wants_to_talk = False
        else:
            response = chatbot.get_response(user_in)
            print(response)


