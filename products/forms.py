from django import forms


class ProductUploadForm(forms.Form):
    file = forms.FileField(label='Excel file (.xlsx)')

    def clean_file(self):
        upload = self.cleaned_data['file']
        if not upload.name.lower().endswith('.xlsx'):
            raise forms.ValidationError('Only .xlsx files are supported.')
        return upload


class ApprovedFilterForm(forms.Form):
    q = forms.CharField(required=False, label='Search (name/category)')
    start_date = forms.DateField(
        required=False,
        label='Updated from',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    end_date = forms.DateField(
        required=False,
        label='Updated to',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    per_page = forms.ChoiceField(
        required=False,
        label='Rows per page',
        choices=[('5', '5'), ('10', '10'), ('25', '25'), ('50', '50'), ('100', '100')],
        initial='10',
    )
