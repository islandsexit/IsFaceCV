from .models import FaceToken
from django.forms import ModelForm, ImageField,TextInput


class FaceFormRegister(ModelForm):
    class Meta:
        model = FaceToken
        fields = ['face_token_ch']
        widgets = {'face_token_ch':TextInput(attrs={
            'class':'form_face',
            'placeholder':'********',
            'maxlength':'6',
            'pattern':'[0-9]*',
            'x-inputmode':'numeric',
            'oninput':'this.value=this.value.replace(/[^0-9]/,&quot;&quot;)',
            'onkeyup':"this.value = this.value.replace(/[^\d]/g,'');"

            })}


