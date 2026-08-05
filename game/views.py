import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import GameSession, PlayerProfile

def game_index(request):
    """Ana oyun sayfasını ve skor tablosunu yükler."""
    top_scores = GameSession.objects.all()[:5]  # En yüksek 5 skor
    return render(request, 'index.html', {'top_scores': top_scores})

@csrf_exempt
def save_score(request):
    """Oyun bitince JavaScript'ten gelen skoru kaydeder."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            score = data.get('score', 0)
            crystals = data.get('crystals', 0)

            user = request.user if request.user.is_authenticated else None

            # Yeni oturum kaydı
            session = GameSession.objects.create(
                user=user,
                score=score,
                crystals_collected=crystals
            )

            # Giriş yapmış kullanıcı varsa rekorunu güncelle
            if user:
                profile, _ = PlayerProfile.objects.get_or_create(user=user)
                profile.total_crystals += crystals
                if score > profile.high_score:
                    profile.high_score = score
                profile.save()

            return JsonResponse({'status': 'success', 'message': 'Skor kaydedildi!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'invalid_method'}, status=405)