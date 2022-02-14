from app import app
from flask import redirect, render_template, url_for, flash, session
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import RegisterForm, LoginForm, CreatePlaylistForm, AddFilmToPlaylist, RedirectToPlaylist
from app.forms import DeletePlaylistForm, RatePlaylist
from app.models import User, Film, FilmInPlaylist, Playlist, RatingOfPlaylist, RoleOfUser


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    if login_form.submit.data:

        user = User.get_user_by_login(login_form.login.data)

        if user:

            if check_password_hash(user.password_of_user, login_form.password.data):

                login_user(user)
                session['role'] = user.id_of_role
                return redirect(url_for('index'))

            else:
                flash('Введён неверный пароль')
        else:
            flash('Пользователя с такими данными не существует')

    return render_template("login.html", login_form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():

    register_form = RegisterForm()
    list_of_all_roles = RoleOfUser.get_list_of_all_roles()
    register_form.select_role.choices = [i.name_of_role for i in list_of_all_roles]

    if register_form.submit.data:

        role = RoleOfUser.get_id_of_role_by_name_of_role(register_form.select_role.data)

        _hashed_password = generate_password_hash(register_form.password.data)

        User.add_user(register_form.login.data, _hashed_password, register_form.fio.data, role.id_of_role,
                      register_form.pol.data, register_form.age.data)
        return redirect(url_for('login'))

    return render_template("register.html", register_form=register_form, list_of_all_roles=list_of_all_roles)


@app.route('/create_playlist', methods=['GET', 'POST'])
@login_required
def create_playlist():

    if session['role'] == 1:

        create_playlist_form = CreatePlaylistForm()
        delete_playlist_form = DeletePlaylistForm()

        list_of_creators_playlists = Playlist.get_all_playlists_by_id_of_user(current_user.get_id())

        if create_playlist_form.submit.data:

            Playlist.add_playlist(current_user.get_id(), create_playlist_form.name_of_playlist.data)
            return redirect(url_for('create_playlist'))

        if delete_playlist_form.submit_delete.data:

            Playlist.delete_playlist(delete_playlist_form.id_playlist.data)
            return redirect(url_for('create_playlist'))

        return render_template("create_playlist.html", create_playlist_form=create_playlist_form,
                               list_of_creators_playlists=list_of_creators_playlists,
                               delete_playlist_form=delete_playlist_form)

    elif session['role'] != 1:
        return redirect(url_for('index'))


@app.route('/playlists', methods=['GET', 'POST'])
def playlists():

    list_of_all_playlists = Playlist.get_all_playlists()

    redirect_to_playlist_form = RedirectToPlaylist()

    if redirect_to_playlist_form.submit_redirect.data:
        id_playlist = redirect_to_playlist_form.id_of_playlist.data
        return redirect(url_for('playlist', id_playlist=id_playlist))

    return render_template("playlists.html", list_of_all_playlists=list_of_all_playlists,
                           redirect_to_playlist_form=redirect_to_playlist_form)


@app.route('/playlist/<id_playlist>', methods=['GET', 'POST'])
def playlist(id_playlist):

    _playlist = Playlist.get_info_about_playlist(id_playlist)
    print(_playlist)
    print(_playlist[0])

    # mean_mark = mean(_playlist[0][4].mark)
    print(_playlist[0][2].name_of_film)

    if session['role'] == 2:

        rate_playlist_form = RatePlaylist()

        if rate_playlist_form.submit_rate.data:

            RatingOfPlaylist.rate_playlist(id_playlist, current_user.get_id(), rate_playlist_form.rate_playlist.data)
            return redirect(url_for('playlist', id_playlist=id_playlist))

        return render_template("playlist.html", _playlist=_playlist, rate_playlist_form=rate_playlist_form,
                               id_playlist=id_playlist)

    return render_template("playlist.html", _playlist=_playlist, id_playlist=id_playlist)


@app.route('/films', methods=['GET', 'POST'])
@login_required
def films():

    all_films = Film.get_all_films()

    if session['role'] == 1:

        add_film_to_playlist = AddFilmToPlaylist()
        list_of_creators_playlists = Playlist.get_all_playlists_by_id_of_user(current_user.get_id())
        add_film_to_playlist.select_playlist.choices = [i.name_of_playlist for i in list_of_creators_playlists]

        if add_film_to_playlist.submit.data:

            id_playlist = Playlist.get_id_of_playlist_by_name_of_playlist(add_film_to_playlist.select_playlist.data)

            FilmInPlaylist.add_film_in_playlist(add_film_to_playlist.id_of_film.data, id_playlist.id_of_playlist)

        return render_template("films.html", all_films=all_films, add_film_to_playlist=add_film_to_playlist)

    return render_template("films.html", all_films=all_films)


@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))
