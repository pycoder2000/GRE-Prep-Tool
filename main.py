import requests
import random
import json
import sys
import os
import platform
from bs4 import BeautifulSoup

#! IMP : Change these addresses to your directory location
GREWordList = "/Users/parthdesai/lib/GRE-Prep-Tool/GREWordList.json"
VocabularyList = "/Users/parthdesai/lib/GRE-Prep-Tool/vocabulary.json"
TestedWordsList = "/Users/parthdesai/lib/GRE-Prep-Tool/TestedWords.json"

def ClearOutput():
    MyOS = platform.system()

    if MyOS == "Windows":
        os.system("cls")
    elif MyOS == "Darwin":
        os.system("clear")
    elif MyOS == "Linux":
        os.system("clear")
    else:
        print("\nUnknown OS ☠️ Please check ClearOutput() function in Main.py")

def Heading(heading):
    print("\n-----------------------------------")
    print("\n        {}".format(heading))
    print("\n-----------------------------------")
    print("\nPress Enter to continue or Q to quit at any time")

try:
    f = open(GREWordList, 'r')
    GlobalDictionary = json.load(f)
    f.close()
except:
    print("\nUnable to find GREWordList.json file. Please check the address again")
    GlobalDictionary = {}

try:
    f = open(VocabularyList, 'r')
    VocabDictionary = json.load(f)
    f.close()
except:
    print("\nUnable to find vocabulary.json file. Please check the address again")
    VocabDictionary = {}

def DisplayAllLists():
    ClearOutput()
    Heading("GRE Word Lists")
    print()
    for ListName in GlobalDictionary.keys():
        print("-----------------------------------")
        print("List: ", ListName)
        print("Length: ", len(GlobalDictionary[ListName]))
        print("-----------------------------------")
        print()
    input()
    ClearOutput()
    return

def GetItems(TempContentList):
    Links = []
    for item in TempContentList:
        for tag in item.findAll("a"):
            try:
                Links.append(dict(word=tag.text, definition=tag.get("title")))
            except:
                print("Error in getting word and definition")
    return Links

def ScrapeAListFromVocabulary(url, ListName, length):
    # Get the content of the page
    Req = requests.get(url)
    # Parse the content using html.parser
    Soup = BeautifulSoup(Req.text, 'html.parser')

    TempContentList = []
    Entry = "entry"

    for i in range(length):
        try:
            Element = Soup.find("li", {"id":Entry+str(i)})
            TempContentList.append(Element)
        except:
            print("ID: " + Entry + str(i) + " Not Found!!")

    TempWordsList = GetItems(TempContentList)
    FinalWordsList = []
    
    for item in TempWordsList:
        TempDictionary = {}
        TempDictionary['word'] = item['word']
        TempDictionary['Definition'] = item['definition']

        FinalWordsList.append(TempDictionary)

    print("\nNumber of words added : {}".format(len(FinalWordsList)))

    if len(FinalWordsList) > 0:
        GlobalDictionary[ListName] = FinalWordsList
        print("\nList succesfully added!")
        input("\nPress Enter to continue")
        UpdateVocabulary()
    else:
        print("Unsuccessful! No words added!")

def ScrapWordMeaning(word):
    print("Word Added : ".format(word.strip()))
    URL = 'https://www.vocabulary.com/dictionary/' + str(word).strip()
    
    # Get the html content using requests
    try:
        Req = requests.get(URL)
    except:
        return

    # Parse the content
    Soup = BeautifulSoup(Req.content, 'html.parser')

    # Create a dict which will be returned
    ReturnDictionary = {}

    try:
        ReturnDictionary['Short Explanation'] = Soup.find("p", class_="short").text  # type: ignore
    except:
        print("Short explanation not found for {}".format(word.strip()))
    
    try:
        ReturnDictionary['Long Explanation'] = Soup.find("p", class_="long").text    # type: ignore
    except:
        print("Long Explanation not found for {}".format(word.strip()))
    
    try:
        ReturnDictionary['Synonyms'] = Soup.find("dd").text  # type: ignore
    except:
        print("Synonyms not found for {}".format(word.strip()))

    return ReturnDictionary

