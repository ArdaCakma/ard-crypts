import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import GameSession, PlayerProfile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import Score

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





@method_decorator(csrf_exempt, name='dispatch')
class SaveScoreView(View):

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            raw_username = data.get('username', '').strip()
            score_val = int(data.get('score', 0))
            crystals_val = int(data.get('crystals', 0))

            # Kullanıcı adı belirleme mantığı
            if request.user.is_authenticated:
                user_obj = request.user
                player_name = user_obj.username
            else:
                user_obj = None
                player_name = raw_username if raw_username else "Misafir"

            # Skoru Veritabanına Kaydet
            Score.objects.create(
                user=user_obj,
                username=player_name,
                score=score_val,
                crystals=crystals_val
            )

            # Güncel Liderlik Tablosunu Çek (En yüksek 10 skor)
            top_scores = Score.objects.all()[:10]
            leaderboard_data = [
                {
                    'username': item.username,
                    'score': item.score,
                    'crystals': item.crystals,
                    'date': item.created_at.strftime('%Y-%m-%d %H:%M')
                }
                for item in top_scores
            ]

            return JsonResponse({
                'status': 'success',
                'message': 'Skor başarıyla kaydedildi.',
                'leaderboard': leaderboard_data
            }, status=201)

        except (ValueError, json.JSONDecodeError):
            return JsonResponse({'status': 'error', 'message': 'Geçersiz veri formatı.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    def get(self, request, *args, **kwargs):
        """Sadece liderlik tablosunu çekmek isteyen istekler için"""
        top_scores = Score.objects.all()[:10]
        leaderboard_data = [
            {
                'username': item.username,
                'score': item.score,
                'crystals': item.crystals,
                'date': item.created_at.strftime('%Y-%m-%d %H:%M')
            }
            for item in top_scores
        ]
        return JsonResponse({'status': 'success', 'leaderboard': leaderboard_data}, status=200)