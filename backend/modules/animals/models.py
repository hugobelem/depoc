from django.db import models


class Animals(models.Model):
    SPECIES_CHOICES = [
        ('cattle', 'Cattle'),
        ('pig', 'Pig'),
        ('sheep', 'Sheep'),
        ('goat', 'Goat'),
        ('other', 'Other'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown'),
    ]

    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False
    )
    name = models.CharField(max_length=100, blank=True)
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES, blank=False)
    breed = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    age = models.PositiveIntegerField(blank=True, help_text="Age in months")
    medicalHistory = models.TextField(blank=True)
    arrivalDate = models.DateField(blank=True, null=True)
    slaughterDate = models.DateField(blank=True, null=True)
    weight = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        blank=False,
        help_text="Weight in kg",
    )
    carcassWeight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Carcass weight in kg"
    )
    yieldPercentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Carcass yield as a percentage of live weight"
    )
    fatPercentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=False,
        help_text="Percentage of fat",
    )
    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Height in cm",
    )
    healthStatus = models.CharField(
        max_length=255,
        blank=True,
        help_text="General health observations",
    )
    vaccinationStatus = models.TextField(
        blank=True,
        help_text="Details about vaccinations",
    )
    origin = models.CharField(
        max_length=255,
        blank=True,
        help_text="Farm or source of origin"
    )
    tagNumber = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique animal ID or ear tag number"
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes or observations"
    )

    class Meta:
        verbose_name_plural = 'Animals'
        app_label = 'modules_animals'

    def __str__(self):
        return self.species
