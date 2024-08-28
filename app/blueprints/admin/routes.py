from flask import render_template, redirect, url_for, flash, request, send_file, Blueprint, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.forms import AdminLoginForm, ChangePasswordForm, SurveyForm, CommitteeForm
from app.models import Admin, User, Record, Survey, Committee

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
    print(form.name.data)
    print(form.info.data)
    print(form.parent_id.data)
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