def AddAList():
    url = str(input("\nEnter URL : "))
    length = int(input("\nEnter List Length : "))
    ListName = str(input("\nEnter List Name : "))

    ScrapeAListFromVocabulary(url, ListName, length)
    with open(GREWordList, 'w') as f:
        json.dump(GlobalDictionary, f)
        f.close()
    
    input()
    ClearOutput()  

def InteractiveLearner(ListName = "Miscellaneous", NoOfWords = 20):
    '''
    Randomly choose words from the mentioned list
    '''
    ClearOutput()
    print("Type 'exp' or 'e' for explanation")

    RandomWordList = random.sample(GlobalDictionary[ListName], NoOfWords)
    
    try:
        f = open(TestedWordsList, 'r')
        TestedWords = json.load(f)
        f.close()
    except:
        TestedWords = {}

    # Number of words learnt
    count = 0

    for WordDictionary in RandomWordList:
        count += 1
        print("--------------------------------------------------------")
        print("\n" + str(count) + ". " + WordDictionary['word'].strip() + '  ::  ' + WordDictionary['Definition'].strip())

        # Save the word in tested words
        if WordDictionary['word'] not in TestedWords:
            TestedWords[WordDictionary['word']] = WordDictionary['Definition']

        while(True):
            String = str(input())
            if String == 'e' or String == 'exp':
                for key, value in VocabDictionary[WordDictionary['word']].items():
                    print("\n" + key.strip() + " : " + value.strip()) 
            elif String == 'q':
                if TestedWords.__len__() > 1:
                    f = open(TestedWordsList, 'w')
                    json.dump(TestedWords, f)
                    f.close()
                ClearOutput()
                return
            elif len(String) <= 1:
                break
            else:
                print("\nInvalid Choice! Press Enter to continue.")
                input()

    if TestedWords.__len__() > 1:
        f = open(TestedWordsList, 'w')
        json.dump(TestedWords, f)
        f.close()
    
    ClearOutput()
    return

def Learn():
    ClearOutput()
    Heading("Learn From A List")
    Lists = list(GlobalDictionary.keys())
    print("\nWhich list do you want to prepare from? Here are the options:\n")
    
    for i in range(len(Lists)):
        print(str(i+1) + ". " + Lists[i])
    
    ListChoice = input("\nEnter your choice: ")
    while True:
        if ListChoice.isnumeric(): #type: ignore
            ListChoice = int(ListChoice)
            if(ListChoice > 0 and ListChoice <= len(Lists)):
                break
            else:
                print("\nInvalid choice! Enter a number less than or equal to {}".format(len(Lists)))
                ListChoice = input("\nEnter your choice: ")
        else:
            print("\nInvalid choice! Enter numerical input.")
            ListChoice = input("\nEnter your choice: ")
    
    NoOfWords = input("\nHow many words do you want to revise : ")
    while True:
        if NoOfWords.isnumeric():
            NoOfWords = int(NoOfWords)
            if(NoOfWords > GlobalDictionary[Lists[ListChoice-1]].__len__()):
                print("\nInvalid choice! Enter a number less than or equal to {}".format(GlobalDictionary[Lists[ListChoice-1]].__len__()))
                NoOfWords = input("\nHow many words do you want to revise : ")
            else:
                break
        else:
            print("\nInvalid choice! Enter numerical input.")
            NoOfWords = input("\nHow many words do you want to revise : ")

    InteractiveLearner(Lists[ListChoice], NoOfWords)
    return

