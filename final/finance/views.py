from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import IntegrityError
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.core.paginator import Paginator
from datetime import datetime, timedelta

from .models import User, Record, Planned
import json

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dashboard"))    
    else:
        return HttpResponseRedirect(reverse("welcome"))

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if not username or not password:
            return render(request, "finance/login.html", {
                "message": "Incomplete fields. Please try again."
            })

        user = authenticate(request, username=username, password=password)

        if user is not None :
            login(request, user)
            
            current_date = datetime.now().date()
            planneds = Planned.objects.filter(user=user)

            for planned in planneds:
                if planned.date == current_date:
                    time = datetime.now()

                    new_record = Record(
                        user = user,
                        record_type = planned.planned_type,
                        category = 0,
                        amount = planned.amount,
                        comment = f"{Planned.FREQUENCY_CHOICES[planned.frequency-1][1]} Payment for {planned.name}",
                        time = time
                    )

                    new_record.save()
                    
                    if planned.frequency == 1:
                        planned.delete()

                    elif planned.frequency == 2:
                        if planned.recurrence == 1:
                            planned.date = current_date + timedelta(days=1)
                            planned.save()
                        elif planned.recurrence == 2:
                            planned.date = current_date + timedelta(days=7)
                            planned.save()
                        elif planned.recurrence == 3:
                            planned.date = current_date + relativedelta(months=1)
                            planned.save()
                        elif planned.recurrence == 4:
                            planned.date = current_date + relativedelta(years=1)
                            planned.save()

            return HttpResponseRedirect(reverse("dashboard"))

        elif user is None:
            return render(request, "finance/login.html", {
                "message": "Incorrect username or password. Please try again."
            })

        else:
            return render(request, "finance/login.html", {
                "message": "An unknown error occured. Please try again."
            })

    else:
        try:
            # Try and retrieve message if any
            message = request.session.get("message")
            success = request.session.get("success")

            # Delete message from request.session to only show it once 
            del request.session["message"]
            del request.session["success"]

            return render(request, "finance/login.html", {
                "message": message,
                "success": success
            })

        except:
            return render(request, "finance/login.html")

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if not username or not password or not confirmation:
            return render(request, "finance/register.html", {
                "message": "Incomplete fields. Please try again."
            })

        if password != confirmation:
            return render(request, "finance/register.html", {
                "message": "Passwords do not match. Please try again."
            })

        try:
            user = User.objects.create_user(username, "", password)
            user.save()

            # Save context as session variable to retrieve later
            # This is because HttpResponseRedirect does not support passing context data
            request.session["message"] = "Account created successfully. Please attempt to login now."
            request.session["success"] = True

            return HttpResponseRedirect(reverse("login"))

        except IntegrityError:
            return render(request, "finance/register.html", {
                "message": "Username already taken. Please try again."
            })

        except Exception as e:
            return render(request, "finance/register.html", {
                "message": e
            })

    else:
        return render(request, "finance/register.html")


def welcome(request):
    return render(request, "finance/welcome.html")

