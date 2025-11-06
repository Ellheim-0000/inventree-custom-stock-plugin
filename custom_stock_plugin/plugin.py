
from plugin import InvenTreePlugin

from django.urls import path

from django.shortcuts import render

from django.contrib.auth.decorators import login_required

try:
    from stock.models import StockItem
except Exception:
    StockItem = None
class CustomStockViewPlugin(InvenTreePlugin):
    NAME = "Custom Stock View"
    SLUG = "custom-stock-view"
    AUTHOR = "Твоє ім'я"
    DESCRIPTION = "Кастомна сторінка для перегляду Stock з власним фільтром"
    VERSION = "1.0"

    def setup_urls(self):
def setup_urls(self):
    # Реєструємо маршрут: /plugin/custom-stock/
    return [
        path('custom-stock/', login_required(self.stock_view), name='custom-stock-view'),
    ]

def stock_view(self, request):
    """
    Рендеримо кастомну сторінку з фільтром.
    Використовує Django ORM для читання StockItem, якщо модель доступна.
    """
    q = request.GET.get('q', '').strip()
    items = []

    if StockItem is not None:
        qs = StockItem.objects.select_related('part', 'location').all()
        if q:
            # фільтр по імені деталі (case-insensitive contains)
            qs = qs.filter(part__name__icontains=q)
        # обмежимо для безпеки
        items = qs.order_by('pk')[:200]

    context = {
        "title": "Custom Stock View",
        "data": items,
        "query": q,
    }
    return render(request, "custom_stock.html", context)
