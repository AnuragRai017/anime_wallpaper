# forms.py
from django import forms
from .models import Image, Category

class ImageUploadForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Image
        fields = ['title', 'image', 'categories']
