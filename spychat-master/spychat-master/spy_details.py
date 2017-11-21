from datetime import datetime

class Spy:

    def __init__(self, name, salutation, age, rating):
        self.name = name
        self.salutation = salutation
        self.age = age
        self.rating = rating
        self.is_online = True
        self.chats = []
        self.current_status_message = None


class ChatMessage:

    def __init__(self,message,sent_by_me):
        self.message = message
        self.time = datetime.now()
        self.sent_by_me = sent_by_me



spy = Spy

spy.name = raw_input("Welcome to spy chat, you must tell me your spy name first: ")

if len(spy.name) > 0:
    spy.salutation = raw_input("Should I call you Mr. or Ms.?: ")

    spy.age = raw_input("What is your age?")
    spy.age = int(spy.age)

    spy.rating = raw_input("What is your spy rating?")
    spy.rating = float(spy.rating)


else:

    print 'Please add a valid spy name'

friends = []