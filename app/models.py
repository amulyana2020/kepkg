from django.db import models

# Create your models here.


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from autoslug import AutoSlugField
from django.utils.text import slugify

# Create your models here.


GENDER_CHOICES = (
    ('LAKI-LAKI', _('Laki-laki')),
    ('PEREMPUAN', _('Perempuan')),
)

DECISION_CHOICES = (
    ("REVISI", _('Revisi')),
    ("TIDAK PERLU REVISI", _('Tidak Perlu Revisi')),
)

DATA_CHOICES = (
    ('PRIMER', _('Primer')),
    ('SEKUNDER', _('Sekunder')),
)

STATUS_CHOICES = (
    ('PROSES REVIEW', _('Proses Review')),
    ('SELESAI', _('Selesai')),
)


class Profile(models.Model):
  fullname = models.CharField(verbose_name="Fullname with Salutation", max_length=250, null=True, blank=True)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  photo = models.ImageField(verbose_name="Photo", upload_to='images/photo', null=True, blank=True)
  dob = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
  gender = models.CharField(_('Gender'),
                                         choices=GENDER_CHOICES,
                                         blank=True,
                                         null=True, max_length=255)
  address = models.CharField(verbose_name="Address", max_length=250, null=True, blank=True)
  city =  models.CharField(verbose_name="City", max_length=250, null=True, blank=True)
  phone = models.CharField(verbose_name="Phone Number", max_length=15, null=True, blank=True)
  mobile = models.CharField(verbose_name="Mobile Phone Number", max_length=15,null=True, blank=True )

  def __str__(self):
      return '%s %s' % (self.user.first_name, self.user.last_name)


  class Meta:
      ordering=["user__first_name"]


class Submission(models.Model):
    user = models.ForeignKey(User, related_name='author', verbose_name="Nama Peneliti", on_delete=models.CASCADE)
    title = models.CharField(max_length=120, verbose_name="Judul Penelitian", null=False, blank=False)
    study_program = models.CharField(max_length=500, verbose_name="Program Studi", null=False, blank=False)
    sample_or_subject = models.CharField(max_length=500, verbose_name="Sample / Subject", null=False, blank=False)
    data = models.CharField(max_length=255, choices=DATA_CHOICES, verbose_name="Data Primer/Sekunder", default="PRIMER", null=False, blank=False)
    submission_file = models.FileField(upload_to='file/submission/', verbose_name="Formulir Pengajuan", null=False, blank=False)
    consent_file = models.FileField(upload_to='file/consent/', verbose_name="Informed Consent", null=False, blank=False)
    agreement_file = models.FileField(upload_to='file/agreement/', verbose_name="Lembar Persetujuan", null=False, blank=False)
    institution_letter = models.FileField(upload_to='file/institution_letter/', verbose_name="Surat Pengantar dari Institusi", null=False, blank=False)
    statement_letter = models.FileField(upload_to='file/statement_letter/', verbose_name="Surat Pernyataan penelitian belum dilaksanakan sebelum pengajuan kelaikan etik", null=False, blank=False)
    peer_group_form = models.FileField(upload_to='file/peer_group_form/', verbose_name="Kajian ilmiah oleh peer group atau departemen terkait", null=False, blank=False)
    curriculum_vitae = models.FileField(upload_to='file/curriculum_vitae/', verbose_name="Biodata peneliti tentang penelitian yang telah dilaksanakan", null=False, blank=False)
    payment = models.FileField(upload_to='file/payment/', null=False, blank=False,
                                        verbose_name="Bukti Pembayaran")
    created_at = models.DateField(auto_now_add=True)
    slug = AutoSlugField(populate_from='title', max_length=250)
    status = models.CharField(max_length=255, null=False, blank=False, choices=STATUS_CHOICES, default="PROSES REVIEW")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return '%s %s  --%s' % (self.user.first_name, self.user.last_name, self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Submission, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('submission_detail', args=[self.slug])

    def get_update_url(self):
        return reverse('submission_update', args=[self.slug])

    def get_delete_url(self):
        return reverse('submission_delete', args=[self.slug])


class Revision(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='revision',
                                   related_query_name='revision')
    file_revision = models.FileField(upload_to="file/file_revision/", null=False, blank=False,
                                        verbose_name="Upload File Revisi")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return ' %s' % (self.submission.title)


class Decision(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='decision',
                                   related_query_name='decision')
    file_decision = models.FileField(upload_to="file/file_decision/", null=False, blank=False,
                                        verbose_name="Upload File Etik")
    decision = models.CharField(max_length=255, verbose_name="Hasil review akhir", choices=DECISION_CHOICES, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return ' %s' % (self.submission.title)


class Review(models.Model):
    review = models.TextField(verbose_name="Review")
    file_review = models.FileField(upload_to='file/file_review/', null=True, blank=True,
                                        verbose_name="Upload hasil review")
    decision = models.CharField(max_length=255, verbose_name="Hasil review", choices=DECISION_CHOICES)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='reviews',
                                related_query_name='review')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', related_query_name='review')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return '%s %s  -- %s --%s' % (self.reviewer.first_name, self.reviewer.last_name, self.reviewer.email, self.decision)


class Reviewer(models.Model):
    submission = models.ForeignKey(Submission,on_delete=models.CASCADE, related_name="reviewer")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewers', related_query_name='reviewer')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return '%s %s  -- %s' % (self.user.first_name, self.user.last_name, self.submission.title)

    def get_submission_url(self):
        return reverse('submission_detail', args=[self.submission.slug])


