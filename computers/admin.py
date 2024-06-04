from django import forms
from django.contrib import admin
from .models import *

class ComputerForm(forms.ModelForm):
    custom_specs = forms.CharField(
        widget=forms.Textarea,
        required=False,
        help_text="Enter specifications as key:value pairs separated by semicolons. Example: graphics_card:NVIDIA GeForce RTX 3060;color:Black;warranty:2 years"
    )

    class Meta:
        model = Computer
        fields = '__all__'
    def clean_custom_specs(self):
        data = self.cleaned_data['custom_specs']
        if data:
            specs = data.split(';')
            for spec in specs:
                if ':' not in spec:
                    raise forms.ValidationError(
                        "Each specification must be in the format key:value and separated by semicolons."
                    )
        return data

class ComputerAdmin(admin.ModelAdmin):
    form = ComputerForm

admin.site.register(Computer, ComputerAdmin)
admin.site.register(Brand)
admin.site.register(Category)
