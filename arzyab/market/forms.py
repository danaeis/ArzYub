from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length, ValidationError
from arzyab.models import User
from wtforms.fields.html5 import DateField


class FilterRecordsForm(FlaskForm):
    search = StringField('',
                           validators=[Length(max=20)],
                           render_kw={"placeholder": "search ..."})
    fromdate = DateField('from date:', format='%Y-%m-%d')
    todate = DateField('to date:', format='%Y-%m-%d')
    submit = SubmitField('filter')

    def validate_fromDate(self, fromDate, toDate):
        if fromDate.data > toDate.username:
            raise ValidationError('choose valid dates, please :)')
