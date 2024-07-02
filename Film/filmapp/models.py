from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Role(BaseModel):
    name = models.CharField(max_length=20, unique=True)  # tên vai trò phải là unique

    def __str__(self):
        return self.name


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    first_name = None  # Không sử dụng trường first_name của AbstractUser
    last_name = None  # Không sử dụng trường last_name của AbstractUser
    address = models.CharField(max_length=50, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True)
    image = models.ImageField(upload_to='User/%Y/%m', blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=150, null=False, blank=False)  # tên của khách hàng thuê
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)


# Model thể loại phim
class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


# Model film
class Movie(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    release_date = models.DateField()
    duration = models.IntegerField()  # Duration in minutes
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    poster = models.ImageField(upload_to='Poster/%Y/%m', blank=True, null=True)

    def __str__(self):
        return self.name


class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['movie','genre']
    def __str__(self):
        return f'{self.movie.name} - {self.genre.name}'
