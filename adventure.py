import json
import random
import re
from collections import Counter

# Name: Gouranga Khande
# Project: Lost in the Woods game - Text adventure
# Course: CS-515 - Fundamentals of Computing
# Professor: Micheal Greenberg

f=open('map.json')
data=json.load(f)

check=False
while not check:
    player_name=input("Enter player name: ")
    check=re.match("^[a-zA-Z\s]+$", player_name)
    if not check:
        print("Please Enter valid name containing only alphabets and spaces: ")
        
print("\n")
letters=set([y.strip() for y in list(player_name.lower().strip(' ')) if y.strip()])

print(f"\n******************************************************\n\nWelcome to Lost in the Woods game {player_name}!!\n\n******************************************************\n\nYou are about to start the Game!!\n")
print("\nThis game consists of 2 main tasks: \n1. Collect all items which are starting with the letter which is in your name\n2. After completing the task - 1 successfully, Complete the maths quiz to win the game\n")
print("\nInstructions to follow:\n1. You need to collect the exact number of items (starting with letter which is in your name) as the number of unique letters in your name\n2. Please type 'help' to know what commands can be given\n")

inv=[]
quit_checker=False
abbrevations_direction={'n':'north','s':'south','e':'east','w':'west'}
abbrevations_verbs={'g':'go','ge':'get','inv':'inventory','d':'drop','he':'help','l':'look','ch':'checklist'}
status=0
score=0
room_items=[]
room_exits=[]


player_name=set(player_name.lower().strip())

for x in range(len(data)):
    room_items.append(data[x]['items'])
    room_exits.append(list(data[x]["exits"].keys()))
    
def room_info():
    #print(data[status]["desc"])
    if not room_items[status]:
        print("\nSorry! no items present in this room\n")
    else:
        print("\nThis room has the following items: \n")
        for i,x in enumerate(room_items[status]):
            k=i+1
            print(f"{k}. {x}")
    print("\n")
    print("Exits for this room are:")
    for i,x in enumerate(room_exits[status]):
        k=i+1
        print(f"{k}. {x}")
    print("\n")


def get(x):
    if(x not in room_items[status]):
        print("Item is not present in the room")
    else:
        inv.append(x)
        room_items[status].remove(x)
        print(f"You pick up the {x}!")

def drop(x):
    if(x not in inv):
        print("You do not carry the item")
    else:
        inv.remove(x)
        room_items[status].append(x)
        print(f"You drop the {x}")
    
def look():
    print("\n")
    print(data[status]['desc'])
    room_info()
    
def inventory():
    print("You have the following items:\n")
    for i,x in enumerate(inv):
        k=i+1
        print(f"{k}. {x}")
    print("\n")
        
        
def help():
    print("\nYou can execute the following commands\n1. go\n2. get\n3. look\n4. inventory\n5. drop\n6. checklist\n")
    

def go(x):
    global status
    if x in list(data[status]["exits"].keys()):
        status=data[status]["exits"][x]
        print(f"You go {x}!")
        print(data[status]['desc'])
        room_info()
    else:
        print("There is no exit!! Please choose other direction")
        
def execute(x):
    x_token=x.lower().strip().split()
    if(x_token[0] in list(abbrevations_verbs.keys())):
        x_verb=abbrevations_verbs[x_token[0]]
    else:
        x_verb=x_token[0]
    if(len(x_token)>1):
        if(x_token[1] in list(abbrevations_direction.keys())):
            x_dir=abbrevations_direction[x_token[1]]
        else:
            x_dir=x_token[1]
    if(x_verb=="go"):
        if(len(x_token)==1):
            print("You need to go somewhere!!")
        elif(len(x_token)>2):
            print("Please follow instructions and type only one exit after 'go' keyword!")
        else:
            go(x_dir)
    elif(x_verb=="look"):
        look()
    elif(x_verb=="inventory"):
        inventory()
    elif(x_verb=="get"):
        if(len(x_token)==1):
            print("You need to pick up something!!\nPlease type 'look' to see what items are present in the room to pick up")
        elif(len(x_token)>2):
            print("Please follow instructions and type only one item after 'get' keyword!")
        else:
            get(x_dir)
    elif(x_verb=="drop"):
        if(len(x_token)==1):
            print("You need to drop something!!")
        elif(len(x_token)>2):
            print("Please follow instructions and type only one item which needs to be dropped after 'drop' keyword!")
        else:
            drop(x_dir)
    elif(x_verb=="help"):
        help()
    elif(x_verb=="checklist"):
        checklist()
    else:
        print("unknown command entered!!\nPlease type help and get info :)\n")
        
               
