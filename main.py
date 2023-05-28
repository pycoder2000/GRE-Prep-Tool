import calendar
import csv
import datetime
import json
import os
import platform
import random
import requests
import sys
import time
from pathlib import Path
from typing import List

import plotext as plt
from bs4 import BeautifulSoup
from pytz import timezone
from tabulate import tabulate

# Constants should be in CAPITAL_CASE
START_DATE = "15/08/2022"  # The day you start using this program in dd/mm/yyyy format

DATA_FOLDER = Path(__file__).parent.resolve()
GRE_WORD_LIST = DATA_FOLDER / "GREWordList.json"
VOCABULARY_LIST = DATA_FOLDER / "vocabulary.json"
TESTED_WORDS_LIST = DATA_FOLDER / "TestedWords.json"
STATS_FILE = DATA_FOLDER / "Stats.txt"
TEST_SCORES_FILE = DATA_FOLDER / "TestScores.csv"


def clear_output():
    """Clears the terminal output based on the system platform."""
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() in {"Darwin", "Linux"}:
        os.system("clear")
    else:
        print("\nUnknown OS ☠️ Please check clear_output() function in Main.py")


def display_heading(heading: str):
    """Display a formatted heading."""
    print("\n-----------------------------------")
    print(f"\n        {heading}")
    print("\n-----------------------------------")
    print("\nPress Enter to continue or Q to quit at any time")


