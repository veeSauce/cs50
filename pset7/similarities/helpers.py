from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""

    linesA = a.split("\n")
    linesB = b.split("\n")
    matchingLines = []

    for line in linesA:
        if line in linesB:
            matchingLines.append(line)


    s = set(matchingLines)
    return list(s)


def sentences(a, b):
    """Return sentences in both a and b"""

    sentencesA = sent_tokenize(a)
    sentencesB = sent_tokenize(b)
    matchingSentences = []

    for sentence in sentencesA:
        if sentence in sentencesB:
            matchingSentences.append(sentence)

    s = set(matchingSentences)
    return list(s)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # get the length of string a
    lengthA = len(a)
    lengthB = len(b)
    listA = []
    listB = []
    matchedSubstrings = []

    # get substring from string of length n starting from first character index
    for i in range(len(a)):
        listA.append(a[i:i+n+1])

    for j in range(len(b)):
        listB.append(b[j:j+n+1])

    for sub in listA:
        if sub in listB:
            print("match found " + sub)
            matchedSubstrings.append(sub)

    return(set(matchedSubstrings))