from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from django.contrib.auth.models import User
'''
@login_required
def service_home(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        'user_name': profile.user.username,  # Fetch the name from the user profile
    }
    return render(request, 'service.html', context)
'''
@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        # Retrieve updated information from the form and save it
        profile.user.username = request.POST.get('name', profile.user.username)
        profile.gender = request.POST.get('gender', profile.gender)
        profile.living_place = request.POST.get('living_place', profile.living_place)
        profile.description = request.POST.get('description', profile.description)

        # Save the user and profile updates
        profile.user.save()
        profile.save()

        return redirect('profile')  # Redirect to the same page to refresh data

    context = {
        'profile': profile,
        'user_name': profile.user.username,
    }
    return render(request, 'profile.html', context)

def online_service(request):
    return render(request, 'online_service.html')

def chatting_service(request):
    return render(request, 'chatting.html')

def map_service(request):
    return render(request, 'map_service.html')
'''
@login_required
def service_home(request):
    return render(request, 'service.html')  # Make sure this matches your template path
'''

@login_required
def service_home(request):
    # Fetch the profile for the current user
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None  # or handle it as appropriate for your application

    context = {
        'profile': profile,
    }
    return render(request, 'service.html', context)

from service.models import Profile


@login_required
def map_service(request):
    # Get user's profile
    profile = Profile.objects.get(user=request.user)

    # Clear session if requested
    if request.method == 'GET' and 'clear_session' in request.GET:
        if 'locations' in request.session:
            del request.session['locations']
        return redirect('map_detail')

    if request.method == 'POST':
        # Retrieve selected locations from the form
        locations = request.POST.getlist('location')
        if not locations:
            messages.warning(request, "Please select at least one location.")
            return redirect('map_service')

        # Save locations in session
        request.session['locations'] = locations
        return redirect('map_detail')

    # List of available locations for the dropdown
    available_locations = [
        "Adelaide City",
        "Unley",
        "St Peters",
        "Norwood",
        "Rose Park",
        "North Adelaide",
        "Parkside",
        "Wayville",
        "Dulwich"
    ]

    context = {
        'user': request.user,
        'profile': profile,
        'available_locations': available_locations
    }
    return render(request, 'map_service.html', context)


def map_detail(request):
    is_direct_view = request.GET.get('clear_session', False)
    locations = []  # Initialize locations with empty list
    is_at_risk = False

    all_areas = [
        "Adelaide City", "Dulwich", "Mile End", "North Adelaide",
        "Norwood", "Ovingham", "Parkside", "Rose Park",
        "St Peters", "Unley", "Wayville"
    ]

    default_covid_areas = [
        "Adelaide City", "Norwood", "Rose Park",
        "Ovingham", "Mile End", "Unley"
    ]

    area_name_map = {
        "adelaide_city": "Adelaide City",
        "north_adelaide": "North Adelaide",
        "ovingham": "Ovingham",
        "st_peters": "St Peters",
        "norwood": "Norwood",
        "rose_park": "Rose Park",
        "mile_end": "Mile End",
        "unley": "Unley",
        "parkside": "Parkside",
        "dulwich": "Dulwich",
        "wayville": "Wayville"
    }

    # Update positions
    area_positions = {
        "adelaide_city": {"x": 170, "y": -20, "marker_x": 465, "marker_y": 265, "scale": 0.6},
        "north_adelaide": {"x": 145, "y": -135, "marker_x": 465, "marker_y": 65, "scale": 0.6},
        "ovingham": {"x": 239, "y": -58, "marker_x": 365, "marker_y": 165, "scale": 0.6},
        "st_peters": {"x": 500, "y": -30, "marker_x": 615, "marker_y": 165, "scale": 0.4},
        "norwood": {"x": 427, "y": -27, "marker_x": 615, "marker_y": 265, "scale": 0.6},
        "rose_park": {"x": 370, "y": 30, "marker_x": 615, "marker_y": 365, "scale": 0.6},
        "mile_end": {"x": -38, "y": -10, "marker_x": 315, "marker_y": 415, "scale": 0.6},
        "unley": {"x": 270, "y": 210, "marker_x": 465, "marker_y": 415, "scale": 0.6},
        "parkside": {"x": 250, "y": 177, "marker_x": 565, "marker_y": 415, "scale": 0.6},
        "dulwich": {"x": 450, "y": 88, "marker_x": 515, "marker_y": 365, "scale": 0.6},
        "wayville": {"x": 150, "y": 210, "marker_x": 415, "marker_y": 465, "scale": 0.5}
    }


    if not is_direct_view:
        locations = request.session.get('locations', [])
        is_at_risk = any(location in default_covid_areas for location in locations)

    context = {
        'all_areas': all_areas,
        'covid_areas': default_covid_areas,
        'area_positions': area_positions,
        'area_name_map': area_name_map,
        'locations': locations,
        'is_at_risk': is_at_risk,
        'is_direct_view': bool(is_direct_view)
    }

    return render(request, 'map_detail.html', {
        'all_areas': all_areas,
        'locations': locations,
        'is_at_risk': is_at_risk,
        'covid_areas': default_covid_areas,
        'area_positions': area_positions,
        'is_direct_view': False
    })
def ask_doctor(request):
    # Add your view logic here
    return render(request, 'ask_doctor.html')

'''
def profile_view(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        # Fetch form data
        name = request.POST.get('name', profile.user.username)
        gender = request.POST.get('gender', profile.gender)
        living_place = request.POST.get('living_place', profile.living_place)
        description = request.POST.get('description', profile.description)

        # Update the profile fields
        profile.user.username = name
        profile.gender = gender
        profile.living_place = living_place
        profile.description = description

        # Save changes to both the user and profile
        profile.user.save()
        profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('profile')  # Redirect to reload with updated data

    return render(request, 'profile.html', {'profile': profile})
'''