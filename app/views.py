import xlwt
from templated_email import send_templated_mail
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Submission, Review, Reviewer, Revision, Decision
from .forms import UserRegistrationForm, ProfileForm, UserForm, SubmissionForm, ReviewForm, ReviewerForm, RevisionForm, DecisionForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from bootstrap_datepicker_plus.widgets import DatePickerInput


# Create your views here.
def homepage(request):
    context = {

    }
    return render(request, 'homepage.html', context)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
           # send_templated_mail(
           #     template_name='welcome',
           #     from_email='no-reply@ui.ac.id',
           #     recipient_list=[new_user.email],
           #     context={
           #         'username': new_user.username,
           #         'full_name': new_user.get_full_name(),
           #         'password': new_user.password
           #     },
                # Optional:
                # cc=['cc@example.com'],
                # bcc=['bcc@example.com'],
                # headers={'My-Custom-Header':'Custom Value'},
                # template_prefix="my_emails/",
                # template_suffix="email",
            #)

            # Create the user profile
            profile = Profile.objects.create(user=new_user)
            profile.save()
            messages.success(request,
                             'Your registration has been succesfully.')

            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


@login_required
def dashboard(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'dashboard.html', context)


@login_required
def profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'profile/profile.html', context)


@login_required
def profile_update(request):
    if request.method == 'POST':
        formuser = UserForm(instance=request.user,
                            data=request.POST)
        formprofile = ProfileForm(instance=request.user.profile,
                                  data=request.POST,
                                  files=request.FILES)

        # Check if the form is valid:
        if formuser.is_valid() and formprofile.is_valid():
            formuser.save()
            formprofile.save()

            messages.success(request, 'Your profile has been updated.')
        else:
            messages.error(request, 'Error ! Profile has not been updated.')
    else:
        formuser = UserForm(instance=request.user)
        formprofile = ProfileForm(instance=request.user.profile)

    context = {
        'formuser': formuser,
        'formprofile': formprofile,
    }
    return render(request, 'profile/profile_update.html', context)


@login_required
@staff_member_required
def submission_list(request):
    all_submission = Submission.objects.all()

    context = {
        'object_list': all_submission
    }
    return render(request, 'submission/submission_list.html', context)


@login_required
@staff_member_required
def reviewer_submission_list(request):
    all_submission = Reviewer.objects.filter(user=request.user)
    context = {
        'object_list': all_submission
    }
    return render(request, 'submission/reviewer_submission_list.html', context)


@login_required
def my_submission_list(request):
    all_submission = Submission.objects.filter(user=request.user)

    context = {
        'object_list': all_submission
    }
    return render(request, 'submission/my_submission_list.html', context)


@login_required
def submission_detail(request, slug):
    submission = get_object_or_404(Submission, slug=slug)
    reviewers = Reviewer.objects.filter(submission=submission)
    reviews = Review.objects.filter(submission=submission)
    revisions = Revision.objects.filter(submission=submission)
    decisions = Decision.objects.filter(submission=submission)

    context = {
        'object': submission,
        'reviewers': reviewers,
        'reviews': reviews,
        'revisions': revisions,
        "decisions": decisions
    }

    return render(request, 'submission/submission_detail.html', context)


@login_required
def submission_create(request):
    form = SubmissionForm()
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission_form = form.save(commit=False)
            submission_form.user = request.user
            submission_form.save()
        #send_templated_mail(
        #    template_name='submission',
        #    from_email='info_kppikg@ui.ac.id',
        #    recipient_list=['scientific_kppikg@ui.ac.id'],
       #     context={
        #        'full_name': request.user.get_full_name(),
        #    },
            # Optional:
            # cc=['cc@example.com'],
            # bcc=['bcc@example.com'],
            # headers={'My-Custom-Header':'Custom Value'},
            # template_prefix="my_emails/",
            # template_suffix="email",
        #)

        messages.success(request, 'Submission is succesfully created.')
        slug = form.instance.slug
        submission = get_object_or_404(Submission, slug=slug)

        return redirect(submission.get_absolute_url())
    context = {
        'form': form
    }
    return render(request, 'submission/submission_create.html', context)


@login_required
def submission_update(request, slug):
    instance = get_object_or_404(Submission, slug=slug)
    form = SubmissionForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Submission is succesfully updated.')
        slug = form.instance.slug
        submission = get_object_or_404(Submission, slug=slug)
        return redirect(submission.get_absolute_url())
    context = {
        'form': form,
        'instance': 'object'
    }
    return render(request, 'submission/submission_update.html', context)


@login_required
def submission_delete(request, slug):
    submission = get_object_or_404(Submission, slug=slug)

    if request.method == "POST":
        submission.delete()
        messages.success(request, 'Submission is successfully deleted')
        return redirect("/submission/")

    context = {
        'object': submission
    }
    return render(request, 'submission/submission_delete.html', context)


@login_required
@staff_member_required
def review(request, slug):
    submission = Submission.objects.get(slug=slug)
    form = ReviewForm(request.POST, request.FILES)
    if form.is_valid():
        review_form = form.save(commit=False)
        review_form.reviewer = request.user
        review_form.submission = submission
        review_form.save()
        messages.success(request, 'Review is successfully saved')
        return redirect(submission.get_absolute_url())

    form = ReviewForm()
    context = {
        "form":form

    }
    return render(request, 'submission/review.html',context)



@login_required
@staff_member_required
def decision(request, slug):
    submission = Submission.objects.get(slug=slug)
    form = DecisionForm(request.POST, request.FILES)
    if form.is_valid():
        decision_form = form.save(commit=False)
        decision_form.submission = submission
        decision_form.save()
        messages.success(request, 'Decision is successfully submited')

        return redirect(submission.get_absolute_url())

    form = DecisionForm()
    context = {
        "form": form

    }
    return render(request, 'submission/decision.html', context)


@login_required
def revision(request, slug):
    submission = Submission.objects.get(slug=slug)
    form = RevisionForm(request.POST, request.FILES)
    if form.is_valid():
        revision_form = form.save(commit=False)
        revision_form.submission = submission
        revision_form.save()
        messages.success(request, 'Revision is successfully submited')

        return redirect(submission.get_absolute_url())

    form = RevisionForm()
    context = {
        "form":form

    }
    return render(request, 'submission/revision.html',context)


@login_required
@staff_member_required
def success(request):
    return render(request, "submission/success.html")


@login_required
@staff_member_required
def reviewer(request, slug):
    submission = Submission.objects.get(slug=slug)
    form = ReviewerForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        user = get_object_or_404(User, pk=request.POST.get('user'))
        reviewer_form = form.save(commit=False)
        reviewer_form.user = user
        reviewer_form.submission = submission
        reviewer_form.save()
        messages.success(request, 'Reviewer is successfully assigned')
        return redirect('/submission')

    form = ReviewerForm()
    context = {
        "form":form

    }
    return render(request, 'submission/reviewer.html',context)


@login_required
@staff_member_required
def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['First name', 'Last name', 'Username', 'Email address', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = User.objects.all().values_list('first_name', 'last_name', 'username', 'email', )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

@login_required
@staff_member_required
def export_profile_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="profile.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Profile')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['First name', 'Last name', 'Date of birth', 'Gender', 'Address', 'City', 'Phone', 'Mobile',
               'Email', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Profile.objects.all().values_list('user__first_name', 'user__last_name', 'dob', 'gender', 'address',
                                             'city', 'phone', 'mobile', 'user__email', )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
