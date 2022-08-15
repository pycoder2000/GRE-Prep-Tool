<h1 align="center">
  GRE Preparation Tool
</h1>

<p align="center">
  A powerful tool to prepare for GRE using Command Line Terminal<br><br>
  The word lists are provided by <a href="https://www.vocabulary.com/lists/">Vocabulary.com</a>.
</p>

<div align="center">

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

</div>

![Demo](https://github.com/pycoder2000/GRE-Prep-Tool/blob/main/Demo.png?raw=True)

## 🛠 Installation & Set Up

1. Clone this repository

    ```sh
    git clone https://github.com/pycoder2000/GRE-Prep-Tool.git
    ```

2. Change directories

    ```sh
    cd GRE-Prep-Tool
    ```

3. Install dependencies

    ```sh
    pip install -r requirements.txt
    ```

4. Open main.py and edit the following lines:

    ```python
    GREWordList = "<Location to Folder>/GRE-Prep-Tool/GREWordList.json"
    VocabularyList = "<Location to Folder>/GRE-Prep-Tool/vocabulary.json"
    TestedWordsList = "<Location to Folder>/GRE-Prep-Tool/TestedWords.json"
    StatsFile = "<Location to Folder>/GRE-Prep-Tool/Stats.txt"
    TestScoresFile = "<Location to Folder>/GRE-Prep-Tool/TestScores.csv"
    ```

5. Open main.py and edit the `StartDate`:

    ```python
    # The day you start using this program in dd/mm/yyyy format
    StartDate = "dd/mm/yyyy"
    ```

6. Run Project

    ```sh
    python main.py
    ```

7. Add alias to terminal (optional)

   ```sh
   # Add the line below to your .bashrc or .zshrc file (only on MacOS)
   alias gre = 'python <Location to Folder>/GRE-Prep-Tool/main.py'
   ```

## 📚 Vocabulary Lists

1. Manhattan GRE Complete
2. GRE Complete Vocabulary List
3. Barrons 333
4. 900+ Essential GRE Words
5. Word Power Made Easy
6. GRE101
7. High Frequency Words

## ✨ Features

1. **Vocabulary Addition** Add vocabulary lists from [vocabulary.com](vocabulary.com)
  - You can add as many vocab lists as you want. Just add the link and the scraper module will scrape the list and save it.
  - Currently 7 lists are added. Details provided in **Vocabulary Lists** section above.

2. **Learn from lists**: Learn words from any of the provided lists
  - An interactive learner is created to memorize the word meanings  
  - Store learnt vocabulary in TestedWords.json

3. **Tests**: Take tests to memorize the word meanings
  - Supports 4 different types of tests:
   	1. MCQ (Learnt Words)
   	2. MCQ (Random Words)
   	3. Written Test (Learnt Words)
   	4. Written Test (Random Words)
  - Also track the time taken to complete the tests.

4. **Word Search**: Search for any word in the vocabulary
  - The vocabulary consists of all the words in all the lists.

5. **Stats**: Display the statistics of your performance
  - You can look at your Streak Calendar which shows the dates when you practiced.
  - Maintain streaks
  - Get detailed analysis of the score and time taken for every test and compare your performance

## 🪜 Folder Structure

```bash
📦 GRE-Prep-Tool
├── 📝 GREWordList.json       # Contains the list of words categorized by their list names
├── 📝 TestedWords.json       # Contains the list of words that you have learnt
├── 📝 TestScores.csv         # Contains the test scores
├── 📝 requirements.txt       # Contains the requirements needed for running this project
├── 📝 Stats.txt              # Contains Streak information
├── 📝 vocabulary.json        # Contains all the words in the vocabulary
└── 📝 main.py                # Driver code for the program
```

## 📍 RoadMap
- [x] Fix Scraping from Vocabulary.com
- [x] Add more tests
- [x] Track time taken for tests
- [x] Add statistics for tests
- [x] Add daily streak
- [x] Clean and refactor code
- [x] Add feature to save test scores
- [x] Ability to remove words from TestedWords.json
- [ ] Charts to compare performance
- [ ] Create %tile score based on performance
- [ ] Universities available with the score range

## 🔗 Links

[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/lone_Musk) [![github](https://img.shields.io/badge/github-171515?style=for-the-badge&logo=github&logoColor=white)](https://github.com/pycoder2000) [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/parth-desai-2bb1b0160/)

## 🍰 Contributing

Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request.

1. Fork the Project

2. Commit your Changes

   ```bash
   git commit -m 'Add some Feature'
   ```

3. Push to the Branch

   ```bash
   git push origin main
   ```

4. Open a Pull Request

<div align="center">

<a href="https://makeapullrequest.com" target="blank" >![PRs Welcome](https://img.shields.io/badge/PR-Welcome-brightgreen?style=for-the-badge)</a>

**Don't forget to give the project a star! Thanks again!**
</div>

## 🎉 Thanks

This project is an highly modified and working version of [this Github project](https://github.com/itsShnik/gre-preparation-tool).