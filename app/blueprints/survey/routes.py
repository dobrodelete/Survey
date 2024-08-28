import json

from flask import Blueprint, render_template, redirect, url_for, flash

from app import db
from app.forms import SurveyForm, FeedbackForm, IogvRegistrationForm, CriterionForm, SubcriterionForm
from app.models import ContactInfo, Direction, Iogv

survey_bp = Blueprint('survey', __name__)


@survey_bp.route('/')
def index():
    return render_template('survey/index.html', title='Главная')


@survey_bp.route('/about')
def about():
    return render_template('survey/about.html', title='О сайте')


@survey_bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    contact_info = ContactInfo.query.first()  # Предполагается, что есть хотя бы одна запись
    if form.validate_on_submit():
        # Здесь добавьте логику для обработки формы обратной связи
        flash('Ваше сообщение было отправлено.', 'success')
        return redirect(url_for('survey.feedback'))
    return render_template('survey/feedback.html', form=form, title='Обратная связь', contact_info=contact_info)


@survey_bp.route('/one_page', methods=['GET', 'POST'])
def one_page():
    form = SurveyForm()

    registration_form = IogvRegistrationForm()
    directions = Direction.query.all()
    print(json.dumps([direction.to_dict() for direction in directions], ensure_ascii=False, indent=4))

    for direction in directions:
        criterion_form = CriterionForm()
        for criterion in direction.criterions:
            subcriterion_form = SubcriterionForm()
            criterion_form.title.data = criterion.title
            criterion_form.question_number = criterion.number
            for subcriterion in criterion.subcriterions:
                subcriterion_form.question_number.data = subcriterion.question_number
                subcriterion_form.title.data = subcriterion.title
                subcriterion_form.range_slider.data = '0'
                subcriterion_form.radio_buttons.choices = [
                    (p.range_min, p.title) for p in subcriterion.puncts
                ]
                criterion_form.subcriteria.append_entry(subcriterion_form)
        form.directions.append_entry(criterion_form)

    if form.validate_on_submit():
        flash('Ваш ответ был записан.', 'success')
        return redirect(url_for('survey.one_page'))

    # print(form.data)
    return render_template('survey/one_page.html', survey_form=form, registration_form=registration_form, title='Опрос для ИОГВ')


@survey_bp.route('/instruction')
def instruction():
    return render_template('survey/instruction.html', title='Инструкция по заполнению')


@survey_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = IogvRegistrationForm()
    form.iogv.choices = [(iogv.hierarchy_id, iogv.name) for iogv in db.session.query(Iogv).all()]
    if form.validate_on_submit():
        flash('Регистрация прошла успешно!', 'success')
        return redirect(url_for('survey.instruction'))
    return render_template('survey/login.html', form=form, title='Регистрация')


@survey_bp.route('/start', methods=['GET', 'POST'])
def start():
    form = SurveyForm()
    if form.validate_on_submit():
        flash('Ваш ответ был записан.', 'success')
        return redirect(url_for('survey.start'))
    return render_template('survey/start.html', form=form, title='Опрос')
