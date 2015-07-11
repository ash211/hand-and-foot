#!/usr/bin/env python

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
    return value in CARD_VALUES

class UserInputSource(object):
    pass

class KeyboardInputSource(UserInputSource):
    def getString(self, prompt):
        return raw_input(prompt)
    def getBoolean(self, prompt):
        return raw_input(prompt).lower()[0] == "y"
    def getInt(self, prompt):
        return int(raw_input(prompt))
    def getArray(self, prompt):
        return raw_input(prompt).strip().split(' ')

class TeamHandState(dict):
    def __init__(self):
        self['wentOut'] = False
        self['handPenalty'] = 0
        self['sevenCanastaCount'] = 0
        self['wildCanastaCount'] = 0
        self['wildCanastaJokerCount'] = 0
        self['cleansValues'] = []
        self['dirtiesValues'] = []
        self['dirtiesWilds'] = []
        self['redThreesCount'] = 0
        self['partialCanastasPoints'] = 0

class TeamHandScorer(object):

    def __init__(self, inputSource):
        self.inputSource = inputSource
        self.state = TeamHandState()

    def addCleans(self):
        self.state['cleansValues'].append(self.inputSource.getString('Enter face value of cleans (X to end): '))
        while self.state['cleansValues'][-1] != 'X' and self.state['cleansValues'][-1] != '':
            if isValidCardValue(self.state['cleansValues'][-1]):
                print('New score: %d' % self.calcScore())
            else:
                print("Invalid card: $points not in $CARD_VALUES")
                self.state['cleansValues'].pop()
            self.state['cleansValues'].append(self.inputSource.getString('Enter face value of cleans (X to end): '))
        self.state['cleansValues'].pop()

    def addDirties(self):
        self.state['dirtiesValues'].append(self.inputSource.getString('Enter face value of dirties (X to end): '))
        while self.state['dirtiesValues'][-1] != 'X' and self.state['dirtiesValues'][-1] != '':
            if isValidCardValue(self.state['dirtiesValues'][-1]):
                self.state['dirtiesWilds'].append(self.inputSource.getArray('What wilds? ($ or 2 separated by spaces): '))
                print('New score: %d' % self.calcScore())
            else:
                print("Invalid card: $points not in $CARD_VALUES")
                self.state['dirtiesValues'].pop()
            self.state['dirtiesValues'].append(self.inputSource.getString('Enter face value of dirties (X to end): '))
        self.state['dirtiesValues'].pop()

    def addRedThrees(self):
        self.state['redThreesCount'] = self.inputSource.getInt('How many red threes? ')
        print('New score: %d' % self.calcScore())

    def addSpecials(self):
        self.addSevens()
        self.addWilds()

    def addSevens(self):
        self.state['sevenCanastaCount'] = self.inputSource.getInt('How many 7 canastas did you have? ')
        if self.state['sevenCanastaCount']:
            print('New score: %d' % self.calcScore())

    def addWilds(self):
        self.state['wildCanastaCount'] = self.inputSource.getInt('How many wild canastas did you have? ')
        if self.state['wildCanastaCount']:
            self.state['wildCanastaJokerCount'] = self.inputSource.getInt('How many of those %d wild canastas were jokers? ' % self.state['wildCanastaCount'])
            print('New score: %d' % self.calcScore())

    def addGoOutBonus(self):
        self.state['wentOut'] = self.inputSource.getBoolean('Went out? (Y/N): ')
        if not self.state['wentOut']:
            self.state['handPenalty'] = self.inputSource.getInt('How many cards in your hand (count against you)? ')
            print('New score: %d' % self.calcScore())

    def addPartialCanastas(self):
        self.state['partialCanastasPoints'] = self.inputSource.getInt('How many points on the board that are in partial canastas? ')
        print('New score: %d' % self.calcScore())

    def calcScore(self):
        score = 0

        if self.state['wentOut']:
            score += 250
        else:
            score -= self.state['handPenalty']

        # seven canastas
        score += self.state['sevenCanastaCount'] * (7 * CARD_VALUES.get('7') + 1500)

        # wild canastas
        score += 1500 * self.state['wildCanastaCount']
        score += self.state['wildCanastaJokerCount'] * CARD_VALUES.get('$')
        score += (self.state['wildCanastaCount'] * 7 - self.state['wildCanastaJokerCount']) * CARD_VALUES.get('2')

        # clean canastas
        for cleansValue in self.state['cleansValues']:
            score += 7 * CARD_VALUES[cleansValue] + 500

        # dirty canastas
        for (dirtyValue, dirtyWilds) in zip(self.state['dirtiesValues'], self.state['dirtiesWilds']):
            wildFacePoints = sum([CARD_VALUES.get(x) for x in dirtyWilds])
            score += 300
            score += wildFacePoints + (7-len(dirtyWilds)) * CARD_VALUES[dirtyValue]

        # red threes
        score += self.state['redThreesCount'] * 100

        # partial canastas
        score += self.state['partialCanastasPoints']

        return score

    def run(self):
        self.addGoOutBonus()
        self.addSpecials()
        self.addCleans()
        self.addDirties()
        self.addRedThrees()
        self.addPartialCanastas()

    def printState(self):
        print self.state

if __name__ == '__main__':
    scorer = TeamHandScorer(KeyboardInputSource())
    scorer.run()
    scorer.printState()
    print('Final score: %d' % scorer.calcScore())