@login_required
def dashboard(request):
    user = request.user

    current_date = datetime.now().date()
    past_seven_days = current_date - timedelta(days=6)
    past_thirty_days = current_date - timedelta(days=29)
    
    past_7_income = Record.objects.filter(user=user, record_type=1, time__range=(past_seven_days, current_date + timedelta(days=1)))
    past_7_expense = Record.objects.filter(user=user, record_type=2, time__range=(past_seven_days, current_date + timedelta(days=1)))
    past_30_expense = Record.objects.filter(user=user, record_type=2, time__range=(past_thirty_days, current_date + timedelta(days=1)))
    
    # Determining average income and expense (past 7 days) for HTML card
    past_7_total_income = 0
    past_7_total_expense = 0

    for record in past_7_income:
        past_7_total_income += record.amount
    
    for record in past_7_expense:
        past_7_total_expense -= record.amount

    past_7_average_expense = round(past_7_total_expense / 7, 2)

    # Making a dictionary for line chart data
    line_data = {}

    for i in range(30):
        date = current_date - timedelta(days=(29-i))
        line_data[date] = 0

    for record in past_30_expense:
        if record.record_type == 2:
            line_data[record.time.date()] -= record.amount

    # Making a dictionary for pie chart data
    pie_data = {}

    for record in Record.objects.filter(user=user):
        category = Record.CATEGORY_CHOICES[record.category-1][1]

        if record.record_type == 2:
            if category not in pie_data:
                pie_data[category] = -(record.amount)
            else:
                pie_data[category] += -(record.amount)

    return render(request, "finance/dashboard.html", {
        "records": Record.objects.filter(user=user).order_by("-time")[:10],
        "categories": Record.CATEGORY_CHOICES,
        "past_7_total_income": past_7_total_income,
        "past_7_total_expense": past_7_total_expense,
        "past_7_average_expense": past_7_average_expense,
        "pie_data": pie_data,
        "line_data": line_data,
    })

@login_required
def records(request):
    user = request.user

    user_records = Record.objects.filter(user=user).order_by("-time")
    paginator = Paginator(user_records, 10)

    page_number = request.GET.get('page')
    records = paginator.get_page(page_number)

    planneds = Planned.objects.filter(user=user).order_by("date")

    if request.method == "POST":
        record_type = request.POST["record_type"]
        category = request.POST.get("category", False)
        amount = request.POST["amount"]
        comment = request.POST["comment"]
        time = datetime.now()

        if not record_type or not category or not amount:
            return render(request, "finance/records.html", {
                "message": "Incomplete fields. Please try again.",
                "types": Record.TYPE_CHOICES,
                "categories": Record.CATEGORY_CHOICES,
                "frequency": Planned.FREQUENCY_CHOICES,
                "recurrences": Planned.RECURRENCE_CHOICES,
                "records": records,
                "planneds": planneds
            })

        try: 
            record_type = int(record_type)
            category = int(category)

            if record_type == 1:
                amount = float(amount)
            else: 
                amount = -(float(amount))
                
            if amount == 0:
                return render(request, "finance/records.html", {
                    "message": "Amount cannot be 0. Please try again.",
                    "types": Record.TYPE_CHOICES,
                    "categories": Record.CATEGORY_CHOICES,
                    "frequency": Planned.FREQUENCY_CHOICES,
                    "recurrences": Planned.RECURRENCE_CHOICES,
                    "records": records,
                    "planneds": planneds
                })     

            if category == 0:
                return render(request, "finance/records.html", {
                    "message": "Category cannot be a planned payment. Please try again.",
                    "types": Record.TYPE_CHOICES,
                    "categories": Record.CATEGORY_CHOICES,
                    "frequency": Planned.FREQUENCY_CHOICES,
                    "recurrences": Planned.RECURRENCE_CHOICES,
                    "records": records,
                    "planneds": planneds
                })     


            new_record = Record(
                user = user,
                record_type = record_type,
                category = category,
                amount = amount,
                comment = comment,
                time = time
            )
            new_record.save()

            return HttpResponseRedirect(reverse("records"))

        except:
            return render(request, "finance/records.html", {
                "message": "An unknown error occured. Please try again.",
                "types": Record.TYPE_CHOICES,
                "categories": Record.CATEGORY_CHOICES,
                "frequency": Planned.FREQUENCY_CHOICES,
                "recurrences": Planned.RECURRENCE_CHOICES,
                "records": records,
                "planneds": planneds
            })

    else:
        return render(request, "finance/records.html", {
            "types": Record.TYPE_CHOICES,
            "categories": Record.CATEGORY_CHOICES,
            "frequency": Planned.FREQUENCY_CHOICES,
            "recurrences": Planned.RECURRENCE_CHOICES,
            "records": records,
            "planneds": planneds
        })

