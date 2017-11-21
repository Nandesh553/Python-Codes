from termcolor import colored
from spy_details import Spy,spy, ChatMessage, friends
from steganography.steganography import Steganography
from datetime import datetime

STATUS_MESSAGES = ['New user', 'Available.', 'Busy']


print "**WELCOME TO SPY CHAT!**"


#method to add status in spy chat
def add_status():

    spy.updated_status_message = None
    spy.current_status_message=None

    if spy.current_status_message != None:

        print "Your current status message is %s \n" % (spy.current_status_message)
    else:
        print "You don't have any status message currently \n"

    default = raw_input("Do you want to select from the older status (y/n)? ")

    if default.upper() == "N":
        new_status_message = raw_input("What status message do you want to set? ")


        if len(new_status_message) > 0:
            STATUS_MESSAGES.append(new_status_message)
            updated_status_message = new_status_message

    elif default.upper() == 'Y':

        item_position = 1

        for message in STATUS_MESSAGES:
            print '%d. %s' % (item_position, message)
            item_position = item_position + 1

        message_selection = int(raw_input("\nChoose from the above messages "))


        if len(STATUS_MESSAGES) >= message_selection:
            updated_status_message = STATUS_MESSAGES[message_selection - 1]

    else:
        print "The option you chose is not valid! Press either y or n."

    if updated_status_message:
        print "Your updated status message is: %s" % (updated_status_message)
    else:
        print "You current don't have a status update"

    return updated_status_message

# to add a new friend
def add_friend():

    new_friend = Spy('','',0,0.0)

    new_friend.name = raw_input("Please add your friend's name: ")
    new_friend.salutation = raw_input("Are they Mr. or Ms.?: ")

    new_friend.name = new_friend.salutation + " " + new_friend.name

    new_friend.age = raw_input("Age?")
    new_friend.age = int(new_friend.age)

    new_friend.rating = raw_input("Spy rating?")
    new_friend.rating = float(new_friend.rating)

    if len(new_friend.name) > 0 and new_friend.age > 12 and new_friend.rating >= spy.rating:
        friends.append(new_friend)
        print "**Friend Added!**"
    else:
        print "SORRY! Invalid entry. We can't add spy with the details you provided"
        invalid_friend=1

    return len(friends)

#to select a friend from list of friends
def select_a_friend():
    item_number = 0

    for friend in friends:
        print '%d. %s %s aged %d with rating %.2f is online' % (item_number +1, friend.salutation, friend.name,
                                                   friend.age,
                                                   friend.rating)
        item_number = item_number + 1

    friend_choice = raw_input("Choose from your friends")

    friend_choice_position = int(friend_choice) - 1

    return friend_choice_position


def send_message():
        if len(friends)==0: #check if friends are there in friends list
            add_friend()
            send_message()
        else:
            friend_choice=select_a_friend()
            original_image = raw_input("What is the name of the image?")
            output_path = "output.jpg"
            text = raw_input("Write your message ")
            if len(text)>0:
                Steganography.encode(original_image, output_path, text)

                new_chat = ChatMessage(text,True)

                friends[friend_choice].chats.append(new_chat)

                print "Your secret message image is ready!"
            elif len(text) > 100:
                print "you are speaking too much message wont be sent\n"

            else:
                print "please ENTER A MESSAGE"


# method to read a message from list
def read_message():
    if len(friends) == 0: #check if there are friends
        print "No friends and messages!"

    else:
        sender = select_a_friend()

        output_path = raw_input("What is the name of the file?")

        secret_text = Steganography.decode(output_path)

        new_chat = ChatMessage(secret_text,False)

        friends[sender].chats.append(new_chat)

        print "Your secret message has been saved!"

#method to read chats from chats in friends
def read_chat_history():
    if len(friends) == 0: #check if there are existing friends or not
        print "No friends and messages!"

    else:
        read_for = select_a_friend()

        print '\n'

        for chat in friends[read_for].chats:
             if chat.sent_by_me:
                print colored ("[%s]" , "blue") %(chat.time.strftime("%d,%B,%Y")), colored("you said ", "red")
                print chat.message
             else:
                print '(%s) [%s] %s said: %s' % (chat.time.strftime("%d %B %Y"), friends[read_for].name, chat.message)


#def del_a_friend():
    #for friend in friends:
        #item=0
        #for chat in friends[item].chats:
            #if len(chat)>=10:
                #friend[item]=None
                #print "friend at item deleted"
        #item=item+1


# method to start spychat
def start_chat(spy):

    spy.name = spy.salutation + " " + spy.name


    if spy.age > 12 and spy.age < 50: #check age of spy


        print "Authentication complete. Welcome " + spy.name + " age: " \
              + str(spy.age) + " and rating of: " + str(spy.rating) + " Proud to have you onboard"

        show_menu = True

        while show_menu:
            menu_choices = "choose your option \n 1. To Update status \n 2. TO add a friend \n 3. Send a secret message \n 4. Read a secret message \n 5. Read Chats from a user \n 6. Close Application \n"
            menu_choice = raw_input(menu_choices)

            if len(menu_choice) > 0:
                menu_choice = int(menu_choice)
               # choose from menu
                if menu_choice == 1:
                    spy.current_status_message = add_status()
                elif menu_choice == 2:
                    number_of_friends = add_friend()
                    print 'You have %d friends' % (number_of_friends)
                elif menu_choice == 3:
                    send_message()
                elif menu_choice == 4:
                    read_message()
                elif menu_choice == 5:
                    read_chat_history()
                else:
                    show_menu = False
    else:
        print "Sorry you are NOT of the CORRECT AGE to be a spy"

start_chat(spy)
#caling method spy _chat
