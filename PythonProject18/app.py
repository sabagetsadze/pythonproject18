import os
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, News, SavedNews
from forms import RegistrationForm, LoginForm, NewsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# საქაღალდის შექმნა ფოტოებისთვის
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/category/<cat>')
def category(cat):
    news_list = News.query.filter_by(category=cat).all()
    return render_template('news_list.html', news_list=news_list, category=cat)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            file = form.image.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_item = News(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            image_filename=filename,
            user_id=current_user.id
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_news.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(first_name=form.first_name.data, last_name=form.last_name.data,email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
@login_required
def delete_news(id):
    news_item = News.query.get_or_404(id)
    if news_item.user_id == current_user.id:
        db.session.delete(news_item)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/save/<int:news_id>')
@login_required
def save_news(news_id):
    # ვამოწმებთ, ხომ არ არის უკვე შენახული
    exists = SavedNews.query.filter_by(user_id=current_user.id, news_id=news_id).first()

    if exists:
        # თუ უკვე შენახულია, ვაუქმებთ (ვშლით ბაზიდან)
        db.session.delete(exists)
        db.session.commit()
    else:
        # თუ არ არის, ვინახავთ
        new_save = SavedNews(user_id=current_user.id, news_id=news_id)
        db.session.add(new_save)
        db.session.commit()

    # ვუბრუნდებით იმავე გვერდს
    return redirect(request.referrer)

@app.route('/saved')
@login_required
def saved_news():
    # ამოვიღოთ მხოლოდ იმ სიახლეების ID-ები, რომლებიც ამ მომხმარებელს აქვს შენახული
    saved_items = SavedNews.query.filter_by(user_id=current_user.id).all()
    news_ids = [item.news_id for item in saved_items]
    # ამოვიღოთ სიახლეები ბაზიდან
    news_list = News.query.filter(News.id.in_(news_ids)).all()
    return render_template('news_list.html', news_list=news_list, category="შენახული")


@app.route('/search')
def search_news():
    query = request.args.get('q')  # მომხმარებლის მიერ ჩაწერილი ტექსტი
    if query:
        # ეძებს სიახლეებს, რომელთა სათაური შეიცავს ამ ტექსტს
        results = News.query.filter(News.title.contains(query) | News.content.contains(query)).all()
    else:
        results = []

    return render_template('news_list.html', news_list=results, category='ძიების შედეგები: ' + str(query))

if __name__ == '__main__':
    app.run(debug=True)