from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, RadioField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    q = StringField('Имя, фамилия', validators=[DataRequired()])
    country = SelectField('Страна', coerce=int, choices=[
        ('1', 'Россия')])
    sex = RadioField('Пол', coerce=int, default='0', choices=[
        ('2', 'Мужской'),
        ('1', 'Женский'),
        ('0', 'Любой')])
    age_from = SelectField('Возраст', coerce=int, choices=[
        (_, 'от {}'.format(_)) for _ in range(14, 81)])
    age_to = SelectField('Возраст', coerce=int, choices=[
        (_, 'до {}'.format(_)) for _ in range(14, 81)])
    submit = SubmitField('Найти')
