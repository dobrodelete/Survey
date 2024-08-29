import json

from flask import render_template, redirect, url_for, flash, request, send_file, Blueprint, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.forms import AdminLoginForm, ChangePasswordForm, SurveyForm, CommitteeForm
from app.models import Admin, User, Record, Survey, Committee, Direction, Criterion, Subcriterion, Punct
from app.schemas import Data

admin_bp = Blueprint('admin', __name__, template_folder='templates/admin')


@admin_bp.route('/')
@login_required
def index():
    return render_template('admin/dashboard.html', title='Админка - Панель управления')


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = AdminLoginForm()
    print(form.name.data)
    print(form.password.data)
    if form.validate_on_submit():
        admin = Admin.query.filter_by(name=form.name.data).first()
        if admin and check_password_hash(admin.password, form.password.data):
            login_user(admin)
            flash('Вы успешно вошли в систему.', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Неверное имя пользователя или пароль.', 'danger')
    return render_template('admin/login.html', form=form)


@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'success')
    return redirect(url_for('admin.login'))


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html', title='Админка - Панель управления')


@admin_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.password = generate_password_hash(form.new_password.data, method='sha256')
        db.session.commit()
        flash('Ваш пароль был успешно обновлен!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/change_password.html', form=form, title='Смена пароля')


@admin_bp.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    form = SurveyForm()
    if form.validate_on_submit():
        new_survey = Survey(question=form.question.data, answer=form.answer.data)
        db.session.add(new_survey)
        db.session.commit()
        flash('Ответ был успешно записан.', 'success')
        return redirect(url_for('admin.survey'))
    return render_template('admin/survey.html', form=form, title='Опросник')


@admin_bp.route('/user_data')
@login_required
def user_data():
    users = User.query.all()
    return render_template('admin/user_data.html', users=users, title='Данные опрашиваемых')


@admin_bp.route('/statistics')
@login_required
def statistics():
    records = Record.query.all()
    return render_template('admin/statistics.html', records=records, title='Статистика')


@admin_bp.route('/upload-methodology', methods=['GET', 'POST'])
@login_required
def upload_methodology():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file.save(f'/path/to/save/{file.filename}')
            flash('Файл методологии успешно загружен.', 'success')
        else:
            flash('Ошибка при загрузке файла.', 'danger')
    return render_template('admin/upload_methodology.html', title='Загрузка методологии')


@admin_bp.route('/download/<filetype>')
@login_required
def download(filetype):
    if filetype == 'xlsx':
        return send_file('/path/to/file.xlsx', as_attachment=True)
    elif filetype == 'json':
        return send_file('/path/to/file.json', as_attachment=True)
    elif filetype == 'database':
        return send_file('/path/to/database.db', as_attachment=True)
    else:
        flash('Неверный тип файла для загрузки.', 'danger')
        return redirect(url_for('admin.user_data'))


@admin_bp.route('/committees', methods=['GET'])
def view_committees():
    form = CommitteeForm()
    form.parent_id.choices = [(0, 'Нет родительского комитета')] + [(committee.id, committee.name) for committee in Committee.query.all()]
    return render_template('admin/committees.html', form=form)


@admin_bp.route('/questions')
def questions():
    directions = Direction.query.all()
    criterions = Criterion.query.all()
    subcriterions = Subcriterion.query.all()
    puncts = Punct.query.all()

    return render_template(
        'admin/questions.html',
        directions=directions,
       criterions=criterions,
       subcriterions=subcriterions,
       puncts=puncts,
       title='Вопросы'
    )


@admin_bp.route('/add_direction', methods=['GET', 'POST'])
def add_direction():
    if request.method == 'POST':
        title = request.form['title']
        new_direction = Direction(title=title)
        db.session.add(new_direction)
        db.session.commit()
        flash('Новое направление добавлено!')
        return redirect(url_for('admin.questions'))
    return render_template('admin/add_direction.html')


@admin_bp.route('/edit_direction/<int:direction_id>', methods=['GET', 'POST'])
def edit_direction(direction_id):
    direction = Direction.query.get_or_404(direction_id)
    if request.method == 'POST':
        direction.title = request.form['title']
        db.session.commit()
        flash('Направление обновлено!')
        return redirect(url_for('admin.questions'))
    return render_template('admin/edit_direction.html', direction=direction)


@admin_bp.route('/delete_direction/<int:direction_id>', methods=['GET'])
def delete_direction(direction_id):
    direction = Direction.query.get_or_404(direction_id)
    db.session.delete(direction)
    db.session.commit()
    flash('Направление удалено!')
    return redirect(url_for('admin.questions'))


@admin_bp.route('/add_criterion', methods=['GET', 'POST'])
def add_criterion():
    directions = Direction.query.all()
    if request.method == 'POST':
        title = request.form['title']
        number = request.form['number']
        direction_id = request.form['direction_id']
        new_criterion = Criterion(title=title, number=number, direction_id=direction_id)
        db.session.add(new_criterion)
        db.session.commit()
        flash('Новый критерий добавлен!')
        return redirect(url_for('admin.questions'))
    return render_template('admin/add_criterion.html', directions=directions)


@admin_bp.route('/edit_criterion/<int:criterion_id>', methods=['GET', 'POST'])
def edit_criterion(criterion_id):
    criterion = Criterion.query.get_or_404(criterion_id)
    directions = Direction.query.all()
    if request.method == 'POST':
        criterion.title = request.form['title']
        criterion.number = request.form['number']
        criterion.direction_id = request.form['direction_id']
        db.session.commit()
        flash('Критерий обновлен!')
        return redirect(url_for('admin.questions'))
    return render_template('admin/edit_criterion.html', criterion=criterion, directions=directions)


