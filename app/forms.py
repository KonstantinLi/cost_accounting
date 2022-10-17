from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Length


class RegistrationForm(FlaskForm):
    username = StringField(label="Ім'я користувача", validators=[DataRequired(), Length(max=64)])
    submit = SubmitField(label="Прийняти")


class CategoryForm(FlaskForm):
    category_name = StringField(label="Категорія", validators=[DataRequired(), Length(max=64)])
    submit = SubmitField(label="Прийняти")


class RecordForm(FlaskForm):
    date_time = DateTimeField(label="Дата/Час", validators=[DataRequired()])
    pay = IntegerField(label="Вартість", validators=[DataRequired()])

    submit = SubmitField(label="Прийняти")