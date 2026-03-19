#1
import os

os.makedirs("folder/subfolder/nested", exist_ok=True)
print("Directories created")

#2
items = os.listdir(".")
for item in items:
    print(item)

#3
for file in os.listdir("."):
    if file.endswith(".txt"):
        print(file)

#4
import shutil

# copy
shutil.copy("sample.txt", "folder/sample_copy.txt")

# move
shutil.move("sample.txt", "folder/sample_moved.txt")