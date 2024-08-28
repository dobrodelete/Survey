from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, RadioField, FieldList, \
    FormField
from wtforms.validators import DataRequired, EqualTo, Email, Optional


class AdminLoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ChangePasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')


# class SurveyForm(FlaskForm):
#     question = StringField('Question', validators=[DataRequired()])
#     answer = StringField('Answer', validators=[DataRequired()])
#     submit = SubmitField('Submit')


class SubcriterionForm(FlaskForm):
    question_number = StringField('Номер вопроса')
    title = StringField('Заголовок')
    note = StringField('Примечание')
    range_slider = StringField('Градация', validators=[DataRequired()])
    comments = TextAreaField('Комментарий', validators=[Optional()])
    radio_buttons = RadioField('Выбор ответа', choices=[], validators=[DataRequired()])


class CriterionForm(FlaskForm):
    question_number = StringField('Номер вопроса')
    title = StringField('Заголовок')
    question = TextAreaField('Вопрос', validators=[Optional()])
    subcriteria = FieldList(FormField(SubcriterionForm))


class DirectionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    criterions = FieldList(FormField(CriterionForm), min_entries=1)


class SurveyForm(FlaskForm):
    directions = FieldList(FormField(CriterionForm), min_entries=1)
    submit = SubmitField('Закончить опрос')


class FeedbackForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    email = StringField('Ваш Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class IogvRegistrationForm(FlaskForm):
    iogv = SelectField('Выберите ваш ИОГВ', validators=[DataRequired()], choices=[])
    subdivision = StringField('Ваше подразделение', validators=[DataRequired()])
    post = StringField('Введите вашу должность', validators=[DataRequired()])
    privacy = StringField('Подтверждение политики конфиденциальности', validators=[DataRequired()])
    submit = SubmitField('Регистрация')


class CommitteeForm(FlaskForm):
    name = StringField('Название комитета', validators=[DataRequired()])
    info = TextAreaField('Информация о комитете')
    parent_id = SelectField('Родительский комитет', coerce=int, choices=[])
    submit = SubmitField('Добавить комитет')
