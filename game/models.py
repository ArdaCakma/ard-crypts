from django.db import models
from django.contrib.auth.models import User

class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_crystals = models.IntegerField(default=0)
    high_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} | Rekor: {self.high_score}"

class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField(default=0)
    crystals_collected = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']

    def __str__(self):
        player_name = self.user.username if self.user else "Misafir"
        return f"{player_name} - Skor: {self.score}"