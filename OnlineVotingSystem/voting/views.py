from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Candidate, Vote
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404

# from django.contrib.auth.decorators import login_required, user_passes_test

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already in use'})

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)  # auto login after registration
        return redirect('dashboard')

    return render(request, 'register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})


def home(request):
    return render(request,"home.html",)


@login_required
def vote_view(request):
    user = request.user

    # Check if user already voted
    if Vote.objects.filter(voter=user).exists():
        return render(request, 'already_voted.html')

    if request.method == 'POST':
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.get(id=candidate_id)

        # Save vote
        Vote.objects.create(voter=user, candidate=candidate)

        # (Optional) Increment vote count
        candidate.vote_count += 1
        candidate.save()

        return render(request, 'thank_you.html', {'candidate': candidate})

    # GET method: show list of candidates
    candidates = Candidate.objects.all()
    return render(request, 'vote.html', {'candidates': candidates})

# the Admin-only Results Page to see who’s winning

@staff_member_required
def results_view(request):
    candidates = Candidate.objects.all().order_by('-vote_count')
    return render(request, 'results.html', {'candidates': candidates})


# from here onwards we have started crud operations.

# add candidates logic

@staff_member_required
def add_candidate(request):
    if request.method == 'POST':
        name = request.POST['name']
        party = request.POST['party']
        image = request.FILES.get('image')

        Candidate.objects.create(name=name, party=party, image=image)
        return redirect('candidate_list')

    return render(request, 'add_candidate.html')

# candidates list logic

@staff_member_required
def candidate_list(request):
    candidates = Candidate.objects.all()
    return render(request, 'candidate_list.html', {'candidates': candidates})


# update candidate or edit candidate list

@staff_member_required
def edit_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)

    if request.method == 'POST':
        candidate.name = request.POST['name']
        candidate.party = request.POST['party']
        if request.FILES.get('image'):
            candidate.image = request.FILES['image']
        candidate.save()
        return redirect('candidate_list')

    return render(request, 'edit_candidate.html', {'candidate': candidate})


# delete the candidate logic

@staff_member_required
def delete_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    candidate.delete()
    return redirect('candidate_list')

# voting/views.py

# from django.contrib.auth.models import User
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required, user_passes_test

# Only admin or staff can access these
def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
@user_passes_test(is_admin)
def voter_list(request):
    voters = User.objects.filter(is_superuser=False)  # exclude superusers
    return render(request, 'voter_list.html', {'voters': voters})

@login_required
@user_passes_test(is_admin)
def voter_add(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        User.objects.create_user(username=username, email=email, password=password)
        return redirect('voter_list')
    return render(request, 'voter_form.html')

@login_required
@user_passes_test(is_admin)
def voter_update(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()
        return redirect('voter_list')
    return render(request, 'voter_form.html', {'user': user})

@login_required
@user_passes_test(is_admin)
def voter_delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect('voter_list')

# from django.contrib.auth.models import User, Group
# from django.shortcuts import render, redirect
# from django.contrib.auth import login

# Create a custom signup form for Admin2

def register_admin2(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'register_admin2.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register_admin2.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.is_staff = True  #  So they can access staff views
        user.is_superuser = False  #  No full admin access
        user.save()

        # Optional: Add to a group called "Admin2"
        group, created = Group.objects.get_or_create(name='Admin2')
        user.groups.add(group)

        login(request, user)
        return redirect('dashboard')

    return render(request, 'register_admin2.html')

