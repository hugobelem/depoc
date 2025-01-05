from django.db import models


class Animal(models.Model):
    SPECIES_CHOICES = [
        ('cattle', 'Cattle'),
        ('pig', 'Pig'),
        ('sheep', 'Sheep'),
        ('goat', 'Goat'),
    ]
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    STATUS_CHOICES = [
        ('arrival', 'Arrival'),
        ('growth', 'Growth'),
        ('ready', 'Ready'),
        ('sold', 'Sold'),
        ('processing', 'Processing'),
        ('slaughtered', 'Slaughtered'),
    ]

    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False,
    )
    tagNumber = models.CharField(
        max_length=50,
        unique=True,
        help_text='Unique animal ID or ear tag number',
    )
    name = models.CharField(
        max_length=100,
        blank=True,
    )
    species = models.CharField(
        max_length=50,
        choices=SPECIES_CHOICES,
    )
    breed = models.CharField(
        max_length=100,
        blank=True,
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
    )
    age = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text='Age in months',
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='arrival',
        help_text='Current status of the animal or meat',
    )
    origin = models.CharField(
        max_length=255,
        blank=True,
        help_text='Farm or source of origin',
    )

    class Meta:
        verbose_name_plural = 'Animals'
        app_label = 'modules_animals'

    def __str__(self):
        return f"{self.species} - {self.tagNumber}"


class AnimalFinancial(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False,
    )
    animal = models.OneToOneField(
        Animal,
        on_delete=models.CASCADE,
        related_name='financial',
    )
    purchaseCost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    maintenanceCost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    estimatedValue = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Estimated live animal value',
    )
    sellingPrice = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = 'Animals Financial'
        app_label = 'modules_animals'

    def __str__(self):
        f"Financial Info for {self.animal.tagNumber}"


class AnimalLifeCycle(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False,
    )
    animal = models.OneToOneField(
        Animal,
        on_delete=models.CASCADE,
        related_name='life_cycle',
    )
    arrivalDate = models.DateField()
    processedDate = models.DateField(blank=True, null=True)


    class Meta:
        verbose_name_plural = 'Animals Life Cycle'
        app_label = 'modules_animals'

    def __str__(self):
        return f"Lifecycle Info for {self.animal.tagNumber}"


class AnimalGrowth(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False,
    )
    animal = models.OneToOneField(
        Animal,
        on_delete=models.CASCADE,
        related_name='growth',
    )
    feedType = models.CharField(
        max_length=255,
        blank=True,
        help_text='Type of feed provided (e.g., grass-fed, grain-fed)',
    )
    feedConsumed = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Feed consumed in kg',
    )
    feedConversionRate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Feed consumed per kg of weight gained',
    )
    GrowthRate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Growth rate in kg per day',
    )

    class Meta:
        verbose_name_plural = 'Animals Growth'
        app_label = 'modules_animals'

    def __str__(self):
        return f"Growth Info for {self.animal.tagNumber}"


class AnimalWeight(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False,
    )
    animal = models.OneToOneField(
        Animal,
        on_delete=models.CASCADE,
        related_name='weight',
    )
    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Height in m',
    )
    weight = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        blank=False,
        help_text='Weight in kg',
    )
    processedWeight = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        blank=False,
        help_text='Weight at processed date in kg',
    )
    carcassWeight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Carcass weight in kg',
    )
    dressingPercentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Carcass yield as a percentage of processed weight',
    )


    class Meta:
        verbose_name_plural = 'Animals Weight'
        app_label = 'modules_animals'

    def __str__(self):
        return f"Weight Info for {self.animal.tagNumber}"


class AnimalMeatQuality(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False,
    )
    animal = models.OneToOneField(
        Animal,
        on_delete=models.CASCADE,
        related_name='meat_quality',
    )
    backFatThickness = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Meat Quality Info for {self.animal.tagNumber}"


class AnimalHealth(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False,
    )
    animal = models.OneToOneField(
        Animal,
        on_delete=models.CASCADE,
        related_name='health',
    )
    healthStatus = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Health Info for {self.animal.tagNumber}"