def load_json(file_path):
    """Load a JSON file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"\nUnable to find {file_path.name}. Please check the address again")
        return {}


# Global variables should be avoided, consider encapsulating them inside a class or functions
global_dictionary = load_json(GRE_WORD_LIST)
vocab_dictionary = load_json(VOCABULARY_LIST)


def DisplayAllLists():
    """Display all word lists."""
    clear_output()
    display_heading("GRE Word Lists")
    for list_name, words in global_dictionary.items():
        print("-----------------------------------")
        print(f"List: {list_name}")
        print(f"Length: {len(words)}")
        print("-----------------------------------")
    input()
    clear_output()

def get_items(temp_content_list):
    """Extracts word and definition links from the given list."""
    links = []
    for item in temp_content_list:
        for tag in item.findAll("a"):
            try:
                links.append(dict(word=tag.text, definition=tag.get("title")))
            except Exception:
                print("Error in getting word and definition")
    return links


def scrape_a_list_from_vocabulary(url, list_name, length):
    """Scrapes a word list from vocabulary.com."""
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    temp_content_list = []
    for i in range(length):
        try:
            element = soup.find("li", {"id": "entry" + str(i)})
            temp_content_list.append(element)
        except Exception:
            print(f"ID: entry{i} Not Found!!")

    temp_words_list = get_items(temp_content_list)
    final_words_list = []

    for item in temp_words_list:
        temp_dictionary = {
            'word': item['word'].strip(),
            'Definition': item['definition'].strip(),
        }
        final_words_list.append(temp_dictionary)

    print(f"\nNumber of words added: {len(final_words_list)}")

    if final_words_list:
        global_dictionary[list_name] = final_words_list
        print("\nList successfully added!")
        input("\nPress Enter to continue")
        UpdateVocabulary()
    else:
        print("Unsuccessful! No words added!")


def scrape_word_meaning(word):
    """Scrapes the meaning of a word from vocabulary.com."""
    print(f"Word Added: {word}")
    url = 'https://www.vocabulary.com/dictionary/' + word.strip()

    try:
        req = requests.get(url)
    except Exception:
        return

    soup = BeautifulSoup(req.content, 'html.parser')

    return_dictionary = {}

    for explanation_type in ["Short Explanation", "Long Explanation", "Synonyms"]:
        try:
            return_dictionary[explanation_type] = soup.find("p", class_=explanation_type.lower()).text  # type: ignore
        except Exception:
            print(f"{explanation_type} not found for {word.strip()}")

    return return_dictionary


def AddAList():
    """Add a word list to the global dictionary."""
    url = input("\nEnter URL: ")
    length = int(input("\nEnter List Length: "))
    list_name = input("\nEnter List Name: ")

    scrape_a_list_from_vocabulary(url, list_name, length)
    with open(GRE_WORD_LIST, 'w') as file:
        json.dump(global_dictionary, file)

    input()
    clear_output()


def interactive_learner(list_name="Miscellaneous", no_of_words=20, order_choice=1):
    """Interactive learning session."""
    clear_output()
    print("Type 'exp' or 'e' for explanation")

    if order_choice == 1:
        random_word_list = random.sample(global_dictionary[list_name], no_of_words)
    else:
        print(f'\nThe length of the "{list_name}" is {len(global_dictionary[list_name])}.')
        print(f'\nYou can start your revision from 1 to {len(global_dictionary[list_name]) - no_of_words + 1} (inclusive).')

        while True:
            start_choice = input("\nWhere do you want to start from (Leave empty for beginning or 1): ")
            if start_choice in ["", "0", "1"]:
                random_word_list = global_dictionary[list_name][:no_of_words]
                break
            elif start_choice.isnumeric():
                start_choice = int(start_choice)
                if 1 < start_choice <= (len(global_dictionary[list_name]) - no_of_words + 1):
                    random_word_list = global_dictionary[list_name][start_choice-1:start_choice+no_of_words-1]
                    break
                else:
                    print(f"\nInvalid choice! Enter a number less than or equal to {(len(global_dictionary[list_name]) - no_of_words + 1)}")
            else:
                print("\nInvalid choice! Enter numerical input or blank.")

    try:
        with open(TESTED_WORDS_LIST, 'r') as file:
            tested_words = json.load(file)
    except FileNotFoundError:
        tested_words = {}

    for count, word_dictionary in enumerate(random_word_list, start=1):
        print(f"--------------------------------------------------------\n{count}. {word_dictionary['word'].strip()}  ::  {word_dictionary['Definition'].strip()}")
        if word_dictionary['word'] not in tested_words:
            tested_words[word_dictionary['word']] = word_dictionary['Definition']

        while True:
            user_input = input()
            if user_input in ['e', 'exp']:
                for key, value in vocab_dictionary[word_dictionary['word']].items():
                    print(f"\n{key.strip()} : {value.strip()}") 
            elif user_input == 'q':
                if len(tested_words) > 1:
                    with open(TESTED_WORDS_LIST, 'w') as file:
                        json.dump(tested_words, file)
                clear_output()
                return
            elif len(user_input) <= 1:
                break
            else:
                print("\nInvalid Choice! Press Enter to continue.")
                input()
    
    clear_output()
    print("--------------------------------------------------------\nWords we learnt today")
    for index, word_dictionary in enumerate(random_word_list, start=1):
        print(f"\n{index}. {word_dictionary['word'].strip()}  ::  {word_dictionary['Definition'].strip()}")

    if len(tested_words) > 1:
        with open(TESTED_WORDS_LIST, 'w') as file:
            json.dump(tested_words, file)
    
    input()
    clear_output()

def Learn():
    clear_output()
    display_heading("Learn From A List")
    lists = list(global_dictionary.keys())
    print("\nWhich list do you want to prepare from? Here are the options:\n")
    
    for i, list_item in enumerate(lists, start=1):
        print(f"{i}. {list_item}")
    print("8. Exit")
    
    list_choice = input("\nEnter your choice: ")
    while True:
        if list_choice.isnumeric():
            list_choice = int(list_choice)
            if 1 <= list_choice <= (len(lists) + 1):
                if list_choice == 8:
                    clear_output()
                    return
                else:
                    break
            else:
                print(f"\nInvalid choice! Enter a number less than or equal to {len(lists) + 1}")
        else:
            print("\nInvalid choice! Enter numerical input.")
        list_choice = input("\nEnter your choice: ")

    print("\nSelect order of words:\n\n1. Random Order\n2. Serial Order")
    
    order_choice = input("\nEnter your choice: ")
    while True:
        if order_choice.isnumeric():
            order_choice = int(order_choice)
            if 1 <= order_choice <= 2:
                break
            else:
                print("\nInvalid choice! Enter a number less than or equal to 2.")
        else:
            print("\nInvalid choice! Enter numerical input.")
        order_choice = input("\nEnter your choice: ")

    no_of_words = input("\nHow many words do you want to revise : ")
    while True:
        if no_of_words.isnumeric():
            no_of_words = int(no_of_words)
            if no_of_words > len(global_dictionary[lists[list_choice-1]]):
                print(f"\nInvalid choice! Enter a number less than or equal to {len(global_dictionary[lists[list_choice-1]])}")
            else:
                break
        else:
            print("\nInvalid choice! Enter numerical input.")
        no_of_words = input("\nHow many words do you want to revise : ")

    interactive_learner(lists[list_choice-1], no_of_words, order_choice)


def save_test_scores(test_name, score, time_taken, time_stamp):
    try:
        with open(TEST_SCORES_FILE, 'a') as file:
            writer = csv.writer(file)
            writer.writerow([test_name, score, time_taken, time_stamp])
    except FileNotFoundError:
        print("\nUnable to find TestScores.csv file. Please check the address again")
        vocab_dictionary = {}


def read_scores():
    with open(TEST_SCORES_FILE, 'r') as file:
        scores = [[test_name, score, time_taken, date, time] for line in file.readlines() for test_name, score, time_taken, time_stamp in line.strip().split(',') for date, time in time_stamp.split(' ',1)]
    return scores

def mcq_test_learnt():
    clear_output()
    display_heading("MCQ Test Revision")
    random.seed()

    with open(TESTED_WORDS_LIST, 'r') as file:
        word_dictionary = json.load(file)

    words = list(word_dictionary.keys())

    no_of_questions = input(f"\nHow many words do you want in the test from a total of {len(words)} words: ")
    while True:
        if no_of_questions.isnumeric() and 0 < int(no_of_questions) <= len(words):
            no_of_questions = int(no_of_questions)
            break
        else:
            print(f"\nInvalid choice! Enter a number less than or equal to {len(words)}.")
            no_of_questions = input(f"\nHow many words do you want in the test from a total of {len(words)} words: ")

    test_word = random.sample(words, no_of_questions)

    correct = incorrect = answer = answer_index = 0
    start_time = time.time()
    for i in range(no_of_questions):
        print("\n------------------------------------------------")
        random_list_name = random.choice(list(global_dictionary.keys()))
        random_dictionary_list = random.sample(global_dictionary[random_list_name], 4)
        random_words = [list(word.values())[0] for word in random_dictionary_list]
        random_meanings = [list(word.values())[1] for word in random_dictionary_list]
        types = ["Synonym To Meaning", "Meaning To Synonym"]
        random_type = random.choice(types)

        if random_type == "Synonym To Meaning":
            print(f"\nWhat is the meaning of {test_word[i].strip()}?\n")
            process_questions(answer, answer_index, word_dictionary, test_word, i, random_meanings, correct, incorrect)
        else:
            print(f'\nWhat word describes "{word_dictionary[test_word[i]].strip()}"?\n')
            process_questions(answer, answer_index, word_dictionary, test_word, i, random_words, correct, incorrect, False)

    end_time = time.time()
    time_taken = time.strftime("%H:%M:%S", time.gmtime(end_time - start_time))
    score = f"{correct}/{correct + incorrect}"
    time_stamp = datetime.datetime.now().strftime("%d/%m/%Y %I:%M %p")
    save_test_scores("MCQ (Learnt Words)",score,time_taken,time_stamp)

    print_results(correct, incorrect, time_taken)

def process_questions(answer, answer_index, word_dictionary, test_word, i, random_list, correct, incorrect, synonym_to_meaning=True):
    if word_dictionary[test_word[i]] not in random_list:
        random_list.append(word_dictionary[test_word[i]])
        random.shuffle(random_list)

    for count, value in enumerate(random_list, start=1):
        if value == word_dictionary[test_word[i]]:
            answer_index = count
        print(f"{count}. {value.strip()}")

    answer = input("\nAnswer: ")
    while True:
        if answer.isnumeric() and int(answer) in range(1, 6):
            answer = int(answer)
            break
        else:
            print("\nValid options are 1, 2, 3, 4 & 5. Enter again")
            answer = input("\nAnswer: ")

    if answer == answer_index:
        correct += 1
        print("\nCorrect ✅")
    else:
        incorrect += 1
        print("\nIncorrect ❌")
        if synonym_to_meaning:
            print(f"\nThe correct answer is: {word_dictionary[test_word[i]]}")
        else:
            print(f"\nThe correct answer is: {test_word[i]}")

    print("\n\n-------------------------------------\n")
    print(f"          Score: {correct} / {correct + incorrect}")
    print("\n-------------------------------------\n")
    input()
    clear_output()

def print_results(correct, incorrect, time_taken):
    print("\n-------------------------------------\n")
    print(f"        Final Score: {correct} / {correct + incorrect}")
    if correct >= (correct + incorrect) / 2:
        print("\n      You passed the test 🤩")
    else:
        print("\n     You scored less than 50% 😢")
        print("\n       Try retaking the test 😊")
    print("\n-------------------------------------\n")
    print(f"\n       Time Taken: {time_taken}")
    print("\n-------------------------------------\n")
    input()
    clear_output()

def validate_questions_count(prompt: str, vocab_size: int):
    while True:
        print(f"\n{prompt} : ", end='')
        number = input()
        if number.isnumeric():
            number = int(number)
            if number <= vocab_size:
                return number
        print(f"\nInvalid choice or exceeds vocab size {vocab_size}. Enter numerical input.")

def mcq_test_random():
    clear_output()
    display_heading("MCQ Test Random")
    random.seed()

    num_questions = validate_questions_count("How many words do you want in the test", len(vocab_dictionary))

    # Start the tester
    correct, incorrect = 0, 0
    start_time = time.time()
    for _ in range(num_questions):
        print("\n------------------------------------------------")
        random_list_name = random.choice(list(global_dictionary.keys()))
        random_dictionary_list = random.sample(global_dictionary[random_list_name], 5)
        random_words = [list(word.values())[0] for word in random_dictionary_list]
        random_meanings = [list(word.values())[1] for word in random_dictionary_list]
        random_dictionary = {random_words[i]: random_meanings[i] for i in range(len(random_words))}
        types = ["Synonym To Meaning", "Meaning To Synonym"]
        random_type = random.choice(types)
        number = random.randint(0,4)

        answer, answer_index = process_questions(random_type, random_words, random_meanings, random_dictionary, number)

        # increase the scores
        if answer == answer_index:
            correct += 1
            print("\nCorrect ✅")
        else:
            incorrect += 1
            print("\nIncorrect ❌")
            if random_type == "Synonym To Meaning":
                print(f"\nThe correct answer is : {random_dictionary[random_words[number]]}")
            else:
                print(f"\nThe correct answer is : {random_words[number]}")

        print_results(correct, incorrect)
        input()
        clear_output()

    end_time = time.time()

    time_taken = time.strftime("%H:%M:%S", time.gmtime(end_time - start_time))
    score = f"{correct}/{correct + incorrect}"
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %I:%M %p")
    save_test_scores("MCQ (Random Words)", score, time_taken, timestamp)

    print_results(correct, incorrect, time_taken)

def load_tested_words(file):
    with open(file, 'r') as f:
        word_dictionary = json.load(f)
    return word_dictionary

def validate_and_get_questions_count(prompt: str, total_words: int):
    while True:
        print(f"\n{prompt} from a total of {total_words} words : ", end='')
        number = input()
        if number.isnumeric() and int(number) <= total_words:
            return int(number)
        print("\nInvalid choice or exceeds total words. Enter numerical input.")

def written_test(test_words, word_dictionary):
    score = 0
    count = 0
    wrong_answers = {}

    start_time = time.time()
    for word in test_words:
        print("\n-------------------------------------")
        print(f'\nWhat word describes "{word_dictionary[word].strip()}"?')
        input_word = input("\nAnswer: ")

        if input_word.lower() == word.lower():
            print("\nCorrect ✅")
            score += 1
        else:
            print("\nIncorrect ❌")
            print(f"\nThe correct answer is : {word.strip()}")
            wrong_answers[word] = word_dictionary[word]

        count += 1
        print_results(score, count)
        input()
        clear_output()

    end_time = time.time()
    
    time_taken = time.strftime("%H:%M:%S", time.gmtime(end_time - start_time))
    score_string = f"{score}/{count}"
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %I:%M %p")
    save_test_scores("Written Test (Learnt Words)", score_string, time_taken, timestamp)
    
    print_results(score, count, time_taken)

    print_wrong_answers(wrong_answers)

def print_wrong_answers(wrong_answers):
    print("\nRemember these words 📖")
    for word, meaning in wrong_answers.items():
        print(f"\n{word.strip()} : {meaning}")

def written_test_learnt():
    clear_output()
    display_heading("Written Test Revision")
    random.seed()

    word_dictionary = load_tested_words(TESTED_WORDS_LIST)

    words = list(word_dictionary.keys())
    num_questions = validate_and_get_questions_count("How many words do you want in the test", len(words))

    test_words = random.sample(words, num_questions)

    written_test(test_words, word_dictionary)

def written_test_random():
    clear_output()
    display_heading("Written Test Random")
    random.seed()

    num_questions = validate_and_get_questions_count("How many words do you want in the test", len(vocab_dictionary))

    word_dictionary = random.sample(list(vocab_dictionary.items()), num_questions)

    written_test(list(word_dictionary.keys()), dict(word_dictionary))

def UpdateVocabulary():
    clear_output()
    print("\nUpdating the local vocabulary...")
    print("\n-----------------------------------")
    print("\n        {}".format("Update Vocabulary"))
    print("\n-----------------------------------")
    for key in global_dictionary.keys():
        for WordDictionary in global_dictionary[key]:
            # Add new words to the vocabulary dictionary if they're not already there
            if WordDictionary['word'] not in vocab_dictionary:
                vocab_dictionary[WordDictionary['word']] = scrape_word_meaning(WordDictionary['word'])
                vocab_dictionary[WordDictionary['word']]['Definition'] = WordDictionary['Definition']
    
    # Save the updated vocabulary to a file
    with open(VOCABULARY_LIST, 'w') as f:
        json.dump(vocab_dictionary, f)
        print("\nLocal vocabulary successfully updated. Current length is {}".format(len(vocab_dictionary)))
        f.close()
    input("\nPress Enter to continue")
    clear_output()
    return

def RemoveTestedWords():
    clear_output()
    display_heading("Remove Tested Words")
    print("\nIf you feel like you have completely memorized a word in the Tested Words list, you can remove it here.")
    word = input("\nWhich word would you like to remove (Type L for the entire list): ").lower()
    
    # Open the file containing the tested words
    f = open(TESTED_WORDS_LIST,'r')
    data = json.load(f)
    f.close()

    # If user inputs "l", print the entire list of words
    if word == "l":
        for word in data.keys():
            print(word.strip())
        word = input("\nWhich word would you like to remove (Type L for the entire list): ").lower()
    
    # If the word is in the list, remove it
    if word in data.keys():
        f = open(TESTED_WORDS_LIST, 'w')
        RemovedWord = data.pop(word)
        json.dump(data, f)
        print('\n"{}" was successfully removed.'.format(word))
        f.close()
        input()
    else:
        print('\n"{}" was not found in the list.'.format(word))
        print('\nPlease check the spelling and try again.')
        input()

    clear_output()
    return

def SearchInVocabulary(String = None):
    clear_output()
    display_heading("Search In Vocabulary")
    if String is None:
        WordToSearch = str(input("\nEnter the word : ")).lower()
    else:
        WordToSearch = String.lower()

    # If the word is in the vocabulary, print its information
    if WordToSearch in vocab_dictionary.keys():
        for key, value in vocab_dictionary[WordToSearch].items():
            print("\n" + key + " : " + value)
    else:
        print("\nWord not found in vocabulary lists.")
    
    input()
    clear_output()
    return

def VocabularyLength():
    clear_output()
    print("\n-----------------------------------")
    print("\n        {}".format("Vocabulary Length"))
    print("\n-----------------------------------")
    print("\nThe current vocabulary length is : {}".format(len(vocab_dictionary)))
    input()
    clear_output()
    return

def StreakCalendar(streak_days):
    cal = calendar.Calendar()
    mydate = datetime.datetime.now()
    month = mydate.strftime("%m")
    monthString = mydate.strftime("%B")
    year = mydate.strftime("%Y")
    today = datetime.datetime.today().date()
    count = 1

    # Print a calendar for the current month and mark the days when the user practiced
    print("  Streak Calendar - {} {}".format(monthString, year))
    print()
    print("Mon  Tue  Wed  Thu  Fri  Sat  Sun")
    for x in cal.itermonthdays(int(year), int(month)):
        if x == 0:
            print("   ", end='  ')
        elif(len(str(x)) == 1):
                if(x in streak_days):
                    print(" •{}".format(x), end='  ')
                else:
                    print("  {}".format(x), end='  ')
        else:
            if(x in streak_days):
                print("•{}".format(x), end='  ')
            else:
                print(" {}".format(x), end='  ')
        count += 1
        if count == 8:
            print()
            count = 1

def Stats(DaysPassed = None,streak = None,max_streak = None, streak_days = []):
    clear_output()
    headers = ["Test Type", "Score", "Time Taken", "Date", "Time"]
    scores = read_scores()
    Days = []
    NormalizedScores = []
    if scores != []:
        for score in scores:
            ScoreNumerator = int(score[1].split("/")[0])
            ScoreDenominator = int(score[1].split("/")[1])
            NormalizedScores.append(float(ScoreNumerator / ScoreDenominator) * 100)
            Days.append(int(score[3].split("/")[0]))
    
    print("\n-----------------------------------")
    print("\n  Days Passed {} | Current Streak {}".format(DaysPassed,streak))
    print("\n-----------------------------------")
    print("\n  Your highest streak is {} days.".format(max_streak))
    print("\n-----------------------------------\n")
    StreakCalendar(streak_days)
    input()
    if NormalizedScores != []:
        print("\n-----------------------------------\n")
        print(tabulate(scores, headers=headers, tablefmt='fancy_grid'))
        print("\n-----------------------------------\n")
        print("Your average score is {}%".format(round(sum(NormalizedScores) / len(NormalizedScores), 2)))
        input()
        choice = input("\nWould you like to see your scores in a graph? (Y/N) : ").lower()
        if choice == "y":
            plt.theme('dark')
            ymin, ymax = min(NormalizedScores), max(NormalizedScores)
            plt.scatter(Days, NormalizedScores, marker='☯',color=118)
            plt.title("Performance Chart")
            plt.ylim(ymin, 1.05 * ymax)
            plt.xlim(0, 32)
            monthString = datetime.datetime.now().strftime("%B")
            plt.xlabel('Scores for {}'.format(monthString))
            xticks = [int(x) for x in range(1, 32, 2)]
            xlabels = [("Day {}").format(x) for x in range(1, 32, 2)]
            plt.xticks(xticks, xlabels)
            plt.show()
            input("\nPress Enter to continue")
        else:
            clear_output()
            return
    clear_output()
    return

def print_menu():
    print("\n------------------------------------")
    print("\nPlease enter a number:")
    print("1. Display all available lists")
    print("2. Add a list from Vocabulary.com")
    print("3. Learn from a list")
    print("4. Take a test")
    print("5. Update the local vocabulary")
    print("6. Remove words from Tested Words")
    print("7. Search for a word")
    print("8. Vocabulary length")
    print("9. Statistics")
    print("10. Exit")
    print("\n------------------------------------\n")

def read_values():
    stats_values = {'start_date': "", 'count': 0, 'today_date_string': "", 
                    'streak': 0, 'max_streak': 0, 'streak_days': []}

    with open(STATS_FILE, 'r') as f:
        for line in f:
            if line.startswith("StartDate"):
                stats_values['start_date'] = line.split("=")[1].strip().strip('"')
            elif line.startswith("Count"):
                stats_values['count'] = int(line.split("=")[1].strip())
            elif line.startswith("Today"):
                stats_values['today_date_string'] = line.split("=")[1].strip().strip('"')
            elif line.startswith("Streak = "):
                stats_values['streak'] = int(line.split("=")[1].strip())
            elif line.startswith("MaxStreak"):
                stats_values['max_streak'] = int(line.split("=")[1].strip())
            elif line.startswith("StreakDays"):
                stats_values['streak_days'] = [int(i) for i in line.split("=")[1].strip().split(",") if i.strip()]
                
    return stats_values

def write_values(stats_values):
    stats_values['streak_days'] = ','.join(map(str, stats_values['streak_days']))

    with open(STATS_FILE, 'w') as f:
        f.write('StartDate = "{}"\nCount = {}\nToday = "{}"\nStreak = {}\nMaxStreak = {}\nStreakDays = {}'.format(
            stats_values['start_date'], stats_values['count'], stats_values['today_date_string'], 
            stats_values['streak'], stats_values['max_streak'], stats_values['streak_days']))

def main():
    clear_output()
    print("\nWelcome to the GRE World!")
    
    # It's a new day
    stats_values = read_values()
    stats_today_date_object = datetime.datetime.strptime(stats_values['today_date_string'], '%d/%m/%Y')
    start_date_object = datetime.datetime.strptime(START_DATE, '%d/%m/%Y')
    today_date_string = datetime.datetime.now(timezone('Asia/Kolkata')).strftime('%d/%m/%Y')
    today_date_object = datetime.datetime.strptime(today_date_string, '%d/%m/%Y')
    days_passed = (today_date_object - start_date_object).days
    
    if str(stats_values['start_date']) != START_DATE:
        stats_values = reset_stats_values(START_DATE, today_date_string, today_date_object.day)
    else:
        if today_date_string != stats_values['today_date_string']:
            update_daily_stats_values(stats_values, today_date_object, stats_today_date_object)

    while True:    
        print("\nTell us what you would like to do")
        print()
        print_menu()
        choice = input("\nEnter your choice: ")
        
        if choice.isnumeric():
            handle_main_menu_choice(int(choice), days_passed, stats_values)
        else:
            print("\nInvalid Choice! Press Enter to continue.")
            input()
            clear_output()

def reset_stats_values(start_date, today_date_string, day):
    stats_values = {'start_date': start_date, 'count': 1, 
                    'today_date_string': today_date_string, 'streak': 1, 
                    'max_streak': 1, 'streak_days': [day]}
    write_values(stats_values)
    for file_name in [TEST_SCORES_FILE, TESTED_WORDS_LIST]:
        with open(file_name, "w+"):
            pass
    return stats_values

def update_daily_stats_values(stats_values, today_date_object, stats_today_date_object):
    stats_values['today_date_string'] = today_date_object
    stats_values['count'] += 1
    if((today_date_object - stats_today_date_object).days > 1):
        stats_values['streak'] = 1
    elif((today_date_object - stats_today_date_object).days == 1):
        stats_values['streak'] += 1
        if stats_values['streak'] > stats_values['max_streak']:
            stats_values['max_streak'] = stats_values['streak']
    else:
        stats_values['streak'] = 1
    
    if today_date_object.day not in stats_values['streak_days']:
        if(all(x < today_date_object.day for x in stats_values['streak_days'])):
            stats_values['streak_days'].append(today_date_object.day)
        else:
            stats_values['streak_days'] = [today_date_object.day]
    else:
        stats_values['streak_days'] = [today_date_object.day]

    write_values(stats_values)

def handle_main_menu_choice(choice, days_passed, stats_values):
    main_menu_actions = {1: DisplayAllLists, 2: AddAList, 3: Learn, 
                         5: UpdateVocabulary, 6: RemoveTestedWords, 
                         7: SearchInVocabulary, 8: VocabularyLength, 
                         9: lambda: Stats(days_passed + 1, stats_values['streak'], 
                                          stats_values['max_streak'], stats_values['streak_days']), 
                         10: sys.exit}
    
    if choice in main_menu_actions:
        main_menu_actions[choice]()
    elif choice == 4:
        while True:
            print("\n1. MCQ (Learnt Words)\n2. MCQ (Random Words)\n3. Written Test (Learnt Words)\n4. Written Test (Random Words)\n5. Exit")
            test_option = input("\nSelect Test : ")
            if test_option.isnumeric():
                test_option = int(test_option)
                handle_test_menu_choice(test_option)
            else:
                print("\nInvalid Choice! Press Enter to continue.")
                input()
                clear_output()
    else:
        print("\nInvalid Choice! Press Enter to continue.")
        input()
        clear_output()

def handle_test_menu_choice(choice):
    test_menu_actions = {1: mcq_test_learnt, 2: mcq_test_random, 
                         3: written_test_learnt, 4: written_test_random, 
                         5: clear_output}
    
    if choice in test_menu_actions:
        test_menu_actions[choice]()
        clear_output()
    else:
        print("\nInvalid Choice! Press Enter to continue.")
        input()
        clear_output()

if __name__ == '__main__':
    main()