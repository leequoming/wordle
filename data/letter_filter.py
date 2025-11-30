################################## read and write files ##################################
# def write_file(filename, data):
#     try:
#         with open(filename, 'w', encoding='utf-8') as file:
#             file.write(data)
#         print(f"Data successfully written to '{filename}'.")
#     except (OSError, IOError) as e:
#         print(f"Error writing to file '{filename}': {e}")

# def read_file(filename):
#     try:
#         with open(filename, 'r', encoding='utf-8') as file:
#             content = file.read()
#         print(f"Data successfully read from '{filename}'.")
#         return content
#     except FileNotFoundError:
#         print(f"Error: File '{filename}' not found.")
#     except (OSError, IOError) as e:
#         print(f"Error reading file '{filename}': {e}")
#     return None

# def append_file(filename, data):
#     try:
#         with open(filename, 'a', encoding='utf-8') as file:
#             file.write(data)
#         print(f"Data successfully appended to '{filename}'.")
#     except (OSError, IOError) as e:
#         print(f"Error appending to file '{filename}': {e}")

import random
inputLen = 6
outputfile = f"letter{inputLen}.txt"

def readfile(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.readlines()
    words = []
    for line in content:
        line = line.strip() # remove leading/trailing whitespace + newline characters
        if not line:  # ensure line not empty
            continue
        for word in line.split():  # split 
            w = word.strip()  # remove leading/trailing whitespace
            if w.isalpha() and len(w) == inputLen:  # if line contains only letters and 6 letters long
                words.append(w.lower())
    words = sorted(set(words))  # remove duplicates and sort
    print(f"Total valid words found: {len(words)}")
    return words

def writefile(filename, words):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for word in words:
                file.write(word + '\n')
        print(f"Data successfully written to '{filename}'.")
    except (OSError, IOError) as e:
        print(f"Error writing to file '{filename}': {e}")
        
inputfile = "raw"

# wordOfTheDay = readfile(f"E:\\myvenv\\wordle\\data\\{inputfile}.txt")
words = readfile(f"E:\\myvenv\\wordle\\data\\{inputfile}.txt")
wordOfTheDay = random.choice(words)
print(wordOfTheDay)

writefile(f"E:\\myvenv\\wordle\\data\\{outputfile}", words)
