from django.db import models

class Language(models.Model):
    """ It stores cabin crew info in languages """
    lan_name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"

    def __str__(self):
        return self.lan_name
    
class VehicleType(models.Model):
    type_veh = models.CharField(max_length=10,unique=True)

    class Meta:
        verbose_name = "Vehicle Type"
        verbose_name_plural = "Vehicle Types"

    def __str__(self):
        return self.type_veh

    
class ChefRecipe(models.Model):
    """ It stores recipes that only chef type employees can prepare """
    chef = models.ForeignKey('CabinCrew', on_delete=models.CASCADE, related_name='recipes')
    recipe_name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Chef Recipe"
        verbose_name_plural = "Chef Recipes"

    def __str__(self):
        return f"{self.recipe_name}({self.chef.attendant_id})"
    
class CabinCrew(models.Model):

    ATTENDANT_TYPES = (
        ('chief', 'Chief'),
        ('regular', 'Regular'),
        ('chef', 'Chef'),
    )

    SENORITY_LEVELS = (
        ('senior', 'Senior Attendant'),
        ('junior', 'Junior Attendant'),
        ('chef', 'Chef Role'),
    )

    attendant_id = models.CharField(max_length=10,unique=True,primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    nationality = models.CharField(max_length=50)

    attendant_type = models.CharField(max_length=10,choices=ATTENDANT_TYPES)
    senority_level = models.CharField(max_length=10, choices=SENORITY_LEVELS)

    known_languages = models.ManyToManyField(Language,related_name='crew_members')
    vehicle_restrictions = models.ManyToManyField(VehicleType,related_name='allowed_crew')

    class Meta:
        verbose_name = "Cabin Crew Attendant "
        verbose_name_plural = "Cabin Crew Attendants"

    def __str__(self):
        return f"{self.name} - {self.get_attendant_type_display()} ({self.attendant_id})"
