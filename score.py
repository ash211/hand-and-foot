#!/usr/bin/env python

validCardValues = set(['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', '$'])

cardValues = {
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

    def addCleanCanasta(self, faceValue):
        self.score += 7 * cardValues[faceValue] + 500

    def addCleans(self):
        self.cleansValues.append(self.inputSource.getString('Enter face value of cleans (X to end): '))
        while self.cleansValues[-1] != 'X' and self.cleansValues[-1] != '':
            if isValidCardValue(self.cleansValues[-1]):
                self.addCleanCanasta(self.cleansValues[-1])
                print('New score: %d' % self.score)
            else:
                print("Invalid card: $points not in $cardValues")
                self.cleansValues.pop()
            self.cleansValues.append(self.inputSource.getString('Enter face value of cleans (X to end): '))
        self.cleansValues.pop()

    def addDirtyCanasta(self, faceValue, wilds):
        self.dirtyCanastaPoints = sum([cardValues.get(x) for x in wilds])
        self.score += self.dirtyCanastaPoints + (7-len(wilds)) * cardValues[faceValue] + 300

    def addDirties(self):
        self.dirtiesValues.append(self.inputSource.getString('Enter face value of dirties (X to end): '))
        while self.dirtiesValues[-1] != 'X' and self.dirtiesValues[-1] != '':
            if isValidCardValue(self.dirtiesValues[-1]):
                self.dirtiesWilds.append(self.inputSource.getString('What wilds? ($ or 2 separated by spaces): ').strip().split(' '))
                self.addDirtyCanasta(self.dirtiesValues[-1], self.dirtiesWilds[-1])
                print('New score: %d' % self.score)
            else:
                print("Invalid card: $points not in $cardValues")
                self.dirtiesValues.pop()
            self.dirtiesValues.append(self.inputSource.getString('Enter face value of dirties (X to end): '))
        self.dirtiesValues.pop()

    def addRedThrees(self):
        self.redThreesCount = self.inputSource.getInt('How many red threes? ')
        self.score += self.redThreesCount * 100
        print('New score: %d' % self.score)

    def addSpecials(self):
        self.addSevens()
        self.addWilds()

    def addSevens(self):
        self.sevenCanastaCount = self.inputSource.getInt('How many 7 canastas did you have? ')
        if self.sevenCanastaCount:
            self.score += self.sevenCanastaCount * (7 * cardValues.get('7') + 1500)
            print('New score: %d' % self.score)

    def addWilds(self):
        self.wildCanastaCount = self.inputSource.getInt('How many wild canastas did you have? ')
        if self.wildCanastaCount:
            self.wildCanastaJokerCount = self.inputSource.getInt('How many of those %d wild canastas were jokers? ' % self.wildCanastaCount)
            self.score += self.wildCanastaJokerCount * cardValues.get('$') + (self.wildCanastaCount * 7 - self.wildCanastaJokerCount) * cardValues.get('2') + 1500 * self.wildCanastaCount
            print('New score: %d' % self.score)

    def addGoOutBonus(self):
        self.wentOut = self.inputSource.getBoolean('Went out? (Y/N): ')
        if self.wentOut:
            # bonus
            self.score += 250
        else:
            self.handPenalty = self.inputSource.getInt('How many cards in your hand (count against you)? ')
            self.score -= self.handPenalty
            print('New score: %d' % self.score)

    def addPartialCanastas(self):
        self.partialCanastasPoints = self.inputSource.getInt('How many points on the board that are in partial canastas? ')
        self.score += self.partialCanastasPoints
        print('New score: %d' % self.score)

    def calcScore(self):
        pass

    def run(self):
        self.score = 0

        self.addGoOutBonus()
        self.addSpecials()
        self.addCleans()
        self.addDirties()
        self.addRedThrees()
        self.addPartialCanastas()

        print('Final score: %d' % self.score)

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
