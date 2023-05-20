from django.http import JsonResponse
import json
from django.shortcuts import render

from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())

def screener_form(request):
    screener = open("myapp/static/screener.json").read()
    form = json.loads(screener)
    content = form.get("content", {})
    context = {
        'sections': content.get('sections', {}),
        'display_name': content.get('display_name', '')
    }
    for index, sec in enumerate(context['sections']):
        sec['total_questions'] = len(sec['questions'])
        context['sections'][index] = sec
    return render(request, 'screener_form.html', context)

def screener_endpoint(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        answers = data.get('answers', [])
        
        # Retrieve the domain mapping from the json file
        domains = open("myapp/static/domains.json").read()
        domain_mapping = json.loads(domains)
        question_to_domain = {}
        for dict in domain_mapping:
            question_to_domain[dict["question_id"]] = question_to_domain.get(dict["question_id"], []).append(dict["domain"])
        domain_scores = {}
        
        # Calculate the total score for each domain
        for answer in answers:
            value = answer.get('value', 0)
            question_id = answer.get('question_id', '')
            
            # Find the domain for the question
            domain = question_to_domain.get(question_id, None)
            
            if domain:
                domain_scores[domain] = domain_scores.get(domain, 0) + value
        
        assessments = []
        
        # Determine the Level-2 Assessments based on the total scores
        for domain, total_score in domain_scores.items():
            if domain == 'depression' and total_score >= 2:
                assessments.append('PHQ-9')
            elif domain == 'mania' and total_score >= 2:
                assessments.append('ASRM')
            elif domain == 'anxiety' and total_score >= 2:
                assessments.append('PHQ-9')
            elif domain == 'substance_use' and total_score >= 1:
                assessments.append('ASSIST')
        
        response_data = {'results': assessments}
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
