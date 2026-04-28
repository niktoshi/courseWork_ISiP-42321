from django import forms


# оформляет поля, чтобы все формы на сайте выглядели одинаково
def apply_control_style(fields):
    for name, field in fields.items():
        field.widget.attrs.setdefault('class', 'input-control')
        if not isinstance(field.widget, forms.Select):
            field.widget.attrs.setdefault('placeholder', field.label)


# Форма CheckoutForm описывает поля ввода, валидацию и вид HTML-формы.
class CheckoutForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=150)
    last_name = forms.CharField(label='Фамилия', max_length=150, required=False)
    phone = forms.CharField(label='Телефон', max_length=30)
    email = forms.EmailField(label='Email')
    city = forms.CharField(label='Город', max_length=150)
    address = forms.CharField(label='Адрес доставки', widget=forms.Textarea(attrs={'rows': 4}))
    payment_method = forms.ChoiceField(
        label='Способ оплаты',
        choices=[('card', 'Картой онлайн'), ('cash', 'Наличными при получении'), ('transfer', 'Переводом')],
    )
    delivery_date = forms.DateField(label='Дата доставки', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    # это конструктор формы
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_control_style(self.fields)