def MCQTestLearnt():
    ClearOutput()
    Heading("MCQ Test Revision")
    random.seed()
    
    with open(TestedWordsList, 'r') as f:
        WordDictionary = json.load(f)
        f.close()
    
    # Extract words in a list
    Words = list(WordDictionary.keys())

    print("\nHow many words do you want in the test from a total of {} words : ".format(len(Words)), end='')
    NoOfQuestions = input()
    while True:
        if NoOfQuestions.isnumeric():
            NoOfQuestions = int(NoOfQuestions)
            
            # Verify that length of words in more than number of questions
            if NoOfQuestions <= len(Words):
                break
            else:
                print("\nPlease Enter a number less than or equal to {}".format(len(Words)))
                print("\nHow many words do you want in the test from a total of {} words : ".format(len(Words)), end='')
                NoOfQuestions = input()
        else:
            print("\nInvalid choice! Enter numerical input.")
            print("\nHow many words do you want in the test from a total of {} words : ".format(len(Words)), end='')
            NoOfQuestions = input()

    # Sample random words
    TestWord = random.sample(Words, NoOfQuestions)
    
    # Start the tester
    Correct = 0
    Incorrect = 0
    Answer = 0
    AnswerIndex = 0
    for i in range(NoOfQuestions):
        print("\n------------------------------------------------")
        RandomListName = random.choice(list(GlobalDictionary.keys()))
        RandomDictionaryList = random.sample(GlobalDictionary[RandomListName], 4)
        RandomWords = [list(word.values())[0] for word in RandomDictionaryList]
        RandomMeanings = [list(word.values())[1] for word in RandomDictionaryList]
        Types = ["Synonym To Meaning", "Meaning To Synonym"]
        RandomType = random.choice(Types)
        
        if RandomType == "Synonym To Meaning":
            print("\nWhat is the meaning of {}?\n".format(TestWord[i].strip()))
            
            if WordDictionary[TestWord[i]] not in RandomMeanings:
                RandomMeanings.append(WordDictionary[TestWord[i]])
                random.shuffle(RandomMeanings)

            Count = 0
            for meaning in RandomMeanings:
                Count += 1
                if meaning == WordDictionary[TestWord[i]]:
                    AnswerIndex = Count
                print("{}. {}".format(Count, meaning.strip()))

            Answer = input("\nAnswer: ")
            while True:
                if Answer.isnumeric():
                    if int(Answer) in [1, 2, 3, 4, 5]:
                        Answer = int(Answer)
                        break
                    else:
                        print("\nValid options are 1, 2, 3, 4 & 5. Enter again")
                        Answer = input("\nAnswer: ")
                else:
                    print("\nInvalid choice! Enter numerical input.")
                    Answer = input("\nAnswer: ")

        else:
            print('\nWhat word descibes "{}"?\n'.format(WordDictionary[TestWord[i]].strip()))

            if TestWord[i] not in RandomWords:
                RandomWords.append(TestWord[i])
                random.shuffle(RandomWords)

            Count = 0
            for word in RandomWords:
                Count += 1
                if word == TestWord[i]:
                    AnswerIndex = Count
                print("{}. {}".format(Count, word.strip()))

            Answer = input("\nAnswer: ")
            while True:
                if Answer.isnumeric():
                    if int(Answer) in [1, 2, 3, 4, 5]:
                        Answer = int(Answer)
                        break
                    else:
                        print("\nValid options are 1, 2, 3, 4 & 5. Enter again")
                        Answer = input("\nAnswer: ")
                else:
                    print("\nInvalid choice! Enter numerical input.")
                    Answer = input("\nAnswer: ")

        # increase the scores
        if Answer == AnswerIndex:
            Correct += 1
            print("\nCorrect ✅")
        else:
            Incorrect += 1
            print("\nIncorrect ❌")
            if RandomType == "Synonym To Meaning":
                print("\nThe correct answer is : {}".format(WordDictionary[TestWord[i]]))
            else:
                print("\nThe correct answer is : {}".format(TestWord[i]))

        print("\n\n-------------------------------------\n")
        print("          Score: {} / {}".format(Correct, Correct + Incorrect))
        print("\n-------------------------------------")
        print()
        input()
        ClearOutput()
    
    if Correct >= (Correct + Incorrect) / 2:
        print("\n-------------------------------------\n")
        print("        Final Score: {} / {}".format(Correct, (Correct + Incorrect)))
        print("\n      You passed the test 🤩")
        print("\n-------------------------------------\n")
        input()
        ClearOutput()
        return
    else:
        print("\n-------------------------------------\n")
        print("        Final Score: {} / {}".format(Correct, (Correct + Incorrect)))
        print("\n     You scored less than 50% 😢")
        print("\n       Try retaking the test 😊")
        print("\n-------------------------------------\n")
        input()
        ClearOutput()
        return

