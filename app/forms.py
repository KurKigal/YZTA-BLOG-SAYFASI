from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[
        DataRequired(message='Kullanıcı adı gereklidir.'),
        Length(min=3, max=64, message='Kullanıcı adı 3-64 karakter arasında olmalıdır.')
    ])
    email = StringField('E-posta', validators=[
        DataRequired(message='E-posta gereklidir.'),
        Email(message='Geçerli bir e-posta adresi giriniz.')
    ])
    password = PasswordField('Şifre', validators=[
        DataRequired(message='Şifre gereklidir.'),
        Length(min=6, message='Şifre en az 6 karakter olmalıdır.')
    ])
    password_confirm = PasswordField('Şifre Tekrar', validators=[
        DataRequired(message='Şifre tekrarı gereklidir.'),
        EqualTo('password', message='Şifreler eşleşmiyor.')
    ])
    submit = SubmitField('Kayıt Ol')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Bu kullanıcı adı zaten kullanılıyor.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Bu e-posta adresi zaten kayıtlı.')


class LoginForm(FlaskForm):
    email = StringField('E-posta', validators=[
        DataRequired(message='E-posta gereklidir.'),
        Email(message='Geçerli bir e-posta adresi giriniz.')
    ])
    password = PasswordField('Şifre', validators=[
        DataRequired(message='Şifre gereklidir.')
    ])
    remember_me = BooleanField('Beni Hatırla')
    submit = SubmitField('Giriş Yap')


class PostForm(FlaskForm):
    title = StringField('Başlık', validators=[
        DataRequired(message='Başlık gereklidir.'),
        Length(max=200, message='Başlık en fazla 200 karakter olabilir.')
    ])
    content = TextAreaField('İçerik', validators=[
        DataRequired(message='İçerik gereklidir.')
    ])
    category = SelectField('Kategori', coerce=int, validators=[])
    allow_comments = BooleanField('Yorumlara İzin Ver', default=True)
    submit = SubmitField('Yayınla')
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        from app.models import Category
        self.category.choices = [(0, 'Kategori Seçin (Opsiyonel)')] + [
            (c.id, c.name) for c in Category.query.order_by(Category.name).all()
        ]


class CommentForm(FlaskForm):
    body = TextAreaField('Yorumunuz', validators=[
        DataRequired(message='Yorum yazmanız gerekiyor.'),
        Length(max=1000, message='Yorum en fazla 1000 karakter olabilir.')
    ])
    submit = SubmitField('Yorum Yap')


class SearchForm(FlaskForm):
    query = StringField('Ara', validators=[
        DataRequired(message='Arama terimi giriniz.')
    ])
    submit = SubmitField('Ara')


class CategoryForm(FlaskForm):
    name = StringField('Kategori Adı', validators=[
        DataRequired(message='Kategori adı gereklidir.'),
        Length(max=64, message='Kategori adı en fazla 64 karakter olabilir.')
    ])
    submit = SubmitField('Ekle')
