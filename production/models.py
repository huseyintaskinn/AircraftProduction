from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _

PART_CHOICES = (
    ('wing', 'Kanat'),
    ('fuselage', 'Gövde'),
    ('tail', 'Kuyruk'),
    ('avionics', 'Aviyonik'),
)

AIRCRAFT_CHOICES = (
    ('TB2', 'TB2'),
    ('TB3', 'TB3'),
    ('AKINCI', 'AKINCI'),
    ('KIZILELMA', 'KIZILELMA'),
)

TEAM_CHOICES = (
    ('wingTeam', 'Kanat Takımı'),
    ('fuselageTeam', 'Gövde Takımı'),
    ('tailTeam', 'Kuyruk Takımı'),
    ('avionicsTeam', 'Aviyonik Takımı'),
    ('assemblyTeam', 'Montaj Takımı'),
)


def create_groups():
    admin_group, created = Group.objects.get_or_create(name='Admin')
    wing_group, created = Group.objects.get_or_create(name='Kanat Takımı')
    fuselage_group, created = Group.objects.get_or_create(name='Gövde Takımı')
    tail_group, created = Group.objects.get_or_create(name='Kuyruk Takımı')
    avionics_group, created = Group.objects.get_or_create(name='Aviyonik Takımı')
    assembly_group, created = Group.objects.get_or_create(name='Montaj Takımı')

    return admin_group, wing_group, fuselage_group, tail_group, avionics_group, assembly_group


def team_to_group(team):
    return {
        'wingTeam': 'Kanat Takımı',
        'fuselageTeam': 'Gövde Takımı',
        'tailTeam': 'Kuyruk Takımı',
        'avionicsTeam': 'Aviyonik Takımı',
        'assemblyTeam': 'Montaj Takımı',
    }[team]


class Part(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        choices=PART_CHOICES,
        verbose_name=_('Parça Adı'),
        max_length=100
    )
    aircraft_type = models.CharField(
        choices=AIRCRAFT_CHOICES,
        verbose_name=_('Uçak Tipi'),
        max_length=100
    )
    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Parça')
        verbose_name_plural = _('Parçalar')

    def __str__(self):
        return f"{self.aircraft_type} Tipi {self.name}"


class Employee(AbstractUser):
    team = models.CharField(
        choices=TEAM_CHOICES,
        verbose_name=_('Takım Adı'),
        max_length=100
    )
    groups = models.ManyToManyField(
        Group,
        related_name='employee_set',
        blank=True,
        help_text=_('Kullanıcının ait olduğu gruplar.')
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='employee_permissions',
        blank=True,
        help_text=_('Bu kullanıcı için özel izinler.')
    )

    def save(self, *args, **kwargs):
        super(Employee, self).save(*args, **kwargs)
        if self.team:
            group = Group.objects.get(name=team_to_group(self.team))
            self.groups.clear()
            self.groups.add(group)

    class Meta:
        verbose_name = _('Çalışan')
        verbose_name_plural = _('Çalışanlar')

    def __str__(self):
        return f"{self.username}"


class Assembly(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    aircraft_type = models.CharField(
        choices=AIRCRAFT_CHOICES,
        verbose_name=_('Uçak Tipi'),
        max_length=100
    )
    wing = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='wing')
    fuselage = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='fuselage')
    tail = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='tail')
    avionics = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='avionics')
    is_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.wing.aircraft_type != self.aircraft_type:
            raise ValueError('Kanat parçası ilgili uçak tipine ait değil.')
        if self.fuselage.aircraft_type != self.aircraft_type:
            raise ValueError('Gövde parçası ilgili uçak tipine ait değil.')
        if self.tail.aircraft_type != self.aircraft_type:
            raise ValueError('Kuyruk parçası ilgili uçak tipine ait değil.')
        if self.avionics.aircraft_type != self.aircraft_type:
            raise ValueError('Aviyonik parçası ilgili uçak tipine ait değil.')
        if self.wing.name != 'wing':
            raise ValueError('Kanat parçası yanlış.')
        if self.fuselage.name != 'fuselage':
            raise ValueError('Gövde parçası yanlış.')
        if self.tail.name != 'tail':
            raise ValueError('Kuyruk parçası yanlış.')
        if self.avionics.name != 'avionics':
            raise ValueError('Aviyonik parçası yanlış.')
        if self.employee.team != 'assemblyTeam':
            raise ValueError('Kullanıcı montaj takımında değil.')

        super(Assembly, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Montaj')
        verbose_name_plural = _('Montajlar')

    def __str__(self):
        return f"{self.aircraft_type} Montajı"