def MCQTestRandom():
    ClearOutput()
    Heading("MCQ Test Random")
    random.seed()

    print("\nHow many words do you want in the test : ", end='')
    NoOfQuestions = input()
    while True:
        if NoOfQuestions.isnumeric():
            NoOfQuestions = int(NoOfQuestions)
            if(NoOfQuestions <= len(VocabDictionary)):
                break
            else:
                print("\nPlease Enter a number less than or equal to {}".format(len(VocabDictionary)))
                print("\nHow many words do you want in the test : ", end='')
                NoOfQuestions = input()
        else:
            print("\nInvalid choice! Enter numerical input.")
            print("\nHow many words do you want in the test : ", end='')
            NoOfQuestions = input()
    
    # Start the tester
    Correct = 0
    Incorrect = 0
    Answer = 0
    AnswerIndex = 0
    for i in range(NoOfQuestions):
        print("\n------------------------------------------------")
        RandomListName = random.choice(list(GlobalDictionary.keys()))
        RandomDictionaryList = random.sample(GlobalDictionary[RandomListName], 5)
        RandomWords = [list(word.values())[0] for word in RandomDictionaryList]
        RandomMeanings = [list(word.values())[1] for word in RandomDictionaryList]
        RandomDictionary = {RandomWords[i]: RandomMeanings[i] for i in range(len(RandomWords))}
        Types = ["Synonym To Meaning", "Meaning To Synonym"]
        RandomType = random.choice(Types)
        Number = random.randint(0,4)
        
        if RandomType == "Synonym To Meaning":
            print("\nWhat is the meaning of {}?\n".format(RandomWords[Number].strip()))
            random.shuffle(RandomMeanings)
            Count = 0
            for meaning in RandomMeanings:
                Count += 1
                if meaning == list(RandomDictionary.values())[Number]:
                    AnswerIndex = Count
                print("{}. {}".format(Count, meaning.strip()))

            Answer = input("\nAnswer: ")
            while True:
                if Answer.isnumeric():
                    if int(Answer) in [1, 2, 3, 4, 5]:
                        Answer = int(Answer)
                        break
                    else:
                        print("\nValid options are 1, 2, 3, 4 & 5. Enter again")
                        Answer = input("\nAnswer: ")
                else:
                    print("\nInvalid choice! Enter numerical input.")
                    Answer = input("\nAnswer: ")

        else:
            print('\nWhat word descibes "{}"?\n'.format(RandomMeanings[Number].strip()))
            random.shuffle(RandomWords)
            Count = 0
            for word in RandomWords:
                Count += 1
                if word == list(RandomDictionary.keys())[Number]:
                    AnswerIndex = Count
                print("{}. {}".format(Count, word.strip()))

            Answer = input("\nAnswer: ")
            while True:
                if Answer.isnumeric():
                    if int(Answer) in [1, 2, 3, 4, 5]:
                        Answer = int(Answer)
                        break
                    else:
                        print("\nValid options are 1, 2, 3, 4 & 5. Enter again")
                        Answer = input("\nAnswer: ")
                else:
                    print("\nInvalid choice! Enter numerical input.")
                    Answer = input("\nAnswer: ")

        # increase the scores
        if Answer == AnswerIndex:
            Correct += 1
            print("\nCorrect ✅")
        else:
            Incorrect += 1
            print("\nIncorrect ❌")
            if RandomType == "Synonym To Meaning":
                print("\nThe correct answer is : {}".format(RandomDictionary[RandomWords[Number]]))
            else:
                print("\nThe correct answer is : {}".format(RandomWords[Number]))

        print("\n\n-------------------------------------\n")
        print("          Score: {} / {}".format(Correct, Correct + Incorrect))
        print("\n-------------------------------------")
        print()
        input()
        ClearOutput()
    
    if Correct >= (Correct + Incorrect) / 2:
        print("\n-------------------------------------\n")
        print("        Final Score: {} / {}".format(Correct, (Correct + Incorrect)))
        print("\n      You passed the test 🤩")
        print("\n-------------------------------------\n")
        input()
        ClearOutput()
        return
    else:
        print("\n-------------------------------------\n")
        print("        Final Score: {} / {}".format(Correct, (Correct + Incorrect)))
        print("\n     You scored less than 50% 😢")
        print("\n       Try retaking the test 😊")
        print("\n-------------------------------------\n")
        input()
        ClearOutput()
        return

