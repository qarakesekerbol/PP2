#1
import re

text = "ab abb abbb a ac"
pattern = r"ab*"

matches = re.findall(pattern, text)
print(matches)

#2
import re

text = "ab abb abbb abbbb"
pattern = r"ab{2,3}"

matches = re.findall(pattern, text)
print(matches)

#3
import re

text = "hello_world test_value Hello_World"
pattern = r"[a-z]+_[a-z]+"

print(re.findall(pattern, text))

#4
import re

text = "Hello world Test Python"
pattern = r"[A-Z][a-z]+"

print(re.findall(pattern, text))

#5
import re

text = "acb axxxb a123b ab"
pattern = r"a.*b"

print(re.findall(pattern, text))

#6
import re

text = "Hello, world. Python is cool"
result = re.sub(r"[ ,.]", ":", text)

print(result)

#7
text = "hello_world_python"

words = text.split("_")
camel = words[0] + "".join(word.capitalize() for word in words[1:])

print(camel)

#8
import re

text = "HelloWorldPython"

result = re.split(r"(?=[A-Z])", text)

print(result)

#9
import re

text = "HelloWorldPython"

result = re.sub(r"([A-Z])", r" \1", text).strip()

print(result)

#10
import re

text = "helloWorldPython"

snake = re.sub(r'([A-Z])', r'_\1', text).lower()

print(snake)