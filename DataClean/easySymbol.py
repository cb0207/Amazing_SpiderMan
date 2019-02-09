# -*- coding: utf-8 -*-

import re
import string

def cleanInput(input):
    input = re.sub('\n+', " ", input)
    input = re.sub('\[[0-9]*\]', "", input)
    input = re.sub(' +', " ", input)
    input = bytes(input, "UTF-8")
    input = input.decode("ascii", "ignore")
    cleanInput = []
    input = input.split(' ')
    for item in input:
        # 清除标点符号
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanInput.append(item)
    return cleanInput

def ngrams(input, n):
    input = cleanInput(input)
    output = []
    # range(len(input) - n + 1), 计算截取次数，避免出现错误
    for i in range(len(input) - n + 1):
        output.append(input[i:i + n])
    return output


if __name__ == '__main__':

html = requests.get("http://en.wikipedia.org/wiki/Python_(programming_language)")
bsObj = BeautifulSoup(html.text, 'html.parser')
content = bsObj.find("div", {"id": "mw-content-text"}).get_text()


ngram = ngrams(content, 2)
print(ngram)
print("2-grams count is: " + str(len(ngram)))