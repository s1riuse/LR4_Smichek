from django.shortcuts import render
from django.http import JsonResponse
import json
import os
import time

# Имитация хранилища лимитов (в реальном контейнере они лежат в БД или переменных окружения)
limits = {"rate_limit": 3, "time_window_sec": 10, "disk_threshold_percent": 90}

# Имитация журнала событий (список словарей)
event_log = [
    {
        "timestamp": "2026-04-16T10:00:00",
        "user_id": "ваня",
        "action": "доступ разрешен",
        "reason": "",
    },
    {
        "timestamp": "2026-04-16T10:00:05",
        "user_id": "киря",
        "action": "доступ заблокирован",
        "reason": "превышение количества входов",
    },
    {
        "timestamp": "2026-04-16T10:01:00",
        "user_id": "тимон",
        "action": "доступ заблокирован",
        "reason": "превышен лимит памяти",
    },
    
]


def index(request):
    """Главная страница админ-панели"""
    # Получаем текущее состояние диска (имитация)
    disk_free_percent = 45  # в реальности получаем через os.statvfs
    context = {
        "limits": limits,
        "disk_free_percent": disk_free_percent,
        "events": event_log[-20:],  # последние 20 событий
    }
    return render(request, "admin_panel/index.html", context)


def update_limits(request):
    """Обработчик AJAX-запроса для обновления лимитов"""
    if request.method == "POST":
        data = json.loads(request.body)
        limits["rate_limit"] = int(data.get("rate_limit", limits["rate_limit"]))
        limits["time_window_sec"] = int(
            data.get("time_window_sec", limits["time_window_sec"])
        )
        limits["disk_threshold_percent"] = int(
            data.get("disk_threshold_percent", limits["disk_threshold_percent"])
        )
        # Запись в лог о смене лимитов
        event_log.append(
            {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "user_id": "admin",
                "action": "config_change",
                "reason": f"limits updated to {limits}",
            }
        )
        return JsonResponse({"status": "ok", "limits": limits})
    return JsonResponse({"error": "Method not allowed"}, status=405)


def get_logs(request):
    """Возвращает журнал событий в JSON (для динамической подгрузки)"""
    return JsonResponse({"logs": event_log[-50:]})
