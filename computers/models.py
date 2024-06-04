from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to='brands', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Computer(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    processor = models.CharField(max_length=100)
    ram = models.IntegerField()  # in GB
    
    storage = models.CharField(max_length=100)  # e.g., '256GB SSD'
    custom_specs = models.TextField(blank=True, null=True)
    image1 = models.ImageField(upload_to='computers', blank=True, null=True)
    image2 = models.ImageField(upload_to='computers', blank=True, null=True)
    image3 = models.ImageField(upload_to='computers', blank=True, null=True)

    def __str__(self):
        return self.name
    
    def get_custom_specs(self):
        """Parse the custom_specs field and return as a dictionary."""
        if not self.custom_specs:
            return {}
        specs = {}
        for spec in self.custom_specs.split(';'):
            key_value = spec.split(':')
            if len(key_value) == 2:
                key, value = key_value
                specs[key.strip()] = value.strip()
        return specs

    def display_custom_specs(self):
        """Return the custom specifications in a readable format."""
        specs = self.get_custom_specs()
        return "\n".join(f"{key}: {value}" for key, value in specs.items())
    

# wishlist

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'Wishlist of {self.user.username}'

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.computer.name} in wishlist of {self.wishlist.user.username}'