import codecs
import math

alpha1 = 0.999
groups = {}
numBerOfParagraph = 0  # used for calculating probability of language
resultTableOfUnigram = {}
resultTableOfBigram = {}
correctTestBigram = 0
correctTestUnigram = 0
allTests = 0


def main():
    global allTests
    global correctTestBigram
    global correctTestUnigram
    global numBerOfParagraph
    global alpha1
    global groups

    text = ""
    with codecs.open('HAM-Train.txt', encoding='utf-8') as f:
        for line in f:
            text += line
            if '\n' in line:
                numBerOfParagraph += 1
                splited = text.split('@@@@@@@@@@')
                paragraph = "* " + splited[1]
                target = groups.get(splited[0])  # kind of your group
                if target is None:
                    groups[splited[0]] = Field(splited[0], paragraph)
                else:
                    target.apendingText(paragraph)
                text = ""
                #  print('i find one enter')
    # now we calculate Number of word and what we need in bigram
    # print(groups)
    # intialize resultTables
    for firstKey in groups:
        for secondKey in groups:
            resultTableOfBigram[firstKey, secondKey] = 0
            resultTableOfUnigram[firstKey, secondKey] = 0

    for key in groups:
        groups.get(key).countAllWord()
        groups.get(key).countAlldoubleWords()

    with codecs.open('HAM-Test.txt', encoding='utf-8') as g:
        for line in g:
            text += line
            if '\n' in line:
                allTests += 1
                splited = text.split('@@@@@@@@@@')
                paragraph = "* " + splited[1]
                target = groups.get(splited[0])  # kind of your group
                # print(fieldChooseBigram(paragraph.split(" ")),splited[0])  # if you want to print all perdiction of Bigram use this
                # print(fieldChooseUnigram(paragraph.split(" ")),splited[0])  # if you want to print all perdiction of Unigram use this

                unigramResult = fieldChooseUnigram(paragraph.split(" "))
                bigramResult = fieldChooseBigram(paragraph.split(" "))

                resultTableOfUnigram[unigramResult, splited[0]] += 1
                resultTableOfBigram[bigramResult, splited[0]] += 1

                if bigramResult == splited[0]:
                    correctTestBigram += 1
                if unigramResult == splited[0]:
                    correctTestUnigram += 1
                text = ""
    for key in groups:
        print("bigram results:", end=" ==>")
        result_printerOfBigram(key)
    for key in groups:
        print("unigram results", end=" ==>")
        result_printerOfUnigram(key)
    print("amount of correctness of bigram is ", correctTestBigram / allTests)
    print("amount of correctness of Unigram is ", correctTestUnigram / allTests)


def result_printerOfBigram(group):
    global resultTableOfBigram
    # global resultTableOfBigram
    global groups
    TP = resultTableOfBigram[group, group]
    makhrajPrecesion = 0
    for key in groups:
        makhrajPrecesion += resultTableOfBigram[key, group]
    makhrajRecall = 0
    for key in groups:
        makhrajRecall += resultTableOfBigram[group, key]
    prescision =TP / makhrajPrecesion
    recall = TP / makhrajRecall
    print("precision :", prescision ,"recall", recall ,"F-measure :",2 * prescision * recall / (prescision+recall) ,"of group" ,group)

def result_printerOfUnigram(group):
    global resultTableOfUnigram
    # global resultTableOfBigram
    global groups
    TP = resultTableOfUnigram[group, group]
    makhrajPrecesion = 0
    for key in groups:
        makhrajPrecesion += resultTableOfUnigram[key, group]
    makhrajRecall = 0
    for key in groups:
        makhrajRecall += resultTableOfUnigram[group, key]
    prescision =TP / makhrajPrecesion
    recall = TP / makhrajRecall
    print("precision :", prescision ,"recall", recall ,"F-measure :",2 * prescision * recall / (prescision+recall) ,"of group" ,group)

def fieldChooseUnigram(paragraph):
    global groups
    results = []
    for key in groups:
        results.append([probobiltyUnigram(paragraph, key), key])
    max = results[0]
    for temp in results:
        if temp[0] > max[0]:
            max = temp
    return max[1]


def fieldChooseBigram(paragraph):
    global groups
    results = []
    for key in groups:
        # print(probobiltyBigram(paragraph,key),print(key))
        results.append([probobiltyBigram(paragraph, key), key])
    max = results[0]
    for temp in results:
        if temp[0] > max[0]:
            max = temp
    return max[1]


def probobiltyUnigram(paragraph, group):
    result = 0
    for word in paragraph:
        amount = groups[group].probebilityOfWord(word)
        if amount == 0:
            result += math.log(1 / 100000)
        else:
            result += math.log(amount)
    return result + math.log(groups[group].count)


def probobiltyBigram(paragraph, group):  # text mean one paragraph
    global alpha1
    result = 0
    for i in range(1, len(paragraph)):
        # print(paragraph[i])
        amount = alpha1 * (groups[group].probebilityOfDoubleWord(paragraph[i - 1], paragraph[i])) + (1 - alpha1) * \
                 groups[group].probebilityOfWord(paragraph[i])
        # print(test ,alpha1 * (groups[group].probebilityOfDoubleWord(paragraph[i - 1], paragraph[i])),(1 - alpha1) * groups[group].probebilityOfWord(paragraph[i]) )
        if amount == 0:
            result += math.log(1 / 100000)
        else:
            result += math.log(amount)
    return result + math.log(groups[group].count)


class Field:

    def __init__(self, name, text):
        self.name = name
        self.paragraphs = []
        self.paragraphs.append(text)
        self.setOfWord = {}
        self.setOfDoubleWord = {}
        self.count = 1

    def __eq__(self, other):
        return self.name == other.name

    def apendingText(self, newText):
        self.paragraphs.append(newText)
        self.count += 1

    def countAllWord(self):
        for paragraph in self.paragraphs:
            self.count += 1
            arr = paragraph.split(" ")
            for x in arr:
                cond = self.setOfWord.get(x)
                if cond is None:
                    self.setOfWord[x] = 1
                else:
                    self.setOfWord[x] += 1

    def countAlldoubleWords(self):
        for pargaraph in self.paragraphs:
            words = pargaraph.split(" ")
            for i in range(1, len(words)):
                # print(self.setOfDoubleWord.get(words[i - 1], words[i]), "****")
                # print("----",test,"-----")
                if (words[i - 1], words[i]) not in self.setOfDoubleWord:
                    self.setOfDoubleWord[words[i - 1], words[i]] = 1
                else:
                    self.setOfDoubleWord[words[i - 1], words[i]] += 1

    def probebilityOfWord(self, word):
        if word in self.setOfWord:
            return self.setOfWord[word] / self.count
        else:
            return 0;

    def probebilityOfDoubleWord(self, word1, word2):
        if (word1, word2) in self.setOfDoubleWord:
            return self.setOfDoubleWord[word1, word2] / self.setOfWord[word1]
        else:
            return 0


if __name__ == '__main__':
    main()
