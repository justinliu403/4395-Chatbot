from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import pickle
import yaml
import os.path


if __name__ == '__main__':
    nflKnowledge = pickle.load(open('knowledgeBase.pickle', 'rb'))
    with open(r'.\knowledgeBase.yml', 'w') as file:
        documents = yaml.dump(nflKnowledge, file)
    if os.path.exists("./userBase.p"):
        user_knowledge = pickle.load(open('userBase.p', 'rb'))
    else:
        user_knowledge = {}



    chatbot = ChatBot(name ="NFL Bot")
    corpus_trainer = ChatterBotCorpusTrainer(chatbot)
    #corpus_trainer.train('chatterbot.corpus.english')
    corpus_trainer.train("./knowledgeBase.yml")
    trainer = ListTrainer(chatbot)
    wants_to_talk = True
    print("Hi my name is NFL Bot! If at any time you want to stop, just enter * \nWhat is your name?")
    user_in = input()
    if user_in in user_knowledge:
        print("Welcome back,", user_in)
    else:
        print("Nice to meet you,", user_in)
        user_knowledge[user_in] = []


    while wants_to_talk:
        user_in = input()
        if user_in == "*":
            wants_to_talk = False
        else:
            response = chatbot.get_response(user_in)
            print(response)

    pickle.dump(user_knowledge, open("./userBase.p", "wb"))


