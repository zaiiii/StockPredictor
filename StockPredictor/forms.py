from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import URLValidator

class NextDayPredictionForm(forms.ModelForm):
    stock = (
        ('aapl', 'Apple'),
        ('sch', 'Whtevs'),
        ('ssc', 'shdjka'),
        ('hsc', 'umm'),
        ('grad', 'Lekha'),
        ('postgrad', 'Sharmaji'),
    )
    company = forms.ChoiceField(choices = stock)

# class GraphPredictionForm(forms.ModelForm):
#     stock = (
#         ('aapl', 'Apple'),
#         ('sch', 'Whtevs'),
#         ('ssc', 'shdjka'),
#         ('hsc', 'umm'),
#         ('grad', 'Lekha'),
#         ('postgrad', 'Sharmaji'),
#     )
#     company = forms.ChoiceField(choices = stock)
#     date = forms.DateField(widget=AdminDateWidget)

class GraphPredictionForm(forms.Form):
    stock = (
                ('aapl', 'Apple'),
                ('sch', 'Whtevs'),
                ('ssc', 'shdjka'),
                ('hsc', 'umm'),
                ('grad', 'Lekha'),
                ('postgrad', 'Sharmaji'),
            )
    company = forms.ChoiceField(choices = stock)
    holiday_date = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))

