#1
with open("sample.txt", "w") as file:
    file.write("Hello, this is sample data.\n")
    file.write("Second line of text.\n")

#2
with open("sample.txt", "r") as file:
    content = file.read()
    print(content)

#3
with open("sample.txt", "a") as file:
    file.write("This is an appended line.\n")

with open("sample.txt", "r") as file:
    print(file.read())

#4
import shutil

shutil.copy("sample.txt", "sample_backup.txt")
print("File copied successfully!")

#5
import os

file_name = "sample_backup.txt"

if os.path.exists(file_name):
    os.remove(file_name)
    print("File deleted")
else:
    print("File does not exist")