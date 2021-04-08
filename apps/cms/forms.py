from apps.forms_errors import FormErrorMixin
from django import forms

class AlbumTagsForm(forms.Form):
    pk = forms.IntegerField(error_messages={'required':'必须传入主键'})
    tag = forms.CharField(max_length=200)

class DelAlbumTagsForm(forms.Form):
    pk = forms.IntegerField(error_messages={'required':'必须有pk'})


#处理beauty
