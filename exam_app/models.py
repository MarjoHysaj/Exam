from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if 'name' not in postData or len(postData['name']) < 3:
            errors['name'] = "Name should be at least 3 characters!"
        if 'username' not in postData or len(postData['username']) < 3:
            errors['username'] = "Username should be at least 3 characters!"
        username_usage = self.filter(username = postData['username'])
        if username_usage:
            errors['username'] = "Username already exists!"
        if 'password' not in postData or len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters!"
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "The passwords do not match!"
        if 'date' not in postData or len(postData['date']) < 1:
            errors['date'] = "Date Hired should be at least 3 characters!"
        return errors

    def authenticate(self, username, password):
        users = self.filter(username = username)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, postData):
        pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()

        return self.create(
            name = postData['name'],
            username = postData['username'],
            date = postData['date'],
            password = pw
        )

class WishlistManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if 'item' not in postData or len(postData['item']) < 3:
            errors['item'] = "Item should be at least 3 characters!"
        return errors

class User(models.Model):
    name = models.CharField(max_length=225)
    username = models.CharField(max_length=225)
    password = models.CharField(max_length=255)
    date = models.DateTimeField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Wishlist(models.Model):
    item = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="created_wishlist", on_delete = models.CASCADE)
    wishlister = models.ManyToManyField(User, related_name="wishlists")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishlistManager()
    