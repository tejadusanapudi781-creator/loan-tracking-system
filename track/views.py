from django.shortcuts import render, redirect
from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone
from .models import Borrower, Loan, Collection


def dashboard(request):
    # ====== TOP CARDS ======
    total_loans = Loan.objects.aggregate(
        total=Sum('principal_amount')
    )['total'] or 0

    completed_loans = Loan.objects.filter(status='COMPLETED').count()

    total_interest = Loan.objects.aggregate(
        total=Sum('interest_amount')
    )['total'] or 0

    # ====== RECENT LOANS (LAST 5) ======
    recent_loans = Loan.objects.select_related('borrower') \
        .order_by('-id')[:5]

    # add collected & remaining amount dynamically for recent loans
    for loan in recent_loans:
        collected = Collection.objects.filter(
            loan=loan
        ).aggregate(total=Sum('amount'))['total'] or 0

        loan.collected_amount = collected
        loan.remaining_amount = loan.total_due - collected

    # ====== ALL LOANS (for sidebar / borrowers modal) ======
    all_loans = Loan.objects.select_related('borrower').order_by('-id')
    for loan in all_loans:
        collected = Collection.objects.filter(
            loan=loan
        ).aggregate(total=Sum('amount'))['total'] or 0
        loan.collected_amount = collected
        loan.remaining_amount = loan.total_due - collected

    # ====== WEEKLY COLLECTION (LAST 4 WEEKS) ======
    today = timezone.now().date()
    week_labels = []
    week_totals = []

    for i in range(4):
        start_week = today - timezone.timedelta(
            days=today.weekday() + i * 7
        )
        end_week = start_week + timezone.timedelta(days=6)

        week_labels.insert(0, f"Week {4 - i}")

        week_sum = Collection.objects.filter(
            collection_date__range=[start_week, end_week]
        ).aggregate(total=Sum('amount'))['total'] or 0

        week_totals.insert(0, float(week_sum))

    # ====== PIE CHART DATA ======
    completed_count = Loan.objects.filter(status='COMPLETED').count()
    pending_count = Loan.objects.filter(status='PENDING').count()

    total_loan_sum = float(total_loans)
    total_interest_sum = float(total_interest)

    context = {
        'total_loans': total_loans,
        'completed_loans': completed_loans,
        'total_interest': total_interest,

        # recent borrowers section
        'recent_loans': recent_loans,

        # ALL loans (pending + completed) with collected & remaining amounts
        'loans': all_loans,

        'borrowers': Borrower.objects.all(),

        'week_labels_json': week_labels,
        'week_totals_json': week_totals,

        'completed_count': completed_count,
        'pending_count': pending_count,
        'total_loan_sum': total_loan_sum,
        'total_interest_sum': total_interest_sum,
    }

    return render(request, 'dashboard.html', context)


def add_borrower(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        principal_amount = Decimal(request.POST['loan_amount'])
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        interest_amount = (
            principal_amount * Decimal('15') / Decimal('100')
        ).quantize(Decimal('0.01'))

        borrower = Borrower.objects.create(
            name=name,
            phone=phone
        )

        Loan.objects.create(
            borrower=borrower,
            principal_amount=principal_amount,
            interest_amount=interest_amount,
            start_date=start_date,
            end_date=end_date
        )

    return redirect('dashboard')


def add_collection(request):
    if request.method == 'POST':
        loan_id = request.POST['loan_id']
        amount = Decimal(request.POST['amount'])
        collection_date = request.POST['collection_date']

        loan = Loan.objects.get(id=loan_id)

        Collection.objects.create(
            loan=loan,
            amount=amount,
            collection_date=collection_date
        )

        loan.total_due -= amount
        if loan.total_due <= 0:
            loan.status = 'COMPLETED'

        loan.save()

    return redirect('dashboard')

