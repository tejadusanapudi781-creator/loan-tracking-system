from django.contrib import admin
from .models import Borrower, Loan, Collection

@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    search_fields = ('name', 'phone')


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('borrower', 'principal_amount', 'interest_amount', 'total_due', 'start_date', 'end_date', 'status')
    list_filter = ('status',)
    search_fields = ('borrower__name',)
    readonly_fields = ('total_due',)  # Total due is auto-calculated


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('loan', 'amount', 'collection_date')
    search_fields = ('loan__borrower__name',)
    list_filter = ('collection_date',)

