from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField("Авторизуйтесь")


class RegisterForm(FlaskForm):
    login = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    fio = StringField()
    pol = StringField()
    age = IntegerField()
    select_role = SelectField(choices=[])
    submit = SubmitField("Зарегистрируйтесь")


class CreatePlaylistForm(FlaskForm):
    name_of_playlist = StringField(validators=[DataRequired()])
    submit = SubmitField("Добавить плейлист")


class AddFilmToPlaylist(FlaskForm):
    select_playlist = SelectField(choices=[])
    id_of_film = HiddenField()
    submit = SubmitField("Добавить фильм в плейлист")


class RedirectToPlaylist(FlaskForm):
    id_of_playlist = HiddenField()
    submit_redirect = SubmitField("Перейти к плейлисту")


class DeletePlaylistForm(FlaskForm):
    id_playlist = HiddenField()
    submit_delete = SubmitField("Удалить плейлист")


class RatePlaylist(FlaskForm):
    rate_playlist = IntegerField(validators=[DataRequired()])
    submit_rate = SubmitField("Оценить плейлист")
