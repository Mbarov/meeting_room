from django import forms 



class CreateForm(forms.Form):
    title = forms.CharField(max_length=255,label="Название")
    description = forms.CharField(label="Описание")
    start_time = forms.DateTimeField(
        input_formats=['%d-%m-%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1',

        }))
    end_time =forms.DateTimeField(
        input_formats=['%d-%m-%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker2',

        }))



