from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from myproject.demo1.models import Score, Rank



def upload(request):
    if request.method == 'GET':
        return render(request, 'demo1/upload.html')
    if request.method == 'POST':
        # 接受页面上传的数据
        score = request.POST.get('score', '')
        username=request.POST.get('username', '')
        if score:
            Score.objects.create(client=request.user, score=score)
            # 排名表数据更新
            Rank.objects.all().delete()
            score_li = [score_obj.id for score_obj in Score.objects.all().order_by('-score')]
            n = 1
            for i in score_li:
                Rank.objects.create(c_id_id=i, rank=n)
                n = n + 1
            return JsonResponse({'status': 'sucess'})
        return JsonResponse({'status': 'error'})

def show(request):
    result_list=[]
    for scor in Score.objects.all().order_by('-score'):
        context = {}
        context['client']=scor.client
        context['rank']=scor.rank.rank
        context['score']=scor.score
        result_list.append(context)
    result={'scores':result_list}

    if request.method == 'GET':
        count = Score.objects.all().count()
        uscore = Score.objects.filter(client=request.user).first()
        uscore = {'ranking': uscore.rank.rank, 'score': uscore.score}
        return render(request, 'demo1/show.html', {'result': result, 'count': count, 'uscore': uscore})
    if request.method == 'POST':
        try:
            start = int(request.POST.get('start'))
            end = int(request.POST.get('end'))
        except ValueError:
            return JsonResponse({'status': 'error'})

        for scor in Score.objects.all().order_by('-score')[start - 1:end]:
            context = {}
            context['client'] = scor.client
            context['rank'] = scor.rank.rank
            context['score'] = scor.score
            result_list.append(context)
        result = {'scores': result_list}
        return JsonResponse({'status': 'ok', 'result': result})

