from django import forms
from django_select2.forms import Select2Widget
from .models import Profile, Submission, Review, Reviewer, Revision, Decision
from bootstrap_datepicker_plus.widgets  import DatePickerInput
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('fullname', 'photo', 'dob', 'gender', 'address', 'city', 'phone', 'mobile')

        widgets = {
            'dob': DatePickerInput()
        }


class SubmissionForm(forms.ModelForm):

    class Meta:
        model = Submission
        fields = '__all__'
        exclude = ['user', 'status' ]





class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = '__all__'
        exclude = ['reviewer', 'submission', ]


class RevisionForm(forms.ModelForm):

    class Meta:
        model = Revision
        fields = '__all__'
        exclude = ['submission', 'created_at'  ]


class DecisionForm(forms.ModelForm):

    class Meta:
        model = Decision
        fields = '__all__'
        exclude = ['submission', 'created_at'  ]


class ReviewerForm(forms.ModelForm):

    class Meta:
        model = Reviewer
        fields = '__all__'
        exclude = [ 'submission', ]

        widgets = {
            'user': Select2Widget,
        }