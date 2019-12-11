from textblob import TextBlob

def getEmotion(*args):
    blob = TextBlob(' '.join(args))
    blob.tags
    blob.noun_phrases

    totalSentences = 0
    totalSubjectivity = 0
    totalPolarity = 1
    for sentence in blob.sentences:
        totalSubjectivity += sentence.sentiment.subjectivity
        totalPolarity += sentence.sentiment.polarity
        totalSentences += 1

    subjectivity = totalSubjectivity/totalSentences
    polarity = totalPolarity/totalSentences
    print("Subjectiveity: {}".format(subjectivity))
    print("Polarity: {}".format(polarity))
    
    if polarity > 1.5:
        print('Happy')
    elif polarity >= 1 and polarity < 1.5:
        print("Neutral")
    elif polarity < 1:
        print("Sad")
    if subjectivity > .8:
        print("Thats an opinion")
    elif subjectivity < .8 or subjectivity > .6:
        print("Thats neither an opinion or a fact")
    elif subjectivity < .6:
        print("Thats a fact")
    
