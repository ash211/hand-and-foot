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

ynBooleans = {
    'Y': True,
    'y': True,
    'N': False,
    'n': False
    }

def isValidCardValue(value):
    return value in validCardValues

class TeamHandResult(object):

    def addCleanCanasta(self, faceValue):
        self.score += 7 * cardValues[faceValue] + 500

    def addCleans(self):
        self.cleansValues = []
        self.cleansValues.append(raw_input('Enter face value of cleans (X to end): '))
        while self.cleansValues[-1] != 'X' and self.cleansValues[-1] != '':
            if isValidCardValue(self.cleansValues[-1]):
                self.addCleanCanasta(self.cleansValues[-1])
                print('New score: %d' % self.score)
            else:
                print("Invalid card: $points not in $cardValues")
                self.cleansValues.pop()
            self.cleansValues.append(raw_input('Enter face value of cleans (X to end): '))
        self.cleansValues.pop()

    def addDirtyCanasta(self, faceValue, wilds):
        self.dirtyCanastaPoints = sum([cardValues.get(x) for x in wilds])
        self.score += self.dirtyCanastaPoints + (7-len(wilds)) * cardValues[faceValue] + 300

    def addDirties(self):
        self.dirtiesValues = []
        self.wilds = []
        self.dirtiesValues.append(raw_input('Enter face value of dirties (X to end): '))
        while self.dirtiesValues[-1] != 'X' and self.dirtiesValues[-1] != '':
            if isValidCardValue(self.dirtiesValues[-1]):
                self.wilds.append(raw_input('What wilds? ($ or 2 separated by spaces): ').strip().split(' '))
                self.addDirtyCanasta(self.dirtiesValues[-1], self.wilds[-1])
                print('New score: %d' % self.score)
            else:
                print("Invalid card: $points not in $cardValues")
                self.dirtiesValues.pop()
            self.dirtiesValues.append(raw_input('Enter face value of dirties (X to end): '))
        self.dirtiesValues.pop()

    def addRedThrees(self):
        self.redThreesCount = int(raw_input('How many red threes? '))
        self.score += self.redThreesCount * 100
        print('New score: %d' % self.score)

    def addSpecials(self):
        self.addSevens()
        self.addWilds()

    def addSevens(self):
        self.sevenCanastaCount = int(raw_input('How many 7 canastas did you have? '))
        if self.sevenCanastaCount:
            self.score += self.sevenCanastaCount * (7 * cardValues.get('7') + 1500)
            print('New score: %d' % self.score)

    def addWilds(self):
        self.wildCanastaCount = int(raw_input('How many wild canastas did you have? '))
        if self.wildCanastaCount:
            self.jokerCount = int(raw_input('How many of those %d wild canastas were jokers? ' % self.wildCanastaCount))
            self.score += self.jokerCount * cardValues.get('$') + (self.wildCanastaCount * 7 - self.jokerCount) * cardValues.get('2') + 1500 * self.wildCanastaCount
            print('New score: %d' % self.score)

    def addGoOutBonus(self):
        self.wentOut = [ynBooleans.get(v) for v in [raw_input('Went out? (Y/N): ')]][0]
        if self.wentOut:
            # bonus
            self.score += 250
            self.handPenalty = 0
        else:
            self.handPenalty = int(raw_input('How many cards in your hand (count against you)? '))
            self.score -= self.handPenalty
            print('New score: %d' % self.score)

    def addPartialCanastas(self):
        self.partialCanastasPoints = int(raw_input('How many points on the board that are in partial canastas? '))
        self.score += self.partialCanastasPoints
        print('New score: %d' % self.score)

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
        print "cleansValues: %s" % self.cleansValues
        print "dirtiesValues: %s" % self.dirtiesValues
        print "redThreesCount: %s" % self.redThreesCount
        print "partialCanastasPoints: %s" % self.partialCanastasPoints

if __name__ == '__main__':
    result = TeamHandResult()
    result.run()
    result.printState()
