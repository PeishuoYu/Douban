file = open('movies.txt', 'r', encoding="utf8")
new_file = open('new_movies.txt', 'a', encoding="utf8")
content = file.readline()
while content != '':
    content = content.replace(' ', '')
    if '</s' in content:
        content = file.readline()
        continue
    text = content.split(',,')
    if text[-1] == '' or text[-2] == '' or text[-1] == '\n':
        content = file.readline()
        continue
    if int(text[-1]) > 500 or int(text[-1]) < 60:
        content = file.readline()
        continue
    new_file.write(content)
    content = file.readline()
file.close()
new_file.close()
