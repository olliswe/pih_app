from django.db import models
from accounts.models import User
from django.db.models import Q

class ExpenseQueryset(models.QuerySet):
    def need_organizing(self):
        return self.filter(organized_by_us = True, is_organized = False, request_form__status = 'approved')

    def outstanding(self):
        return self.filter(Q(expenses_covered_by = 'Covered by us but reimbursed')\
                                          | Q(expenses_covered_by = 'Covered by us (not reimbursed)'), \
                                          expense_paid = False)

    def need_reimbursement(self):
        return self.filter(expenses_covered_by = 'Covered by us but reimbursed',expense_paid = True,
                                          expense_reimbursed=False)

class ExpenseManager(models.Manager):
    def get_queryset(self):
        return ExpenseQueryset(self.model, using=self._db)

    def need_organizing(self):
        return self.get_queryset().need_organizing()

    def outstanding(self):
        return self.get_queryset().outstanding()

    def need_reimbursement(self):
        return self.get_queryset().need_reimbursement()




class Request(models.Model):
    DEPARTURE_CHOICES = [
        ('PIH Haiti','PIH Haiti'),
        ('PIH Kazakhstan','PIH Kazakhstan'),
        ('PIH Lesotho','PIH Lesotho'),
        ('PIH Liberia','PIH Liberia'),
        ('PIH Malawi','PIH Malawi'),
        ('PIH Mexico','PIH Mexico'),
        ('PIH Navajo','PIH Navajo'),
        ('PIH Peru','PIH Peru'),
        ('PIH Rwanda','PIH Rwanda'),
        ('PIH Sierra Leone','PIH Sierra Leone'),
        ('other','Other')
    ]
    STATUS_CHOICES = [
        ('review','Under Review'),
        ('approved','Approved'),
        ('rejected','Rejected')
    ]
    host = models.ForeignKey(User, on_delete='SET_DEFAULT',default=None, null=True, blank=True, verbose_name="Requestor/Host")
    departure_place = models.CharField(max_length=225, verbose_name="Place of Departure", choices=DEPARTURE_CHOICES)
    other_place = models.CharField(max_length=225, verbose_name="Other Place of Departure (please specify)", null=True, blank=True)
    purpose = models.TextField(max_length=1000, verbose_name="Purpose of Visit")
    arrival_date = models.DateField(verbose_name="Arrival Date")
    departure_date = models.DateField(verbose_name="Departure Date")
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name="Submitted on")
    num_visitors = models.IntegerField(verbose_name='Number of Visitors')
    review_comment = models.TextField(max_length=1000, verbose_name="Review comment", null=True, blank=True)
    status = models.CharField(max_length=225, choices = STATUS_CHOICES, default='review' )
    reviewer = models.ForeignKey(User, related_name="reviewer_user", on_delete='SET_DEFAULT', default=None, null=True, blank=True)
    review_date = models.DateField(verbose_name="Reviewed on", null=True, blank=True)

    def get_status(self):
        return dict(Request.STATUS_CHOICES)[self.status]




    def get_organized_counter(self):
        counter = [0,0]

        for expense in self.expense_set.all():
            if expense.organized_by_us == True :
                counter[1] += 1
                if expense.is_organized == True:
                    counter[0] += 1

        return counter


    def organization_status(self):
        counter = self.get_organized_counter()
        if counter[0]==counter[1]:
            return 'completed'

        elif counter[0]!=0:
            return 'partial'

        else:
            return 'not_completed'





    def get_reimbursement_counter(self):
        counter = [0, 0]

        for expense in self.expense_set.all():
            if expense.expenses_covered_by=="Covered by us but reimbursed" :
                counter[1] += 1
                if expense.expense_reimbursed == True:
                    counter[0] += 1

        return counter



    def reimbursement_status(self):
        counter = self.get_reimbursement_counter()
        if counter[0] == counter[1]:
            return 'completed'

        elif counter[0] != 0:
            return 'partial'

        else:
            return 'not_completed'



    def is_archived(self):
        if self.status == "review":
            return False

        elif self.organization_status()=='completed' and self.reimbursement_status()=='completed' and self.status == 'approved':
            return True

        elif self.status == 'rejected':
            return True

        return False


    def print_names_of_visitors(self):
        visitors = ''
        count = 1
        for visitor in self.visitor_set.all():
            if count > 3:
                visitors += ', +' + str(self.num_visitors - (count - 1)) + " more"
                break
            elif count == 1:
                visitors += visitor.name
                count += 1
            else:
                visitors += ', ' + visitor.name
                count += 1
        return visitors

    class Meta:
        ordering = ['arrival_date']




class Expense (models.Model):
    TYPE_CHOICES = [
        ('Flights','Flights'),
        ('Visa','Visa'),
        ('Accommodation','Accommodation'),
        ('Transport','Transport'),
        ('Seacoach','Seacoach'),
        ('Other','Other')
    ]
    EXPENSES_CHOICES = [
        ('Entirely by visitor','Entirely by visitor'),
        ('Covered by us but reimbursed','Covered by us but reimbursed'),
        ('Covered by us (not reimbursed)','Covered by us (not reimbursed)')
    ]
    type = models.CharField(max_length=225, choices=TYPE_CHOICES)
    organized_by_us = models.BooleanField(default=False, verbose_name="Organized by us?")
    name_of_organizer = models.ForeignKey(User, on_delete='SET_DEFAULT',
                                          default=None, null=True, blank=True, verbose_name="Name of Organizer")
    expenses_covered_by = models.CharField(max_length=225, choices = EXPENSES_CHOICES,
                                           verbose_name="Expenses covered by")
    expenses_amount = models.FloatField(verbose_name="Estimated expenses amount in USD", null=True, blank='True')
    notes = models.TextField(max_length=225,verbose_name='Additional Notes', null=True, blank=True)
    request_form = models.ForeignKey(Request, verbose_name="Request", on_delete='CASCADE',)

    is_organized = models.BooleanField(default=False, verbose_name="Has been organized")
    marked_as_organized_by = models.ForeignKey(User, related_name="marked_as_organized_by", verbose_name="Marked as organized by",
                                          on_delete='SET_DEFAULT', default=None, null=True, blank=True)
    marked_as_organized_on = models.DateField(verbose_name="Marked as organized on", null=True, blank=True)

    expense_reimbursed = models.BooleanField(default=False, verbose_name="Expense has been reimbursed")
    marked_as_reimbursed_by = models.ForeignKey(User, related_name="marked_as_reimbursed_by", verbose_name="Marked as reimbursed by",
                                          on_delete='SET_DEFAULT', default=None, null=True, blank=True)
    marked_as_reimbursed_on = models.DateField(verbose_name="Marked as reimbursed on", null=True, blank=True)
    amount_reimbursed = models.FloatField(verbose_name="Amount reimbursed", default=None, null=True, blank=True)

    objects = models.Manager()
    manager = ExpenseManager()




    def needs_to_be_organized(self):
        if self.organized_by_us == True and self.is_organized == False and self.request_form.is_approved == True:
            return True
        else:
            return False



    def __str__(self):
        return dict(Expense.TYPE_CHOICES)[self.type]



class Visitor(models.Model):
    name = models.CharField(max_length=500, verbose_name="Full name of Visitor")
    request_form = models.ForeignKey(Request, verbose_name="Request", on_delete='CASCADE')


