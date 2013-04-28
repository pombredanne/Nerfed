from nerfed import Application
from nerfed import Imperator
from nerfed import Sub


class LoginImperator(Imperator):

    login = String()
    password = String()

    def valid_login(self):
        if self.login == 'amirouche' and self.password == 'amirouche':
            return True, None
        else:
            return False, ['You must be amirouche!']

    cross_checks = [valid_login]


class Login(Sub):

    def get(self, app, request):
        form = LoginImperator.form()
        return self.render('login.html', form=form)

    def post(self, request):
        login = LoginImperator(self, request.form)
        ok, messages = login.valid()
        if ok:
            return self.redirect(self.reverse('index'))
        else:
            form = LoginImperator.Form(request.form, messages)
            return self.render('login.html', form=form)


class Door(Sub):

    def __init__(self):
        super(Door, self).__init__()
        self.register(Login, 'login')


class Hypermove(Application):

    def __init__(self):
        super(Hypermove, self).__init__()
        self.register('www', Door)


if __name__ == '__main__':
    app = Application()

