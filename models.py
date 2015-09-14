from flask.ext.wtf import Form
from sqlalchemy.ext.declarative import declarative_base
from wtforms.fields import SelectField, SubmitField
from wtforms_alchemy import ModelForm, ModelFieldList, model_form_factory

from app import db

from score import TeamHandState, scoreState

BaseModelForm = model_form_factory(Form)
Base = declarative_base()

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

def toBooleanOrNone(s):
    if type(s) != str and type(s) != unicode:
        return None
    return len(s) > 0 and s.lower()[0] == "y"

class Round(Base):
    __tablename__ = 'round'
    id = db.Column(db.Integer, primary_key=True)

    team = db.Column(db.Unicode(255), info={'label': 'Team Name'})

    wentOut = db.Column(db.Boolean, info={'label': 'Did you go out?'})
    #wentOut = db.Column(db.Boolean, info={'label': 'Did you go out?', 'choices': [[None, ''], [False, 'No'], [True, 'Yes']]})
    handPenalty = db.Column(db.Integer, info={'label': 'How many points in your hand?'})
    sevenCanastaCount = db.Column(db.Integer, info={'label': 'How many complete canastas of sevens?'})
    wildCanastaCount = db.Column(db.Integer, info={'label': 'How many complete canastas of wilds?'})
    wildCanastaJokerCount = db.Column(db.Integer, info={'label': 'How many jokers in those complete canastas of wilds?'})
    cleansValues = db.Column(db.Integer, info={'label': 'What were your clean books?'}) # array[String]
    dirtiesValues = db.Column(db.Integer, info={'label': 'What were your dirty books?'}) # array[String]
    dirtiesWilds = db.Column(db.Integer, info={'label': 'What were the wilds in your dirties?'}) # array[array[String]]
    redThreesCount = db.Column(db.Integer, info={'label': 'How many red threes?'})
    partialCanastasPoints = db.Column(db.Integer, info={'label': 'How many points in partial canastas?'})

    def score(self):
        state = TeamHandState()

        if self.wentOut is not None:
            state['wentOut'] = self.wentOut
        if self.handPenalty is not None:
            state['handPenalty'] = self.handPenalty
        if self.sevenCanastaCount is not None:
            state['sevenCanastaCount'] = self.sevenCanastaCount
        if self.wildCanastaCount is not None:
            state['wildCanastaCount'] = self.wildCanastaCount
        if self.wildCanastaJokerCount is not None:
            state['wildCanastaJokerCount'] = self.wildCanastaJokerCount
        if self.cleansValues is not None:
            state['cleansValues'] = self.cleansValues
        if self.dirtiesValues is not None:
            state['dirtiesValues'] = self.dirtiesValues
        if self.dirtiesWilds is not None:
            state['dirtiesWilds'] = self.dirtiesWilds
        if self.redThreesCount is not None:
            state['redThreesCount'] = self.redThreesCount
        if self.partialCanastasPoints is not None:
            state['partialCanastasPoints'] = self.partialCanastasPoints

        return scoreState(state)

class RoundForm(ModelForm):
    class Meta:
        model = Round

    #wentOut = SelectField('Did you go out?', default='', choices=[['', ''], ['No', 'No'], ['Yes', 'Yes']], coerce=toBooleanOrNone)
    submit = SubmitField()