@admin_bp.route('/delete_criterion/<int:criterion_id>', methods=['GET'])
def delete_criterion(criterion_id):
    criterion = Criterion.query.get_or_404(criterion_id)
    db.session.delete(criterion)
    db.session.commit()
    flash('Критерий удален!')
    return redirect(url_for('admin.questions'))


@admin_bp.route('/add_subcriterion', methods=['GET', 'POST'])
def add_subcriterion():
    criterions = Criterion.query.all()
    if request.method == 'POST':
        title = request.form['title']
        criterion_id = request.form['criterion_id']
        new_subcriterion = Subcriterion(title=title, criterion_id=criterion_id)
        db.session.add(new_subcriterion)
        db.session.commit()
        flash('Новый подкритерий добавлен!')
        return redirect(url_for('admin.questions'))
    return render_template('admin/add_subcriterion.html', criterions=criterions)


@admin_bp.route('/edit_subcriterion/<int:subcriterion_id>', methods=['GET', 'POST'])
def edit_subcriterion(subcriterion_id):
    subcriterion = Subcriterion.query.get_or_404(subcriterion_id)
    criterions = Criterion.query.all()
    if request.method == 'POST':
        subcriterion.title = request.form['title']
        subcriterion.criterion_id = request.form['criterion_id']
        db.session.commit()
        flash('Подкритерий обновлен!')
        return redirect(url_for('admin.questions'))
    return render_template('admin/edit_subcriterion.html', subcriterion=subcriterion, criterions=criterions)


@admin_bp.route('/delete_subcriterion/<int:subcriterion_id>', methods=['GET'])
def delete_subcriterion(subcriterion_id):
    subcriterion = Subcriterion.query.get_or_404(subcriterion_id)
    db.session.delete(subcriterion)
    db.session.commit()
    flash('Подкритерий удален!')
    return redirect(url_for('admin.questions'))


@admin_bp.route('/add_punct', methods=['GET', 'POST'])
def add_punct():
    subcriterions = Subcriterion.query.all()
    if request.method == 'POST':
        title = request.form['title']
        range_min = request.form['range_min']
        range_max = request.form['range_max']
        subcriterion_id = request.form['subcriterion_id']
        new_punct = Punct(title=title, range_min=range_min, range_max=range_max, subcriterion_id=subcriterion_id)
        db.session.add(new_punct)
        db.session.commit()
        flash('Новый вопрос добавлен!')
        return redirect(url_for('admin.questions'))
    return render_template('admin/add_punct.html', subcriterions=subcriterions)


# Редактирование вопроса
@admin_bp.route('/edit_punct/<int:punct_id>', methods=['GET', 'POST'])
def edit_punct(punct_id):
    punct = Punct.query.get_or_404(punct_id)
    subcriterions = Subcriterion.query.all()
    if request.method == 'POST':
        punct.title = request.form['title']
        punct.range_min = request.form['range_min']
        punct.range_max = request.form['range_max']
        punct.subcriterion_id = request.form['subcriterion_id']
        db.session.commit()
        flash('Вопрос обновлен!')
        return redirect(url_for('admin.questions'))
    return render_template('admin/edit_punct.html', punct=punct, subcriterions=subcriterions)


@admin_bp.route('/delete_punct/<int:punct_id>', methods=['GET'])
def delete_punct(punct_id):
    punct = Punct.query.get_or_404(punct_id)
    db.session.delete(punct)
    db.session.commit()
    flash('Вопрос удален!')
    return redirect(url_for('admin.questions'))


@admin_bp.route('/questions_tree')
def questions_tree():
    directions_data = Direction.query.all()

    data = Data.model_validate({"directions": [direction.to_dict() for direction in directions_data]})
    print(data)

    return render_template('admin/questions_tree.html', directions=directions_data, data=data)


@admin_bp.route('/api/committees', methods=['GET'])
def api_committees():
    committees = Committee.query.all()
    return jsonify([{
        'id': committee.id,
        'name': committee.name,
        'info': committee.info,
        'parent_id': committee.parent_id
    } for committee in committees])


@admin_bp.route('/api/committees/<int:parent_id>', methods=['GET'])
def api_sub_committees(parent_id):
    committees = Committee.query.filter_by(parent_id=parent_id).all()
    return jsonify([{
        'id': committee.id,
        'name': committee.name,
        'info': committee.info,
        'parent_id': committee.parent_id
    } for committee in committees])


@admin_bp.route('/api/committees', methods=['POST'])
def add_committee():
    form = CommitteeForm()
    if form.validate_on_submit():
        committee = Committee(
            name=form.name.data,
            info=form.info.data,
            parent_id=form.parent_id.data if form.parent_id.data else None
        )
        db.session.add(committee)
        db.session.commit()
        return jsonify({'message': 'Комитет добавлен!'})
    return jsonify({'error': 'Ошибка при добавлении комитета.'}), 400


@admin_bp.route('/api/committees/<int:committee_id>', methods=['PUT'])
def edit_committee(committee_id):
    form = CommitteeForm()
    if form.validate_on_submit():
        committee = Committee.query.get_or_404(committee_id)
        committee.name = form.name.data
        committee.info = form.info.data
        committee.parent_id = form.parent_id.data if form.parent_id.data else None
        db.session.commit()
        return jsonify({'message': 'Комитет обновлен!'})
    return jsonify({'error': 'Invalid data'}), 400


@admin_bp.route('/api/committees/<int:committee_id>', methods=['DELETE'])
def delete_committee(committee_id):
    committee = Committee.query.get_or_404(committee_id)
    db.session.delete(committee)
    db.session.commit()
    return jsonify({'message': 'Комитет удален!'})
