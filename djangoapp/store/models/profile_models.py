from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
import re
from store.utils.utils import valida_cc


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(blank=True, null=True)
    date_of_birth = models.DateField()
    cc = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    number = models.CharField(max_length=5)
    postal_code = models.CharField(max_length=8)
    city = models.CharField(max_length=30)
    local = models.CharField(max_length=50)
    district = models.CharField(
        max_length=2,
        default='LI',
        choices=(
            ('LI', 'Lisboa'),
            ('PO', 'Porto'),
            ('SE', 'Setubal'),
            ('BR', 'Braga'),
            ('AV', 'Aveiro'),
            ('FA', 'Faro'),
            ('LE', 'Leiria'),
            ('SA', 'Santarém'),
            ('CO', 'Coimbra'),
            ('VI', 'Viseu'),
            ('MA', 'Madeira'),
            ('AÇ', 'Açores'),
            ('VC', 'Viana Do Castelo'),
            ('VR', 'Vila Real'),
            ('CB', 'Castelo Branco'),
            ('EV', 'Évora'),
            ('BE', 'Beja'),
            ('GU', 'Guarda'),
            ('BG', 'Bragança'),
            ('PO', 'Portalegre'),
        )
    )

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def clean(self) -> None:
        error_messages = {}

        _cc = self.cc or None

        _db_cc = None

        _profile = UserProfile.objects.filter(cc=_cc).first()

        if _profile:
            _db_cc = _profile.cc

            if _db_cc is not None and self.pk != _profile.pk:
                # cc already exists
                error_messages['cc'] = 'cc number already exists!'

        if not valida_cc(self.cc):
            error_messages['cc'] = 'Input a correct cc number'

        if re.search(r'[^0-9+''-'']', self.postal_code) or len(self.postal_code) < 7:
            error_messages['postal_code'] = (
                'Invalid Postal Code!, input only 7 digits (4-3) numbers'
            )

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'Profiles'