def WrittenTestLearnt():
    ClearOutput()
    Heading("Written Test Revision")
    random.seed()

    with open(TestedWordsList, 'r') as f:
        WordDictionary = json.load(f)
        f.close()

    # Extract words in a list
    Words = list(WordDictionary.keys())

    print("\nHow many words do you want in the test from a total of {} words : ".format(len(Words)), end='')
    NoOfQuestions = input()
    while True:
        if NoOfQuestions.isnumeric():
            NoOfQuestions = int(NoOfQuestions)
            
            # Verify that length of words in more than number of questions
            if NoOfQuestions <= len(Words):
                break
            else:
                print("\nPlease Enter a number less than or equal to {}".format(len(Words)))
                print("\nHow many words do you want in the test from a total of {} words : ".format(len(Words)), end='')
                NoOfQuestions = input()
        else:
            print("\nInvalid choice! Enter numerical input.")
            print("\nHow many words do you want in the test from a total of {} words : ".format(len(Words)), end='')
            NoOfQuestions = input()

    # Sample random words
    TestWords = random.sample(Words, NoOfQuestions)

    Score = 0
    Count = 0
    WrongAnswers = {}

    for word in TestWords:
        print("\n-------------------------------------")
        print('\nWhat word descibes "{}"?'.format(WordDictionary[word].strip()))
        InputWord = str(input("\nAnswer: "))

        if InputWord.lower() == word.lower():
            print("\nCorrect ✅")
            Score += 1

        else:
            print("\nIncorrect ❌")
            print("\nThe correct answer is : {}".format(word.strip()))
            WrongAnswers[word] = WordDictionary[word]

        Count += 1

        print("\n\n-------------------------------------\n")
        print("          Score: {} / {}".format(Score, Count))
        print("\n-------------------------------------")
        print()
        input()
        ClearOutput()

    if Score >= Count / 2:
        print("\n-------------------------------------\n")
        print("        Final Score: {} / {}".format(Score, Count))
        print("\n      You passed the test 🤩")
        print("\n-------------------------------------\n")
        input()
    else:
        print("\n-------------------------------------\n")
        print("        Final Score: {} / {}".format(Score, Count))
        print("\n     You scored less than 50% 😢")
        print("\n       Try retaking the test 😊")
        print("\n-------------------------------------\n")
        input()
    
    # print the wrong answers
    print("\nRemember these words 📖")

    for word, meaning in WrongAnswers.items():
        print("\n{} : {}".format(word.strip(), meaning))
    
    input()
    ClearOutput()
    return

def WrittenTestRandom():
    ClearOutput()
    Heading("Written Test Random")
    random.seed()

    print("\nHow many words do you want in the test : ", end='')
    NoOfQuestions = input()
    while True:
        if NoOfQuestions.isnumeric():
            NoOfQuestions = int(NoOfQuestions)
            if(NoOfQuestions <= len(VocabDictionary)):
                break
            else:
                print("\nPlease Enter a number less than or equal to {}".format(len(VocabDictionary)))
                print("\nHow many words do you want in the test : ", end='')
                NoOfQuestions = input()
        else:
            print("Invalid choice! Enter numerical input.")
            print("\nHow many words do you want in the test : ", end='')
            NoOfQuestions = input()

    Score = 0
    Count = 0
    WrongAnswers = {}

    for i in range(NoOfQuestions):
        RandomListName = random.choice(list(GlobalDictionary.keys()))
        RandomDictionary = random.choice(GlobalDictionary[RandomListName])
        RandomWord = list(RandomDictionary.values())[0]
        RandomMeaning = list(RandomDictionary.values())[1]
        
        print("\n-------------------------------------")
        print('\nWhat word descibes "{}"?'.format(RandomMeaning.strip()))
        InputWord = str(input("\nAnswer: "))

        if InputWord.lower() == RandomWord.lower():
            print("\nCorrect ✅")
            Score += 1

        else:
            print("\nIncorrect ❌")
            print("\nThe correct answer is : {}".format(RandomWord))
            WrongAnswers[RandomWord] = RandomMeaning

        Count += 1

        print("\n\n-------------------------------------\n")
        print("          Score: {} / {}".format(Score, Count))
        print("\n-------------------------------------")
        print()
        input()
        ClearOutput()

    if Score >= Count / 2:
        print("\n-------------------------------------\n")
        print("        Final Score: {} / {}".format(Score, Count))
        print("\n      You passed the test 🤩")
        print("\n-------------------------------------\n")
        input()
    else:
        print("\n-------------------------------------\n")
        print("        Final Score: {} / {}".format(Score, Count))
        print("\n     You scored less than 50% 😢")
        print("\n       Try retaking the test 😊")
        print("\n-------------------------------------\n")
        input()
    
    # print the wrong answers
    print("\nRemember these words 📖")

    for word, meaning in WrongAnswers.items():
        print("\n{} : {}".format(word.strip(), meaning))
    
    input()
    ClearOutput()
    return

