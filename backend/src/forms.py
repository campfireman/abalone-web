from collections import defaultdict

from mongoengine import DoesNotExist
from pydantic import BaseModel, Extra, PrivateAttr

from . import auth, models


class ValidationError(Exception):
    pass


class BaseForm(BaseModel):
    class Meta:
        model = None

    class Config:
        extra = Extra.allow

    _form_data: dict = PrivateAttr()
    _errors: defaultdict = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._form_data = {}
        self._errors = defaultdict(list)

    def process(self):
        self._form_data = self.dict()
        funcs = dir(self.__class__)
        cleaning_funcs = [x for x in funcs if x.startswith('clean_')]
        for name in cleaning_funcs:
            field_name = name.split('_', 1)[1]
            try:
                getattr(self, name)()
            except ValidationError as e:
                self._errors[field_name].append(str(e))

    @property
    def is_valid(self):
        self.process()
        return not bool(self._errors)

    @property
    def errors(self):
        return self._errors

    def save(self, commit=True):
        if self.errors:
            raise ValidationError('Form is not valid! Can\'t save safely.')
        new_model = self.Meta.model(
            **self._form_data
        )
        if commit:
            new_model.save()
        return new_model

    def quick_save(self):
        self.process()
        return self.save()


class UserForm(BaseForm):
    username: str
    email: str
    password: str

    def clean_username(self):
        try:
            models.User.objects.get(username=self._form_data['username'])
        except DoesNotExist:
            return
        raise ValidationError('Username already taken')

    def clean_email(self):
        try:
            models.User.objects.get(email=self._form_data['email'])
        except DoesNotExist:
            return
        raise ValidationError('E-mail already taken')

    def clean_password(self):
        self._form_data['password'] = auth.hash_password(self.password)

    class Meta:
        model = models.User


class GameForm(BaseForm):
    black: str
    white: str
    starting_formation: int

    def clean_black(self):
        if self._form_data['black'] == self._form_data['white']:
            raise ValidationError('Player can\'t play against himself')

        try:
            self._form_data['black'] = models.User.objects.get(
                username=self.black).pk
        except DoesNotExist:
            raise ValidationError('User for black does not exist')

    def clean_white(self):
        try:
            self._form_data['white'] = models.User.objects.get(
                username=self.white).pk
        except DoesNotExist:
            raise ValidationError('User for white does not exist')

    class Meta:
        model = models.Game