@login_required
def planned(request):
    user = request.user

    user_records = Record.objects.filter(user=user).order_by("-time")
    paginator = Paginator(user_records, 10)

    page_number = request.GET.get('page')
    records = paginator.get_page(page_number)

    planneds = Planned.objects.filter(user=user).order_by("date")

    if request.method == "POST":
        name = request.POST["name"]
        planned_type = request.POST["planned_type"]
        frequency = request.POST["frequency"]
        recurrence = request.POST.get("recurrence", False)
        amount = request.POST["amount"]
        date = request.POST["date"]

        if not name or not planned_type or not frequency or not amount or not date or ((int(frequency) == 2) and not recurrence):
            return render(request, "finance/records.html", {
                "message": "Incomplete fields. Please try again.",
                "types": Record.TYPE_CHOICES,
                "categories": Record.CATEGORY_CHOICES,
                "frequency": Planned.FREQUENCY_CHOICES,
                "recurrences": Planned.RECURRENCE_CHOICES,
                "records": records,
                "planneds": planneds
            })

        try:
            planned_type = int(planned_type)
            frequency = int(frequency)
            recurrence = int(recurrence)
            date = datetime.strptime(date, "%Y-%m-%d").date()
            current_date = datetime.now().date()

            if planned_type == 1:
                amount = float(amount)
            else: 
                amount = -(float(amount))
                
            if amount == 0:
                return render(request, "finance/records.html", {
                    "message": "Amount cannot be 0. Please try again.",
                    "types": Record.TYPE_CHOICES,
                    "categories": Record.CATEGORY_CHOICES,
                    "frequency": Planned.FREQUENCY_CHOICES,
                    "recurrences": Planned.RECURRENCE_CHOICES,
                    "records": records,
                    "planneds": planneds
                })                
            
            if date <= current_date:
                return render(request, "finance/records.html", {
                    "message": "Date must be in the future. Please try again.",
                    "types": Record.TYPE_CHOICES,
                    "categories": Record.CATEGORY_CHOICES,
                    "frequency": Planned.FREQUENCY_CHOICES,
                    "recurrences": Planned.RECURRENCE_CHOICES,
                    "records": records,
                    "planneds": planneds
                })          


            if frequency == 2:
                new_planned = Planned(
                    user = user,
                    planned_type = planned_type,
                    frequency = frequency,
                    recurrence = recurrence,
                    name = name,
                    amount = amount,
                    date = date
                )
            
            else:
                new_planned = Planned(
                    user = user,
                    planned_type = planned_type,
                    frequency = frequency,
                    name = name,
                    amount = amount,
                    date = date
                )

            new_planned.save()

            return render(request, "finance/records.html", {
                "types": Record.TYPE_CHOICES,
                "categories": Record.CATEGORY_CHOICES,
                "frequency": Planned.FREQUENCY_CHOICES,
                "recurrences": Planned.RECURRENCE_CHOICES,                
                "records": records,
                "planneds": planneds
            })     

        except: 
            return render(request, "finance/records.html", {
                "message": "An unknown error occured. Please try again.",
                "types": Record.TYPE_CHOICES,
                "categories": Record.CATEGORY_CHOICES,
                "frequency": Planned.FREQUENCY_CHOICES,
                "recurrences": Planned.RECURRENCE_CHOICES,
                "records": records,
                "planneds": planneds
            })

    else:
        return HttpResponseRedirect(reverse("records"))

@login_required
def delete(request, id):
    if request.method == "POST":
        origin_url = request.POST["origin_url"]
        
        if origin_url == "dashboard" or origin_url == "records":
            record = Record.objects.get(id=id)
            record.delete()
        elif origin_url == "planned": 
            record = Planned.objects.get(id=id)
            record.delete()

        if origin_url == "dashboard":
            return HttpResponseRedirect(reverse("dashboard"))
        
        elif origin_url == "records":
            return HttpResponseRedirect(reverse("records"))

        elif origin_url == "planned":
            return HttpResponseRedirect(reverse("records"))

    else:
        return HttpResponseRedirect(reverse("dashboard"))