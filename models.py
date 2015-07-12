from flask.ext.wtf import Form
from sqlalchemy.ext.declarative import declarative_base
from wtforms.fields import FormField, SubmitField
from wtforms_alchemy import ModelForm, ModelFieldList, model_form_factory

from app import db

from score import TeamHandState, scoreState

BaseModelForm = model_form_factory(Form)
Base = declarative_base()

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

class Round(Base):
    __tablename__ = 'round'
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.Unicode(255))

    wentOut = db.Column(db.Boolean)
    handPenalty = db.Column(db.Integer)
    sevenCanastaCount = db.Column(db.Integer)
    wildCanastaCount = db.Column(db.Integer)
    wildCanastaJokerCount = db.Column(db.Integer)
    cleansValues = db.Column(db.Integer) # array[String]
    dirtiesValues = db.Column(db.Integer) # array[String]
    dirtiesWilds = db.Column(db.Integer) # array[array[String]]
    redThreesCount = db.Column(db.Integer)
    partialCanastasPoints = db.Column(db.Integer)

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

    submit = SubmitField()
