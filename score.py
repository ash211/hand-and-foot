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

class TeamScorer(object):

    def addCleanCanasta(self, faceValue):
        self.score += 7 * cardValues[faceValue] + 500

    def addCleans(self):
        value = raw_input('Enter face value of cleans (X to end): ')
        while value != 'X' and value != '':
            if isValidCardValue(value):
                print(value)
            	self.addCleanCanasta(value)
                print('New score: %d' % self.score)
            else:
                print("Invalid card: $points not in $cardValues")
            value = raw_input('Enter face value of cleans (X to end): ')

    def addDirtyCanasta(self, faceValue, wilds):
        points = sum([cardValues.get(x) for x in wilds])
        self.score += points + (7-len(wilds)) * cardValues[faceValue] + 300

    def addDirties(self):
        value = raw_input('Enter face value of dirties (X to end): ')
        while value != 'X' and value != '':
            if isValidCardValue(value):
                wilds = raw_input('What wilds? ($ or 2 separated by spaces): ').strip().split(' ')
                self.addDirtyCanasta(value, wilds)
                print('New score: %d' % self.score)
            else:
                print("Invalid card: $points not in $cardValues")
            value = raw_input('Enter face value of dirties (X to end): ')

    def addRedThrees(self):
        count = int(raw_input('How many red threes? '))
        self.score += count * 100

    def addSpecials(self):
        self.addSevens()
        self.addWilds()

    def addSevens(self):
        sevenCanasta = [ynBooleans.get(v) for v in [raw_input('Had a 7 canasta? (Y/N): ')]][0]
        if sevenCanasta:
            self.score += 7 * cardValues.get('7') + 1500
            print('New score: %d' % self.score)

    def addWilds(self):
        wildCanasta = [ynBooleans.get(v) for v in [raw_input('Had a wild canasta? (Y/N): ')]][0]
        if wildCanasta:
            jokerCount = int(raw_input('How many of those wilds were jokers? '))
            self.score += jokerCount * cardValues.get('$') + (7 - jokerCount) * cardValues.get('2') + 1500
            print('New score: %d' % self.score)

    def addGoOutBonus(self):
        wentOut = [ynBooleans.get(v) for v in [raw_input('Went out? (Y/N): ')]][0]
        if wentOut:
            # bonus
            self.score += 250
            # seven canasta
            self.score += 7 * cardValues.get('7') + 1500
            print('New score: %d' % self.score)
            # wilds
            jokerCount = int(raw_input('How many of your wilds were jokers? '))
            self.score += jokerCount * cardValues.get('$') + (7 - jokerCount) * cardValues.get('2') + 1500
            print('New score: %d' % self.score)
        else:
            count = int(raw_input('How many cards in your hand (count against you)? '))
            self.score -= count
            print('New score: %d' % self.score)
            self.addSpecials()

    def addPartialCanastas(self):
        score = int(raw_input('How many points on the board that are in partial canastas? '))
        self.score += score
        print('New score: %d' % self.score)


    def run(self):
        self.score = 0

        self.addGoOutBonus()
        self.addCleans()
        self.addDirties()
        self.addRedThrees()
        self.addPartialCanastas()

        print('Final score: %d' % self.score)

if __name__ == '__main__':
	TeamScorer().run()
