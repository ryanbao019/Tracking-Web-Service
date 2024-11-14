from django import forms

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'living_place', 'description']

# In views.py:
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()