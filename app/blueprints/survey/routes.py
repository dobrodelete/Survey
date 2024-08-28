import json
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, flash

from app import db
from app.forms import SurveyForm, FeedbackForm, IogvRegistrationForm, CriterionForm, SubcriterionForm, DirectionForm
from app.models import ContactInfo, Direction, Iogv, User

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
    # print(json.dumps([direction.to_dict() for direction in directions], ensure_ascii=False, indent=4))

    for direction in directions:
        direction_form = DirectionForm()  # Создаем форму для каждого направления
        direction_form.title.label = direction.title
        for criterion in direction.criterions:
            criterion_form = CriterionForm()
            criterion_form.title.label.text = criterion.title
            # print(criterion.title)
            criterion_form.question_number.data = criterion.number
            for subcriterion in criterion.subcriterions:
                subcriterion_form = SubcriterionForm()
                subcriterion_form.question_number.label.data = subcriterion.question_number
                subcriterion_form.title.label.data = subcriterion.title
                print(subcriterion.title)
                subcriterion_form.range_slider.data = '0'
                subcriterion_form.radio_buttons.choices = [
                    (p.range_min, p.title) for p in subcriterion.puncts
                ]
                criterion_form.subcriteria.append_entry(subcriterion_form)
            direction_form.criterions.append_entry(criterion_form)
        form.directions.append_entry(direction_form)  # добавляем в основную форму

    if form.validate_on_submit():
        flash('Ваш ответ был записан.', 'success')
        return redirect(url_for('survey.one_page'))

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


@survey_bp.route('/survey', methods=['GET', 'POST'])
def survey():
    form = SurveyForm()

    registration_form = IogvRegistrationForm()
    
    iogvs = Iogv.query.all()
    registration_form.iogv.choices = [(iogv.hierarchy_id, iogv.name) for iogv in iogvs]

    directions = Direction.query.all()

    for direction in directions:
        direction_form = DirectionForm()
        direction_form.title.label = direction.title
        for criterion in direction.criterions:
            criterion_form = CriterionForm()
            criterion_form.title.label.text = criterion.title
            criterion_form.question_number.data = criterion.number

            for subcriterion in criterion.subcriterions:
                subcriterion_form = SubcriterionForm()
                subcriterion_form.question_number.data = subcriterion.question_number
                subcriterion_form.title.label.text = subcriterion.title
                subcriterion_form.range_slider.data = '0'
                
                subcriterion_form.radio_buttons.choices = [
                    (p.range_min, p.title) for p in subcriterion.puncts
                ]
                
                criterion_form.subcriteria.append_entry(subcriterion_form)
            
            direction_form.criterions.append_entry(criterion_form)
        
        form.directions.append_entry(direction_form)

    if form.validate_on_submit() and registration_form.validate_on_submit():
        user = User(
            post=registration_form.post.data,
            iogv_id=registration_form.iogv.data,
            subdivision_id=None,
            created_at=datetime.utcnow().isoformat()
        )
        db.session.add(user)
        db.session.commit()

        flash('Ваш ответ был записан.', 'success')
        return redirect(url_for('survey.survey'))
    print(form.data)
    return render_template(
        'survey/survey.html',
        survey_form=form,
        registration_form=registration_form,
        title='Опрос для ИОГВ'
    )
