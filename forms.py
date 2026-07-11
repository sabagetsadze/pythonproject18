from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, FileField
from wtforms.validators import DataRequired

# რეგისტრაციის ფორმა
class RegistrationForm(FlaskForm):
    first_name = StringField('სახელი', validators=[DataRequired()])
    last_name = StringField('გვარი', validators=[DataRequired()])
    email = StringField('ელ.ფოსტა', validators=[DataRequired()])
    password = PasswordField('პაროლი', validators=[DataRequired()])
    submit = SubmitField('რეგისტრაცია')

# შესვლის ფორმა
class LoginForm(FlaskForm):
    email = StringField('ელ.ფოსტა', validators=[DataRequired()])
    password = PasswordField('პაროლი', validators=[DataRequired()])
    submit = SubmitField('შესვლა')

# სიახლის ფორმა
class NewsForm(FlaskForm):
    title = StringField('სათაური', validators=[DataRequired()])
    content = TextAreaField('კონტენტი', validators=[DataRequired()])
    category = SelectField('კატეგორია', choices=[
        ('agriculture', 'სოფლის მეურნეობა'),
        ('tech', 'ციფრული ტექნოლოგიები'),
        ('sport', 'სპორტი'),
        ('science', 'მეცნიერება')
    ])
    image = FileField('ფოტოს ატვირთვა')
    submit = SubmitField('დამატება')