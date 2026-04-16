from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .services import search_qa, build_answer


def qa_page(request):
    query = request.GET.get("q", "").strip()
    results = search_qa(query) if query else []
    answer_data = build_answer(query, results) if query else None

    return render(request, "qa/qa_page.html", {
        "query": query,
        "results": results,
        "answer_data": answer_data,
    })


@require_GET
def qa_ask(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return JsonResponse({
            "ok": False,
            "message": "Введите вопрос."
        }, status=400)

    results = search_qa(query)
    answer_data = build_answer(query, results)

    serialized_results = []
    for item in results:
        serialized_results.append({
            "title": item.title,
            "url": item.url,
            "source_type": item.get_source_type_display(),
            "summary": item.summary,
        })

    return JsonResponse({
        "ok": True,
        "query": query,
        "answer": answer_data["text"],
        "top_result": {
            "title": answer_data["top_result"].title,
            "url": answer_data["top_result"].url,
            "summary": answer_data["top_result"].summary,
            "source_type": answer_data["top_result"].get_source_type_display(),
        } if answer_data["top_result"] else None,
        "results": serialized_results,
    })