def UpdateVocabulary():
    ClearOutput()
    print("\nUpdating the local vocabulary...")
    print("\n-----------------------------------")
    print("\n        {}".format("Update Vocabulary"))
    print("\n-----------------------------------")
    for key in GlobalDictionary.keys():
        for WordDictionary in GlobalDictionary[key]:
            if WordDictionary['word'] not in VocabDictionary:
                VocabDictionary[WordDictionary['word']] = ScrapWordMeaning(WordDictionary['word'])
                VocabDictionary[WordDictionary['word']]['Definition'] = WordDictionary['Definition']

    with open(VocabularyList, 'w') as f:
        json.dump(VocabDictionary, f)
        print("\nLocal vocabulary successfully updated. Current length is {}".format(len(VocabDictionary)))
        f.close()
    input("\nPress Enter to continue")
    ClearOutput()
    return

def SearchInVocabulary(String = None):
    ClearOutput()
    Heading("Search In Vocabulary")
    if String is None:
        WordToSearch = str(input("\nEnter the word : ")).lower()
    else:
        WordToSearch = String.lower()

    if WordToSearch in VocabDictionary.keys():
        for key, value in VocabDictionary[WordToSearch].items():
            print("\n" + key + " : " + value)
    else:
        print("\nWord not found in vocabulary lists.")
    
    input()
    ClearOutput()
    return

def VocabularyLength():
    ClearOutput()
    print("\n-----------------------------------")
    print("\n        {}".format("Vocabulary Length"))
    print("\n-----------------------------------")
    print("\nThe current vocabulary length is : {}".format(len(VocabDictionary)))
    input()
    ClearOutput()
    return

def PrintMenu():
    print("------------------------------------")
    print("Please enter a number: ")
    print("1. Display all available lists")
    print("2. Add a list from Vocabulary.com")
    print("3. Learn from a list")
    print("4. Take a test")
    print("5. Update the local vocabulary")
    print("6. Search for a word")
    print("7. Vocabulary length")
    print("8. Exit")
    print("------------------------------------")

def main():
    ClearOutput()
    print("\nWelcome to the GRE World!")
    
    while(True):
        print("\nTell us What would you like to do")
        print()
        PrintMenu()
        choice = input("\nEnter your choice: ")

        
        if choice.isnumeric():
            choice = int(choice)
            if choice == 1:
                DisplayAllLists()
            elif choice == 2:
                AddAList()
            elif choice == 3:
                Learn()
            elif choice == 4:
                while(True):
                    print("\n1. MCQ (Learnt Words)\n2. MCQ (Random Words)\n3. Written Test (Learnt Words)\n4. Written Test (Random Words)\n5. Exit")
                    TestOption = input("\nSelect Test : ")
                    if TestOption.isnumeric():
                        TestOption = int(TestOption)
                        if TestOption == 1:
                            MCQTestLearnt()
                            ClearOutput()
                            break
                        elif TestOption == 2:
                            MCQTestRandom()
                            ClearOutput()
                            break
                        elif TestOption == 3:
                            WrittenTestLearnt()
                            ClearOutput()
                            break
                        elif TestOption == 4:
                            WrittenTestRandom()
                            ClearOutput()
                            break
                        elif TestOption == 5:
                            ClearOutput()
                            break
                        else:
                            print("\nInvalid Choice! Press Enter to continue.")
                            input()
                            ClearOutput()
                    else:
                        print("\nInvalid Choice! Press Enter to continue.")
                        input()
                        ClearOutput()
                    continue
            elif choice == 5:
                UpdateVocabulary()
            elif choice == 6:
                SearchInVocabulary()
            elif choice == 7:
                VocabularyLength()
            elif choice == 8:
                ClearOutput()
                sys.exit()
            else:
                print("\nInvalid Choice! Press Enter to continue.")
                input()
                ClearOutput()
        else:
            print("\nInvalid Choice! Press Enter to continue.")
            input()
            ClearOutput()
            continue

if __name__=='__main__':
    main()

