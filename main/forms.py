from django import forms
from .models import Fertilizer, P_profile

class FertilizerForm(forms.ModelForm):
    class Meta:
        model = Fertilizer
        fields = ['name', 'no3', 'nh4', 'p2o5', 'k2o', 'cao', 'mgo', 's', 'cl', 'fe', 'mn', 'b', 'zn', 'cu', 'mo', 'co', 'si']

class P_profileForm(forms.ModelForm):
    class Meta:
        model = P_profile
        fields = ['name', 'growth_stage', 'no3', 'nh4', 'p', 'k', 'ca', 'mg', 's', 'cl', 'fe', 'mn', 'b', 'zn', 'cu', 'mo', 'co', 'si']

class UploadFileForm(forms.Form):
    file = forms.FileField(label='')