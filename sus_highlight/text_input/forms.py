from django import forms

class TOSInputForm(forms.Form):
    terms_of_service = forms.CharField(widget=forms.Textarea(
    		attrs={
    		'class': 'form-control',
    		'rows': '25'
    		}
    	))