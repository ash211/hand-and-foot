#!/usr/bin/env python

validCardValues = set(['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', '$'])

CARD_VALUES = {
    'A': 20,
    '2': 20,
    '3': 5,
    '4': 5,
    '5': 5,
    '6': 5,
    '7': 5,
    '8': 10,
    '9': 10,
    'T': 10,
    'J': 10,
    'Q': 10,
    'K': 10,
    '$': 50
    }

def isValidCardValue(value):
    return value in validCardValues

class UserInputSource(object):
    pass

class KeyboardInputSource(UserInputSource):
    def getString(self, prompt):
        return raw_input(prompt)
    def getBoolean(self, prompt):
        return raw_input(prompt).lower()[0] == "y"
    def getInt(self, prompt):
        return int(raw_input(prompt))

class TeamHandScorer(object):

    def __init__(self, inputSource):
        self.inputSource = inputSource
        self.wentOut = False
        self.handPenalty = 0
        self.sevenCanastaCount = 0
        self.wildCanastaCount = 0
        self.wildCanastaJokerCount = 0
        self.cleansValues = []
        self.dirtiesValues = []
        self.dirtiesWilds = []
        self.redThreesCount = 0
        self.partialCanastasPoints = 0

    def addCleans(self):
        self.cleansValues.append(self.inputSource.getString('Enter face value of cleans (X to end): '))
        while self.cleansValues[-1] != 'X' and self.cleansValues[-1] != '':
            if isValidCardValue(self.cleansValues[-1]):
                print('New score: %d' % self.calcScore())
            else:
                print("Invalid card: $points not in $CARD_VALUES")
                self.cleansValues.pop()
            self.cleansValues.append(self.inputSource.getString('Enter face value of cleans (X to end): '))
        self.cleansValues.pop()

    def addDirties(self):
        self.dirtiesValues.append(self.inputSource.getString('Enter face value of dirties (X to end): '))
        while self.dirtiesValues[-1] != 'X' and self.dirtiesValues[-1] != '':
            if isValidCardValue(self.dirtiesValues[-1]):
                self.dirtiesWilds.append(self.inputSource.getString('What wilds? ($ or 2 separated by spaces): ').strip().split(' '))
                print('New score: %d' % self.calcScore())
            else:
                print("Invalid card: $points not in $CARD_VALUES")
                self.dirtiesValues.pop()
            self.dirtiesValues.append(self.inputSource.getString('Enter face value of dirties (X to end): '))
        self.dirtiesValues.pop()

    def addRedThrees(self):
        self.redThreesCount = self.inputSource.getInt('How many red threes? ')
        print('New score: %d' % self.calcScore())

    def addSpecials(self):
        self.addSevens()
        self.addWilds()

    def addSevens(self):
        self.sevenCanastaCount = self.inputSource.getInt('How many 7 canastas did you have? ')
        if self.sevenCanastaCount:
            print('New score: %d' % self.calcScore())

    def addWilds(self):
        self.wildCanastaCount = self.inputSource.getInt('How many wild canastas did you have? ')
        if self.wildCanastaCount:
            self.wildCanastaJokerCount = self.inputSource.getInt('How many of those %d wild canastas were jokers? ' % self.wildCanastaCount)
            print('New score: %d' % self.calcScore())

    def addGoOutBonus(self):
        self.wentOut = self.inputSource.getBoolean('Went out? (Y/N): ')
        if not self.wentOut:
            self.handPenalty = self.inputSource.getInt('How many cards in your hand (count against you)? ')
            print('New score: %d' % self.calcScore())

    def addPartialCanastas(self):
        self.partialCanastasPoints = self.inputSource.getInt('How many points on the board that are in partial canastas? ')
        print('New score: %d' % self.calcScore())

    def calcScore(self):
        score = 0

        if self.wentOut:
            score += 250
        else:
            score -= self.handPenalty

        # seven canastas
        score += self.sevenCanastaCount * (7 * CARD_VALUES.get('7') + 1500)

        # wild canastas
        score += 1500 * self.wildCanastaCount
        score += self.wildCanastaJokerCount * CARD_VALUES.get('$')
        score += (self.wildCanastaCount * 7 - self.wildCanastaJokerCount) * CARD_VALUES.get('2')

        # clean canastas
        for cleansValue in self.cleansValues:
            score += 7 * CARD_VALUES[cleansValue] + 500

        # dirty canastas
        for (dirtyValue, dirtyWilds) in zip(self.dirtiesValues, self.dirtiesWilds):
            wildFacePoints = sum([CARD_VALUES.get(x) for x in dirtyWilds])
            score += 300
            score += wildFacePoints + (7-len(dirtyWilds)) * CARD_VALUES[dirtyValue]

        # red threes
        score += self.redThreesCount * 100

        # partial canastas
        score += self.partialCanastasPoints

        return score

    def run(self):
        self.addGoOutBonus()
        self.addSpecials()
        self.addCleans()
        self.addDirties()
        self.addRedThrees()
        self.addPartialCanastas()

    def printState(self):
        print "wentOut: %s" % self.wentOut
        print "handPenalty: %d" % self.handPenalty
        print "sevenCanastaCount: %s" % self.sevenCanastaCount
        print "wildCanastaCount: %s" % self.wildCanastaCount
        print "wildCanastaJokerCount: %s" % self.wildCanastaJokerCount
        print "cleansValues: %s" % self.cleansValues
        print "dirtiesValues: %s" % self.dirtiesValues
        print "dirtiesWilds: %s" % self.dirtiesWilds
        print "redThreesCount: %s" % self.redThreesCount
        print "partialCanastasPoints: %s" % self.partialCanastasPoints

if __name__ == '__main__':
    scorer = TeamHandScorer(KeyboardInputSource())
    scorer.run()
    scorer.printState()
    print('Final score: %d' % scorer.calcScore())
