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

class ConsoleUi(object):
    def getString(self, prompt):
        return raw_input(prompt)
    def getBoolean(self, prompt):
        return raw_input(prompt).lower()[0] == "y"
    def getInt(self, prompt):
        return int(raw_input(prompt))
    def getArray(self, prompt):
        return raw_input(prompt).strip().split(' ')
    def show(self, s):
        print(s)

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

def scoreState(state):
    score = 0

    if state['wentOut']:
        score += 250
    else:
        score -= state['handPenalty']

    # seven canastas
    score += state['sevenCanastaCount'] * (7 * CARD_VALUES.get('7') + 1500)

    # wild canastas
    score += 1500 * state['wildCanastaCount']
    score += state['wildCanastaJokerCount'] * CARD_VALUES.get('$')
    score += (state['wildCanastaCount'] * 7 - state['wildCanastaJokerCount']) * CARD_VALUES.get('2')

    # clean canastas
    for cleansValue in state['cleansValues']:
        score += 7 * CARD_VALUES[cleansValue] + 500

    # dirty canastas
    for (dirtyValue, dirtyWilds) in zip(state['dirtiesValues'], state['dirtiesWilds']):
        wildFacePoints = sum([CARD_VALUES.get(x) for x in dirtyWilds])
        score += 300
        score += wildFacePoints + (7-len(dirtyWilds)) * CARD_VALUES[dirtyValue]

    # red threes
    score += state['redThreesCount'] * 100

    # partial canastas
    score += state['partialCanastasPoints']

    return score

class TeamHandInterrogator(object):

    def __init__(self, ui):
        self.ui = ui
        self.state = TeamHandState()

    def addCleans(self):
        self.state['cleansValues'].append(self.ui.getString('Enter face value of cleans (X to end): '))
        while self.state['cleansValues'][-1] != 'X' and self.state['cleansValues'][-1] != '':
            if isValidCardValue(self.state['cleansValues'][-1]):
                self.ui.show('New score: %d' % scoreState(self.state))
            else:
                self.ui.show("Invalid card: $points not in $CARD_VALUES")
                self.state['cleansValues'].pop()
            self.state['cleansValues'].append(self.ui.getString('Enter face value of cleans (X to end): '))
        self.state['cleansValues'].pop()

    def addDirties(self):
        self.state['dirtiesValues'].append(self.ui.getString('Enter face value of dirties (X to end): '))
        while self.state['dirtiesValues'][-1] != 'X' and self.state['dirtiesValues'][-1] != '':
            if isValidCardValue(self.state['dirtiesValues'][-1]):
                self.state['dirtiesWilds'].append(self.ui.getArray('What wilds? ($ or 2 separated by spaces): '))
                self.ui.show('New score: %d' % scoreState(self.state))
            else:
                self.ui.show("Invalid card: $points not in $CARD_VALUES")
                self.state['dirtiesValues'].pop()
            self.state['dirtiesValues'].append(self.ui.getString('Enter face value of dirties (X to end): '))
        self.state['dirtiesValues'].pop()

    def addRedThrees(self):
        self.state['redThreesCount'] = self.ui.getInt('How many red threes? ')
        self.ui.show('New score: %d' % scoreState(self.state))

    def addSevens(self):
        self.state['sevenCanastaCount'] = self.ui.getInt('How many 7 canastas did you have? ')
        if self.state['sevenCanastaCount']:
            self.ui.show('New score: %d' % scoreState(self.state))

    def addWilds(self):
        self.state['wildCanastaCount'] = self.ui.getInt('How many wild canastas did you have? ')
        if self.state['wildCanastaCount']:
            self.state['wildCanastaJokerCount'] = self.ui.getInt('How many of those %d wild canastas were jokers? ' % self.state['wildCanastaCount'])
            self.ui.show('New score: %d' % scoreState(self.state))

    def addGoOutBonus(self):
        self.state['wentOut'] = self.ui.getBoolean('Went out? (Y/N): ')
        if not self.state['wentOut']:
            self.state['handPenalty'] = self.ui.getInt('How many cards in your hand (count against you)? ')
            self.ui.show('New score: %d' % scoreState(self.state))

    def addPartialCanastas(self):
        self.state['partialCanastasPoints'] = self.ui.getInt('How many points on the board that are in partial canastas? ')
        self.ui.show('New score: %d' % scoreState(self.state))

    def run(self):
        self.addGoOutBonus()
        self.addSevens()
        self.addWilds()
        self.addCleans()
        self.addDirties()
        self.addRedThrees()
        self.addPartialCanastas()

if __name__ == '__main__':
    interrogator = TeamHandInterrogator(ConsoleUi())
    interrogator.run()
    print('Final score: %d' % scoreState(interrogator.state))
