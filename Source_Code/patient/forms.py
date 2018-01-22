from django.forms import ModelForm

from module.models import Patient


class PatientForm(ModelForm):
    # doctor = forms.ModelChoiceField(queryset=User.objects.filter(groups__name="Doctors"))
    # date = forms.DateField(widget=forms.TextInput(attrs={'class': 'datetime-input'}))
    class Meta:
        model = Patient
        fields = "__all__"