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
    emotion = ''
    if polarity > 1.5:
        emotion = 'Happy'
    elif polarity >= 1 and polarity < 1.5:
        emotion = "Neutral"
    elif polarity < 1:
        emotion = "Sad"
    
    subjective = ''
    if subjectivity > .8:
        subjective = "Opinion"
    elif subjectivity < .8 and subjectivity > .6:
        subjective = "Neither"
    elif subjectivity < .6:
        subjective = "Fact"

    return emotion, subjective
    
