import random
import os                       # handle file paths 

filename = "letter5.txt"
base_path = os.path.dirname(os.path.abspath(__file__))  # folder of fileio.py
file_path = os.path.join(base_path, filename)           # full path to letter5.txt
# print(os.path.dirname(__file__))

def readfile(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        print(content.splitlines())
        words = [line.strip() for line in content.splitlines() if line.strip()]
    print(f'total words: {len(words)}')
    return words
wordOfTheDay = random.choice(readfile(file_path))
# wordOfTheDay = random.choice(readfile(r"letter5.txt"))

print(wordOfTheDay)

