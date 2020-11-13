def tags(request):
    return {
        'breakfast': request.GET.get('breakfast'),
        'lunch': request.GET.get('lunch'),
        'dinner': request.GET.get('dinner'),
    }
