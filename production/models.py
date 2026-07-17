from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

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
    }.get(team)


def team_to_part_type(team):
    return {
        'wingTeam': 'wing',
        'fuselageTeam': 'fuselage',
        'tailTeam': 'tail',
        'avionicsTeam': 'avionics',
    }.get(team)


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
        is_new = self.pk is None
        super(Employee, self).save(*args, **kwargs)
        if self.team:
            group_name = team_to_group(self.team)
            if group_name:
                group, _ = Group.objects.get_or_create(name=group_name)
                self.groups.clear()
                self.groups.add(group)

    class Meta:
        verbose_name = _('Çalışan')
        verbose_name_plural = _('Çalışanlar')

    def __str__(self):
        return f"{self.username} ({self.get_team_display()})"


class Part(models.Model):
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
    is_used = models.BooleanField(default=False, verbose_name=_('Kullanıldı mı?'))
    is_recycled = models.BooleanField(default=False, verbose_name=_('Geri Dönüşüme Gönderildi mi?'))
    created_by = models.ForeignKey(
        Employee, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='produced_parts',
        verbose_name=_('Üreten Personel')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Üretim Tarihi'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Güncellenme Tarihi'))

    class Meta:
        verbose_name = _('Parça')
        verbose_name_plural = _('Parçalar')
        ordering = ['-created_at']

    def __str__(self):
        status = " (Kullanıldı)" if self.is_used else (" (Geri Dönüşüm)" if self.is_recycled else "")
        return f"{self.aircraft_type} Tipi {self.get_name_display()}{status}"


class Assembly(models.Model):
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.PROTECT, 
        related_name='assemblies',
        verbose_name=_('Montajlayan Personel')
    )
    aircraft_type = models.CharField(
        choices=AIRCRAFT_CHOICES,
        verbose_name=_('Uçak Tipi'),
        max_length=100
    )
    wing = models.ForeignKey(Part, on_delete=models.PROTECT, related_name='assembly_wing', verbose_name=_('Kanat Parçası'))
    fuselage = models.ForeignKey(Part, on_delete=models.PROTECT, related_name='assembly_fuselage', verbose_name=_('Gövde Parçası'))
    tail = models.ForeignKey(Part, on_delete=models.PROTECT, related_name='assembly_tail', verbose_name=_('Kuyruk Parçası'))
    avionics = models.ForeignKey(Part, on_delete=models.PROTECT, related_name='assembly_avionics', verbose_name=_('Aviyonik Parçası'))
    assembled_at = models.DateTimeField(default=timezone.now, verbose_name=_('Montaj Tarihi'))
    is_completed = models.BooleanField(default=True, verbose_name=_('Montaj Tamamlandı mı?'))

    class Meta:
        verbose_name = _('Montaj')
        verbose_name_plural = _('Montajlar')
        ordering = ['-assembled_at']

    def __str__(self):
        return f"{self.aircraft_type} Uçağı Montajı (#{self.id})"
