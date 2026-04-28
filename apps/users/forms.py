from django import forms
from django.contrib.auth import authenticate
from .models import User


# Функция apply_control_style нужна для автоматического оформления полей формы
def apply_control_style(fields):
    for name, field in fields.items():
        css = 'input-control'
        field.widget.attrs.setdefault('class', css)
        field.widget.attrs.setdefault('placeholder', field.label)


# Форма LoginForm описывает поля ввода, валидацию и вид HTML-формы.
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

        # это конструктор формы
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_control_style(self.fields)

    # Метод clean проверяет данные формы/модели до сохранения.
    def clean(self):
        cleaned = super().clean()
        email = cleaned.get('email')
        password = cleaned.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Неверный email или пароль.')
            cleaned['user'] = user
        return cleaned


# Форма RegisterForm описывает поля ввода, валидацию и вид HTML-формы.
class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    # Класс Meta группирует связанную логику и настройки.
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_control_style(self.fields)

    # Функция clean_email не даёт зарегистрировать нового пользователя с email, который уже есть в базе данных
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email

    # Функция clean_username не даёт зарегистрировать нового пользователя с логином, который уже есть в базе данных
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует.')
        return username

    # Метод clean проверяет данные формы/модели до сохранения.
    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password1') != cleaned.get('password2'):
            raise forms.ValidationError('Пароли не совпадают.')
        return cleaned

    # Метод save выполняется при сохранении объекта и добавляет дополнительную подготовку данных.
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# Форма ProfileForm описывает поля ввода, валидацию и вид HTML-формы.
class ProfileForm(forms.ModelForm):
    # Класс Meta группирует связанную логику и настройки.
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'address']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_control_style(self.fields)
