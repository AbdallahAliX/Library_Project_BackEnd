from django.db import models



class Bookitem(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    image = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    

class User(models.Model):
    role = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username + ' - ' + self.role
    
class Borrowedbook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Bookitem, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title + ' - ' + self.user.username

class CurrentUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' - ' + self.user.role    