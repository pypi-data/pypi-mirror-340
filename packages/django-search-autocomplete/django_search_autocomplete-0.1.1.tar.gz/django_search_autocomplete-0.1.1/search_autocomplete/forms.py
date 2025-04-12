from django import forms
from django.apps import apps
from django.db import models

class SearchConfigForm(forms.Form):
    model = forms.ChoiceField(
        choices=[],
        label="Select Model",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    search_fields = forms.MultipleChoiceField(
        choices=[],
        label="Search Fields",
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    display_fields = forms.MultipleChoiceField(
        choices=[],
        label="Display Fields",
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    max_results = forms.IntegerField(
        initial=5,
        min_value=1,
        max_value=20,
        label="Maximum Results",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get all installed models
        model_choices = []
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                model_label = f"{model._meta.app_label}.{model._meta.model_name}"
                model_name = model._meta.verbose_name.title()
                model_choices.append((model_label, f"{model_name} ({app_config.verbose_name})"))
        
        self.fields['model'].choices = sorted(model_choices)

    def get_model_fields(self, model_label):
        app_label, model_name = model_label.split('.')
        model = apps.get_model(app_label, model_name)
        fields = []
        
        for field in model._meta.get_fields():
            # Skip many-to-many and reverse relations
            if isinstance(field, (models.ManyToManyRel, models.ManyToOneRel)):
                continue
                
            field_name = field.name
            field_type = field.get_internal_type()
            
            # For ForeignKey fields, add both the ID and string representation
            if isinstance(field, models.ForeignKey):
                fields.append((field_name, f"{field.verbose_name} (ID)"))
                fields.append((f"{field_name}__str", f"{field.verbose_name} (String)"))
            else:
                fields.append((field_name, f"{field.verbose_name} ({field_type})"))
        
        return sorted(fields) 