def checklist():
    inv_list=list(map(lambda x:x[0], inv))
    inv_dict = {k: v for k, v in zip(inv_list, inv)}
    if(letters.issubset(set(inv_list)) and len(inv_list)>len(letters)):
        print("Drop the following items to win the game: ")
        k=1
        for x in inv_list:
            if x not in letters:
                item=inv_dict[x]
                print(f"{k}. {item}")
                k+=1
        print("\n")
    elif(len(inv_list)!=0):
        print("Please collect the items starting with the given alphabet below: ")
        k=1
        for x in letters:
            if x not in inv_list:
                print(f"{k}. {x}")
                k+=1
        print("\n")
    else:
        print("You did not collect any items!!\n")
    
    
    
def checker():
    inv_list=list(map(lambda x:x[0], inv))
    return Counter(list(letters)) == Counter(list(inv_list))
    

       
def math_quiz():
    global score
    global quit_checker
    count=0
    print("You are about to start Maths Quiz...\nFor every question please choose the arithmetical operation you need to perform: \n1. Addition\n2. Subtraction\n3. Multiplication\n")
    while (count<3 and quit_checker==False):
        k=count+1
        print(f"\nQuestion number {k}")
        math_quiz_questions()
        count+=1
    print(f"Your final score is: {score}/3!!\n")
    if(score>=2 and quit_checker==False):
        print("\n********************************\nYou won the game!!\n********************************\n")
    elif((score<2 and quit_checker==False)):
        print("\n********************************\nYou lost the game!!\n********************************\n")
        try:
            again=input("To win this You must pass the test!! Please type 'Yes' to try again or 'Quit' to exit the game: ")
        except KeyboardInterrupt:
            print("\nPlease type 'quit' to exit, 'continue' to resume the game: \n")
            x=input("What do you want to do: ")
            if(x.lower().strip()=='quit'):
                print("\nThank you for playing the game!!")
            else:
                print("Unknown command entered. quiz resumes automatically...\n")
                math_quiz()
        except EOFError:
            print("\nThank you for playing the game!!")
        else:
            if(again.lower().strip()=="yes"):
                math_quiz()
            elif(again.lower().strip()=="quit"):
                print("Goodbye!! See you later\n")
            else:
                print("Unknown command entered...Quiz starts automatically\n")
    elif(quit_checker):
        print("\nSee you again!!\n")
        
        

def math_quiz_questions():
    global score
    global quit_checker
    try:
        command=input("Your option: ")
    except KeyboardInterrupt:
        print("\nPlease type 'quit' to exit, 'continue' to resume the game: \n")
        x=input("What do you want to do: ")
        if(x.lower().strip()=='quit'):
            print("\nThank you for playing the game!!")
            quit_checker=True
        else:
            print("Unknown command entered. quiz resumes automatically...\n")
            math_quiz_questions()
    except EOFError:
        print("\nThank you for playing the game!!")
        quit_checker=True
    
    else:  
        if(command.lower().strip()=="quit"):
            print("Goodbye!!\nEnd of Math Quiz\n")
            quit_checker=True
        
        elif(command not in ["1","2","3"]):
            print("Choose the correct option!!\n")
            math_quiz_questions()
        else: 
            x=random.randint(1,20)
            y=random.randint(1,20)
            if(command=="1"):
                ans=int(input(f"Please calculate and type your answer\n{x} + {y} = "))
                if(ans==(x+y)):
                    print("Correct!!")
                    score+=1
                else:
                    print("Sorry it's incorrect")
            elif(command=="2"):
                ans=int(input(f"Please calculate and type your answer\n{x} - {y} = "))
                if(ans==(x-y)):
                    print("Correct!!")
                    score+=1
                else:
                    print("Sorry it's incorrect")
            elif(command=="3"):
                ans=int(input(f"Please calculate and type your answer\n{x} * {y} = "))
                if(ans==(x*y)):
                    print("Correct!!")
                    score+=1
                else:
                    print("Sorry it's incorrect")

        
  
            
def start():
    global status
    command = ""
    while True:
        if checker():
            print("\n*******************************************************************************************************************************\n\nCongratulations!! You have collected all required items. Please take the math quiz and score atleast 2 points to win the game...\n\n*******************************************************************************************************************************\n")
            #print("Please take the Math quiz\n")
            math_quiz()
            break
        if status==0:
            print(data[status]["desc"])
        try:
            command=input("* What do you want to do: ")
        except KeyboardInterrupt:
            print("\nPlease type 'quit' to exit, 'continue' to resume the game: \n")
            x=input("What do you want to do: ")
            if(x.lower()=='quit'):
                print("\nThank you for playing the game!!")
                break
            else:
                continue
        except EOFError:
            print("\nThank you for playing the game!!")
            break
        if command.lower().strip()=="quit":
            print("\nGoodbye, you are missing a great game!!")
            break
        else:
            execute(command)


                
start()


