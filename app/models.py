from flask_login import UserMixin
from app import db
from app import login_manager
from flask import flash, redirect, url_for


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = '_user'
    __table_args__ = {'extend_existing': True}

    id_of_user = db.Column(db.Integer(), primary_key=True)

    def get_id(self):
        return self.id_of_user

    @staticmethod
    def add_user(login, password, fio, role, pol, age):
        user_to_add = User(login_of_user=login, password_of_user=password, fio_of_user=fio, id_of_role=role,
                           sex_of_user=pol, age_of_user=age)
        try:
            db.session.add(user_to_add)
            db.session.commit()
            flash('Пользователь успешно добавлен')
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('register'))

    @staticmethod
    def get_user_by_login(login):
        try:
            query = db.session.query(User).filter(User.login_of_user == login).one()
            return query
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('login'))


class Film(db.Model):
    __tablename__ = 'film'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def get_all_films():
        try:
            query = db.session.query(Film)
            return query
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('films'))


class FilmInPlaylist(db.Model):
    __tablename__ = 'film_in_playlist'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def add_film_in_playlist(id_film, id_playlist):
        film_to_add = FilmInPlaylist(id_of_film=id_film, id_of_playlist=id_playlist)
        try:
            db.session.add(film_to_add)
            db.session.commit()
            flash('Фильм успешно добавлен в плейлист')
        except:
            db.session.rollback()
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('films'))

    @staticmethod
    def delete_film_in_playlist(id_playlist):
        try:
            query = db.session.query(FilmInPlaylist).filter(FilmInPlaylist.id_of_playlist == id_playlist).delete(synchronize_session=False)
            db.session.commit()
            flash('Плейлист успешно удалён')
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('create_playlist'))


class Playlist(db.Model):
    __tablename__ = 'playlist'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def add_playlist(user, name):
        playlist_to_add = Playlist(id_of_user=user, name_of_playlist=name)
        try:
            db.session.add(playlist_to_add)
            db.session.commit()
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('create_playlist'))

    @staticmethod
    def get_all_playlists_by_id_of_user(id_user):
        try:
            query = db.session.query(Playlist).filter(Playlist.id_of_user == id_user).all()
            return query
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('create_playlist'))

    @staticmethod
    def get_all_playlists():
        try:
            query = db.session.query(Playlist, User)
            query = query.join(User)
            return query.all()
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('playlist'))

    @staticmethod
    def get_id_of_playlist_by_name_of_playlist(name):
        try:
            query = db.session.query(RatingOfPlaylist).filter(Playlist.name_of_playlist == name).one()
            return query
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('films'))

    @staticmethod
    def get_info_about_playlist(id_playlist):
        try:
            query = db.session.query(Playlist, FilmInPlaylist, Film, User, RatingOfPlaylist)
            query = query.join(FilmInPlaylist, Playlist.id_of_playlist == FilmInPlaylist.id_of_playlist)
            query = query.join(Film, Film.id_of_film == FilmInPlaylist.id_of_film)
            query = query.join(User, Playlist.id_of_user == User.id_of_user)
            query = query.outerjoin(RatingOfPlaylist, RatingOfPlaylist.id_of_playlist == Playlist.id_of_playlist)
            query = query.filter(Playlist.id_of_playlist == id_playlist)
            return query.all()
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('playlist', id_playlist=id_playlist))

    @staticmethod
    def delete_playlist(id_playlist):
        # try:
        query = db.session.query(Playlist).filter(Playlist.id_of_playlist == id_playlist).delete(synchronize_session=False)
        db.session.commit()
        flash('Плейлист успешно удалён')
        # except:
        #     flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
        #     return redirect(url_for('create_playlist'))


class RatingOfPlaylist(db.Model):
    __tablename__ = 'rating_of_playlist'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def rate_playlist(id_playlist, id_user, rate):
        rate_to_add = RatingOfPlaylist(id_of_playlist=id_playlist, id_of_user=id_user, mark=rate)
        try:
            db.session.add(rate_to_add)
            db.session.commit()
            flash('Оценка успешно добавлена')
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('playlist', id_playlist=id_playlist))

    @staticmethod
    def delete_rating_of_playlist(id_playlist):
        # try:
        query = db.session.query(RatingOfPlaylist).filter(RatingOfPlaylist.id_of_playlist == id_playlist).delete(synchronize_session=False)
        db.session.commit()
        flash('Плейлист успешно удалён')
        # except:
        #     flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
        #     return redirect(url_for('create_playlist'))


class RoleOfUser(db.Model):
    __tablename__ = 'role_of_user'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def get_list_of_all_roles():
        try:
            query = db.session.query(RoleOfUser).all()
            return query
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('register'))

    @staticmethod
    def get_id_of_role_by_name_of_role(name_role):
        try:
            query = db.session.query(RoleOfUser).filter(RoleOfUser.name_of_role == name_role).one()
            return query
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('register'))
