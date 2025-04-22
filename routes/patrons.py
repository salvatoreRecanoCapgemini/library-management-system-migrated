

from flask import Blueprint, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired
from app.models import Patron, db
import logging

logging.basicConfig(level=logging.INFO)

patrons_blueprint = Blueprint('patrons', __name__)

class PatronForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    birth_date = DateField('Birth Date', validators=[DataRequired()])

@patrons_blueprint.route('/patrons', methods=['POST'])
def create_patron():
    try:
        form = PatronForm(request.form)
        if form.validate_on_submit():
            try:
                patron = Patron(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, phone=form.phone.data, birth_date=form.birth_date.data)
                db.session.add(patron)
                db.session.commit()
                return jsonify({'message': 'Patron created successfully'}), 201
            except Exception as e:
                logging.error(f"Error creating patron: {e}")
                db.session.rollback()
                return jsonify({'message': 'Internal Server Error'}), 500
        else:
            logging.info('Invalid input data')
            return jsonify({'message': 'Invalid input data'}), 400
    except Exception as e:
        logging.error(f"Error handling request: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500