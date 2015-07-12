from flask.ext.wtf import Form
from sqlalchemy.ext.declarative import declarative_base
from wtforms.fields import FormField, SubmitField
from wtforms_alchemy import ModelForm, ModelFieldList, model_form_factory

from app import db

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

class RoundForm(ModelForm):
    class Meta:
        model = Round

    submit = SubmitField()
