import json

from sqlalchemy.exc import IntegrityError

from app.models import Survey, db, Punct, Subcriterion, Criterion, Direction, Committee


def create_or_update_survey(question_id=None, question_text=None, answer_text=None):
    if question_id:
        survey = Survey.query.get(question_id)
        if survey:
            survey.question = question_text if question_text else survey.question
            survey.answer = answer_text if answer_text else survey.answer
        else:
            print("Question not found.")
            return
    else:
        survey = Survey(question=question_text, answer=answer_text)
        db.session.add(survey)

    db.session.commit()
    print("Survey question created/updated successfully.")


def delete_survey(question_id: int):
    survey = Survey.query.get(question_id)
    if survey:
        db.session.delete(survey)
        db.session.commit()
        print("Survey question deleted successfully.")
    else:
        print("Question not found.")


def import_survey_data(json_data: str):
    data = json.loads(json_data)

    for direction_data in data['data']['directions']:
        existing_direction = db.session.query(Direction).filter_by(title=direction_data['title']).first()
        if existing_direction is None:
            direction = Direction(title=direction_data['title'])
            db.session.add(direction)

            for criterion_data in direction_data['criterions']:
                criterion = Criterion(
                    title=criterion_data['title'],
                    number=criterion_data['number'],
                    direction=direction
                )
                db.session.add(criterion)

                for subcriterion_data in criterion_data['subcriterions']:
                    subcriterion = Subcriterion(
                        question_number=subcriterion_data['question_number'],
                        title=subcriterion_data['title'],
                        weight=subcriterion_data['weight'],
                        criterion=criterion,
                        needed_answer=subcriterion_data.get('needed_answer', False)
                    )
                    db.session.add(subcriterion)

                    for punct_data in subcriterion_data['puncts']:
                        punct = Punct(
                            title=punct_data['title'],
                            range_min=punct_data['range_min'],
                            range_max=punct_data['range_max'],
                            prompt=punct_data.get('prompt'),
                            comment=punct_data.get('comment'),
                            subcriterion=subcriterion
                        )
                        db.session.add(punct)

    db.session.commit()
    print("Survey data imported successfully!")


def import_iogv_data(json_data: str):
    data = json.loads(json_data)
    for iogv in data:
        existing_com = db.session.query(Committee).filter_by(name=iogv).first()
        if existing_com is None:
            com = Committee(
                name=iogv,
                info=None,
            )
            db.session.add(com)

    try:
        db.session.commit()
        print("Iogv data imported successfully!")
    except IntegrityError:
        db.session.rollback()
        print("Error: Duplicate data found.")
