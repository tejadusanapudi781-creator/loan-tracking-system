from django import forms
from .models import Borrower, Loan, Collection

class BorrowerForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = ['name', 'phone']  # add other fields if you have

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['borrower', 'amount', 'loan_date', 'completion_date']

        widgets = {
            'loan_date': forms.DateInput(attrs={'type': 'date'}),
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['loan', 'amount', 'collection_date']

        widgets = {
            'collection_date': forms.DateInput(attrs={'type': 'date'}),
        }





