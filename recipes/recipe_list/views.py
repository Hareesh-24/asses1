from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import F
from .models import Recipe

def recipe_list_api(request):
    print(request.GET)
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)

    try:
        page = int(page)
        limit = int(limit)
    except ValueError:
        return JsonResponse({"error": "Invalid page or limit"}, status=400)

    queryset = Recipe.objects.all().order_by(
        F('rating').desc(nulls_last=True)
    )

    paginator = Paginator(queryset, limit)

    try:
        recipes_page = paginator.page(page)
    except:
        return JsonResponse({"error": "Invalid page number"}, status=400)

    results = []

    for recipe in recipes_page:
        results.append({
            "id": recipe.id,
            "cuisine": recipe.cuisine,
            "title": recipe.title,
            "rating": recipe.rating,
            "prep_time": recipe.prep_time,
            "cook_time": recipe.cook_time,
            "total_time": recipe.total_time,
            "description": recipe.description,
            "nutrients": recipe.nutrients,
            "serves": recipe.serves,
        })

    return JsonResponse({
        "page":page,
        "limit":limit,
        "total":paginator.count,
        "data":results
    })
def recipe_search_api(request):
    queryset = Recipe.objects.all()

    title = request.GET.get('title')
    cuisine = request.GET.get('cuisine')
    rating = request.GET.get('rating')
    total_time = request.GET.get('total_time')
    calories = request.GET.get('calories')

    if title:
        queryset = queryset.filter(title__icontains=title)
    if cuisine:
        queryset = queryset.filter(cuisine__icontains=cuisine)

    def apply_filter(qs, field, value):
        if value.startswith('>='):
            return qs.filter(**{f'{field}__gte': float(value[2:])})
        elif value.startswith('<='):
            return qs.filter(**{f'{field}__lte': float(value[2:])})
        return qs.filter(**{field: float(value)})

    if rating:
        queryset = apply_filter(queryset, 'rating', rating)
    if total_time:
        queryset = apply_filter(queryset, 'total_time', total_time)

    results = list(queryset)

    if calories:
        op = '>=' if '>=' in calories else '<=' if '<=' in calories else '='
        cal_val = float(calories.replace('>=','').replace('<=',''))
        results = [r for r in results if r.nutrients and 'calories' in r.nutrients
                   and (float(r.nutrients['calories'].split()[0]) >= cal_val if op == '>='
                   else float(r.nutrients['calories'].split()[0]) <= cal_val if op == '<='
                   else float(r.nutrients['calories'].split()[0]) == cal_val)]

    data = [{"id": r.id, "title": r.title, "cuisine": r.cuisine, "rating": r.rating,
             "prep_time": r.prep_time, "cook_time": r.cook_time, "total_time": r.total_time,
             "description": r.description, "nutrients": r.nutrients, "serves": r.serves}
            for r in results]

    return JsonResponse({"data": data})
