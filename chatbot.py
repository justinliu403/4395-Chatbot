from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import pickle
import spacy
import yaml
import os.path
import random


if __name__ == '__main__':
    nflKnowledge = pickle.load(open('nflTeamKnowledge.p', 'rb'))
    for key in nflKnowledge:
        print(key, nflKnowledge[key])
    with open(r'.\knowledgeBase.yml', 'w') as file:
        documents = yaml.dump(nflKnowledge, file)
    if os.path.exists("./userBase.p"):
        user_knowledge = pickle.load(open('userBase.p', 'rb'))
    else:
        user_knowledge = {}
    print(user_knowledge)

    chatbot = ChatBot("NFL Bot", logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch'
    ])
    corpus_trainer = ChatterBotCorpusTrainer(chatbot)
    print("Loading spacy, this might take a second...")
    spacy_instance = spacy.load('en_core_web_md')
    corpus_trainer.train('chatterbot.corpus.english')
    corpus_trainer.train("./knowledgeBase.yml")
    trainer = ListTrainer(chatbot)

    wants_to_talk = True
    print("Hi my name is NFL Bot! If at any time you want to stop, just enter * \nWhat is your name?")
    user_in = input()
    if user_in in user_knowledge:
        print("Welcome back,", user_in)
        print("How about them", user_knowledge[user_in].get("favorite team"))
    else:
        print("Nice to meet you,", user_in)
        name = user_in
        user_knowledge[name] = {}
        user_in = input("Who's your favorite NFL team?")
        user_knowledge[name] = {"favorite team": user_in}
    print("I know tons of information about the nfl, ask me about your favorite team! If referencing a team, please capitalize"
          " their name because I use NER to recognize if a team is referenced and capitalizing helps")


    while wants_to_talk:
        user_in = input()
        if user_in == "*":
            wants_to_talk = False
        else:
            chatter_response_needed = True
            doc = spacy_instance(user_in)
            orgs = []
            for ent in doc.ents:
                if ent.label_ == "ORG":
                    orgs.append(ent.text)
            for org in orgs:
                if org in nflKnowledge:
                    chatter_response_needed = False
                    if "where" in user_in.lower():
                        print("The", org, "are based in", nflKnowledge[org][0])
                    elif "fact" in user_in.lower() or "know" in user_in.lower():
                        print("Here's a fun fact about the", org, ":", nflKnowledge[org][random.randint(1, 2)])
                    else:
                        print("Sorry, I don't know what you're trying to ask about the", org)

            if chatter_response_needed:
                response = chatbot.get_response(user_in)
                print(response)

    pickle.dump(user_knowledge, open("./userBase.p", "wb"))


