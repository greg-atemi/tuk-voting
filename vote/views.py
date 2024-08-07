from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from vote.models import Candidate, Election, Voter
from KuraProject import settings
from vote.tokens import generate_token


def index(request):
    if request.user.is_authenticated and request.user.is_active:
        fname = request.user.first_name
        context = {
            'fname': fname
        }
    else:
        fname = ''
        context = {
            'fname': fname
        }
    return render(request, 'vote/user/index.html', context)


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists!!")
            return redirect('vote:signup')

        if User.objects.filter(email=email):
            messages.error(request, "Email already exists!!")
            return redirect('vote:signup')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('vote:signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = True

        myuser.save()

        messages.success(request, "Your Account has been created successfully. \n ")

        return redirect('vote:login')

    return render(request, 'vote/auth/signup.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            auth_login(request, user)
            return redirect('vote:dashboard')

        else:
            messages.error(request, "Username or Password is incorrect")
            return redirect('vote:admin_login')

    return render(request, 'vote/auth/login_admin.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login Successful.")
            return redirect('vote:index')

        else:
            messages.error(request, "Username or Password is incorrect")

    return render(request, 'vote/auth/login.html')


def admin_log_out(request):
    logout(request)
    return render(request, 'vote/admin/admin_logout.html')


def log_out(request):
    logout(request)
    return render(request, 'vote/auth/logout.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        return redirect('vote:login')
    else:
        return render(request, 'vote/auth/activation_failed.html')


def activation_failed(request):
    return render(request, 'vote/auth/activation_failed.html')


def dashboard(request):
    if request.user.is_authenticated and request.user.is_staff:
        total = Voter.objects.count()
        threshold = (total / 10) * 100
        fname = request.user.first_name
        lname = request.user.last_name
        context = {
            'fname': fname,
            'lname': lname,
            'total': total,
            'threshold': threshold
        }
    else:
        messages.info(request, "Admin privileges required")
        return redirect('vote:admin_login')

    return render(request, 'vote/admin/dashboard.html', context)


@login_required
def user_account(request):
    uname = request.user.username
    fname = request.user.first_name
    lname = request.user.last_name
    email = request.user.email

    context = {
        'uname': uname,
        'fname': fname,
        'lname': lname,
        'email': email
    }

    return render(request, 'vote/user/user_account.html', context)


def admin_account(request):
    if request.user.is_authenticated and request.user.is_staff:
        uname = request.user.username
        fname = request.user.first_name
        lname = request.user.last_name
        email = request.user.email
        context = {
            'uname': uname,
            'fname': fname,
            'lname': lname,
            'email': email
        }
    else:
        messages.info(request, "Login to continue")
        return redirect('vote:admin_login')

    return render(request, 'vote/admin/admin_account.html', context)


@login_required
def bio(request):
    elections = Election.objects.all()
    fname = request.user.first_name
    if Voter.objects.filter(user=request.user.id):
        messages.error(request, "You are already registered as a voter!!")
        return redirect('vote:index')

    if request.method == "POST":
        registration_number = request.POST['registration_number']
        user = request.user
        election_id = request.POST['election']
        first_name = request.POST['first_name']
        surname = request.POST['surname']
        phone_number = request.POST['phone_number']
        gender = request.POST['gender']
        email = request.user.email

        try:
            election = Election.objects.get(id=election_id)
        except Election.DoesNotExist:
            messages.error(request, "Selected election does not exist.")
            return redirect('vote:bio')

        myvoter = Voter.objects.create( registration_number=registration_number, user=user, election=election, email=email,
                                        first_name=first_name, surname=surname,phone_number=phone_number, gender=gender)

        myvoter.save()
        
        return redirect('vote:confirmation', registration_number)
    
    context = {
        'elections': elections,
        'fname': fname
    }

    return render(request, 'vote/user/bio.html', context)


@login_required
def confirmation(request, registration_number):
    elections = Election.objects.all()
    fname = request.user.first_name
    voter = Voter.objects.get(registration_number=registration_number)
    context = {
        'fname': fname,
        'voter': voter,
        'elections': elections
    }
    if request.method == "POST":
        registration_number = request.POST['registration_number']
        user = request.user
        election_id = request.POST['election']
        first_name = request.POST['first_name']
        surname = request.POST['surname']
        phone_number = request.POST['phone_number']
        gender = voter.gender
        email = request.user.email

        try:
            election = Election.objects.get(id=election_id)
        except Election.DoesNotExist:
            messages.error(request, "Selected election does not exist.")
            return redirect('vote:bio')

        my_voter = Voter(registration_number=registration_number, user=user, election=election, first_name=first_name,
                         surname=surname, email=email, phone_number=phone_number, gender=gender)

        my_voter.save()

        return redirect('vote:success')
        
    return render(request, 'vote/user/confirmation.html', context)


@login_required
def success(request):
    if request.user.is_authenticated:
        fname = request.user.first_name
        context = {
            'fname': fname
        }

    return render(request, 'vote/user/success.html', context)


@login_required
def success_vote(request):
    if request.user.is_authenticated:
        fname = request.user.first_name
        context = {
            'fname': fname
        }

    return render(request, 'vote/user/success_vote.html', context)


def create_voter(request):
    if request.user.is_authenticated and request.user.is_staff:
        fname = request.user.first_name
        lname = request.user.last_name
        context = {
            'fname': fname,
            'lname': lname
        }
        if request.method == "POST":
            registration_number = request.POST['registration_number']
            email = request.user.id
            first_name = request.POST['first_name']
            surname = request.POST['surname']
            phone_number = request.POST['phone_number']
            gender = request.POST['gender']

            myvoter = Voter.objects.create(registration_number=registration_number,
                                           email_id=email, first_name=first_name,
                                           surname=surname, phone_number=phone_number,
                                           gender=gender)

            myvoter.save()

            messages.success(request, "Voter added successfully.")

            return redirect('vote:voter_list')
    else:
        messages.info(request, "Login to continue")
        return redirect('vote:login')

    return render(request, 'vote/admin/create_voter.html', context)


@login_required
def create_candidate(request):
    if request.user.is_staff:
        fname = request.user.first_name
        lname = request.user.last_name
        elections = Election.objects.all()
        context = {
            'fname': fname,
            'lname': lname,
            'election_list' : elections
        }

        if request.method == "POST":
            election_id = request.POST['election']
            registration_number = request.POST['registration_number']
            first_name = request.POST['first_name']
            surname = request.POST['surname']
            email = request.POST['email']
            phone_number = request.POST['phone_number']
            gender = request.POST['gender']

            try:
                election = Election.objects.get(id=election_id)
            except Election.DoesNotExist:
                messages.error(request, "Selected election does not exist.")
                return redirect('vote:bio')


            mycandidate = Candidate.objects.create( registration_number=registration_number, first_name=first_name, email=email,
                                                    election=election, surname=surname, phone_number=phone_number, gender=gender)

            mycandidate.save()

            messages.success(request, "Voter added successfully.")

            return redirect('vote:candidate_list')
    else:
        messages.info(request, "Login to continue")
        return redirect('vote:login')

    return render(request, 'vote/admin/create_candidate.html', context)


@login_required
def create_election(request):
    if request.user.is_staff:
        fname = request.user.first_name
        lname = request.user.last_name
        context = {
            'fname': fname,
            'lname': lname
        }
        if request.method == "POST":
            election_name = request.POST['election_name']

            myelection = Election.objects.create(election_name=election_name)

            myelection.save()

            messages.success(request, "Election added successfully.")

            return redirect('vote:election_list')
    else:
        messages.info(request, "Login to continue")
        return redirect('vote:login')

    return render(request, 'vote/admin/create_election.html', context)


def voter_list(request):
    if request.user.is_authenticated and request.user.is_staff:
        fname = request.user.first_name
        lname = request.user.last_name
        voter = Voter.objects.all()
        user = User.objects.all()
        context = {
            'voter': voter,
            'user': user,
            'fname': fname,
            'lname': lname
        }
    else:
        messages.info(request, "Login to continue")
        return redirect('vote:login')

    return render(request, 'vote/admin/voter_list.html', context)


def election_list(request):
    if request.user.is_authenticated and request.user.is_staff:
        fname = request.user.first_name
        lname = request.user.last_name
        elections = Election.objects.all()
        user = User.objects.all()
        context = {
            'election_list': elections,
            'user': user,
            'fname': fname,
            'lname': lname
        }
    else:
        messages.info(request, "Login to continue")
        return redirect('vote:login')

    return render(request, 'vote/admin/election_list.html', context)


def candidate_list(request):
    if request.user.is_authenticated and request.user.is_staff:
        fname = request.user.first_name
        lname = request.user.last_name
        user = User.objects.all()
        elections = Election.objects.all()
        selected_election = request.GET.get('selected_election')

        sort_by = request.GET.get('sort_by', 'votes')
        order = request.GET.get('order', 'desc')

        if order == 'desc':
            sort_by = '-' + sort_by
        
        if selected_election:
            candidate = Candidate.objects.filter(election_id=selected_election).order_by(sort_by)
        else:
            candidate = Candidate.objects.all().order_by(sort_by)
        
        context = {
            'candidate_list': candidate,
            'election_list': elections,
            'selected_election': selected_election,
            'user': user,
            'fname': fname,
            'lname': lname
        }
    else:
        messages.info(request, "Login to continue")
        return redirect('vote:login')

    return render(request, 'vote/admin/candidate_list.html', context)


def check_details_auth(request):
    if request.user.is_authenticated:
        fname = request.user.first_name

        context = {
            'fname': fname
        }

        if request.method == "POST":

            registration_number = request.POST['registration_number']
            try:
                voter = Voter.objects.select_related('user__voter').get(registration_number=registration_number)
            except Voter.DoesNotExist:
                messages.error(request, "Invalid details, please try again")
                return redirect('vote:check_details_auth')

            email2 = voter.user.email
            email3 = request.user.email

            if email2 == email3:
                return redirect('vote:voter_details', registration_number)

            else:
                messages.error(request, "Invalid details, please try again")
                return redirect('vote:check_details_auth')
    else:
        messages.info(request, "Login to continue")
        return redirect('vote:login')

    return render(request, 'vote/user/check_details_auth.html', context)


@login_required
def cast_vote_auth(request):
    fname = request.user.first_name
    context = {
        'fname': fname
    }

    if request.method == "POST":
        registration_number = request.POST['registration_number']
        try:
            voter = Voter.objects.select_related('user__voter').get(registration_number=registration_number)
        except Voter.DoesNotExist:
            messages.error(request, "Invalid details, please try again")
            return redirect('vote:cast_vote_auth')

        email2 = voter.user.email
        email3 = request.user.email
        election = voter.election.id
        status = voter.status
        
        if email2 != email3:
            messages.error(request, "Invalid details, please try again")
            return redirect('vote:cast_vote_auth')
        elif status == True:
            messages.error(request, "You cannot vote twice!!")
            return redirect('vote:index')
        else:
            return redirect('vote:cast_vote', election)          
        
    return render(request, 'vote/user/cast_vote_auth.html', context)


@login_required
def cast_vote(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    
    try:
        voter = request.user.voter
    except Voter.DoesNotExist:
        messages.error(request, "You are not registered as a voter for this election.")
        return redirect('vote:index')

    if request.method == "POST":
        try:
            id = request.POST["candidate"]
            selected_candidate = election.candidate_set.get(pk=id)
        except (KeyError, Candidate.DoesNotExist):
            # Redisplay the election voting form with an error message
            messages.error(request, "You didn't select a valid candidate.")
            return render(request, 'vote/user/cast_vote.html', {"election": election})

        # Increment the vote count for the selected candidate
        selected_candidate.votes += 1
        selected_candidate.save()

        # Mark the voter as having voted
        voter.status = True
        voter.save()

        # Redirect to the results page or any other page after voting
        return redirect('vote:success_vote')

    # If not a POST request, render the voting form
    return render(request, 'vote/user/cast_vote.html', {"election": election})


def voter_details(request, registration_number):
    if request.user.is_authenticated:
        fname = request.user.first_name
        voter = Voter.objects.select_related('user__voter').get(registration_number=registration_number)
        myvoter = voter.gender
        context = {
            'fname': fname,
            'voter': voter,
            'myvoter': myvoter
        }

    else:
        messages.info(request, "Login to continue")
        return redirect('vote:login')

    return render(request, 'vote/user/check_details.html', context)


def update_details_auth(request):
    if request.user.is_authenticated:
        fname = request.user.first_name

        context = {
            'fname': fname
        }

        if request.method == "POST":

            registration_number = request.POST['registration_number']
            try:
                voter = Voter.objects.select_related('user__voter').get(registration_number=registration_number)
            except Voter.DoesNotExist:
                messages.error(request, "Invalid details, please try again")
                return redirect('vote:update_details_auth')

            email2 = voter.user.email
            email3 = request.user.email

            if email2 == email3:
                return redirect('vote:update_details', registration_number)

            else:
                messages.error(request, "Invalid details, please try again")
                return redirect('vote:update_details_auth')
    else:
        messages.info(request, "Login to continue")
        return redirect('vote:login')

    return render(request, 'vote/user/update_details_auth.html', context)


def update_details(request, registration_number):
    if request.user.is_authenticated:
        fname = request.user.first_name
        voter = Voter.objects.get(registration_number=registration_number)
        context = {
            'fname': fname,
            'voter': voter
        }
        if request.method == "POST":
            registration_number = voter.registration_number
            election = voter.election
            user = request.user
            first_name = voter.first_name
            surname = voter.surname
            phone_number = request.POST['phone_number']
            email = request.POST['email']
            gender = voter.gender

            my_voter = Voter(election=election, registration_number=registration_number, user=user, email=email,
                             first_name=first_name, surname=surname, phone_number=phone_number, gender=gender)

            my_voter.save()

            return redirect('vote:success')

    else:
        messages.info(request, "Login to continue")
        return redirect('vote:login')

    return render(request, 'vote/user/update_details.html', context)