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
def readfile(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        words = [line.strip() for line in content.splitlines() if line.strip()]
    return words
wordOfTheDay = random.choice(readfile("5letter.txt"))
print(wordOfTheDay)
