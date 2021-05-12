from urllib.request import urlopen

myURL = urlopen("https://www.rice666.com").read()

print(myURL)