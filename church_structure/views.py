
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Diocese, Pastorate, Church

def index(request):
    """Church structure main view"""
    dioceses = Diocese.objects.filter(is_active=True).order_by('country', 'name')
    pastorates = Pastorate.objects.filter(is_active=True).select_related('diocese')
    churches = Church.objects.filter(is_active=True).select_related('pastorate__diocese')
    
    # Statistics
    stats = {
        'total_dioceses': dioceses.count(),
        'total_pastorates': pastorates.count(),
        'total_churches': churches.count(),
        'countries': Diocese.objects.values_list('country', flat=True).distinct().count()
    }
    
    context = {
        'page_title': 'Church Structure',
        'dioceses': dioceses,
        'pastorates': pastorates[:10],  # Show recent 10
        'churches': churches[:10],      # Show recent 10
        'stats': stats,
    }
    return render(request, 'church_structure/index.html', context)

def get_pastorates(request, diocese_id):
    """API endpoint to get pastorates for a diocese"""
    pastorates = Pastorate.objects.filter(
        diocese_id=diocese_id, 
        is_active=True
    ).values('id', 'name')
    return JsonResponse(list(pastorates), safe=False)

def get_churches(request, pastorate_id):
    """API endpoint to get churches for a pastorate"""
    churches = Church.objects.filter(
        pastorate_id=pastorate_id, 
        is_active=True
    ).values('id', 'name')
    return JsonResponse(list(churches), safe=False)

def add_diocese(request):
    """Add new diocese"""
    if request.method == 'POST':
        name = request.POST.get('name')
        country = request.POST.get('country')
        bishop_name = request.POST.get('bishop_name')
        bishop_phone = request.POST.get('bishop_phone', '')
        bishop_email = request.POST.get('bishop_email', '')
        description = request.POST.get('description', '')
        
        if name and country and bishop_name:
            Diocese.objects.create(
                name=name,
                country=country,
                bishop_name=bishop_name,
                bishop_phone=bishop_phone,
                bishop_email=bishop_email,
                description=description
            )
            messages.success(request, f'Diocese "{name}" added successfully!')
        else:
            messages.error(request, 'Please fill in all required fields.')
        
        return redirect('church_structure:index')
    
    return redirect('church_structure:index')

def add_pastorate(request):
    """Add new pastorate"""
    if request.method == 'POST':
        name = request.POST.get('name')
        diocese_id = request.POST.get('diocese_id')
        pastor_name = request.POST.get('pastor_name')
        pastor_phone = request.POST.get('pastor_phone', '')
        pastor_email = request.POST.get('pastor_email', '')
        description = request.POST.get('description', '')
        
        if name and diocese_id and pastor_name:
            try:
                diocese = Diocese.objects.get(id=diocese_id)
                Pastorate.objects.create(
                    name=name,
                    diocese=diocese,
                    pastor_name=pastor_name,
                    pastor_phone=pastor_phone,
                    pastor_email=pastor_email,
                    description=description
                )
                messages.success(request, f'Pastorate "{name}" added successfully!')
            except Diocese.DoesNotExist:
                messages.error(request, 'Selected diocese does not exist.')
        else:
            messages.error(request, 'Please fill in all required fields.')
        
        return redirect('church_structure:index')
    
    return redirect('church_structure:index')

def add_church(request):
    """Add new church"""
    if request.method == 'POST':
        name = request.POST.get('name')
        pastorate_id = request.POST.get('pastorate_id')
        address = request.POST.get('address')
        head_teacher_name = request.POST.get('head_teacher_name')
        head_teacher_phone = request.POST.get('head_teacher_phone', '')
        head_teacher_email = request.POST.get('head_teacher_email', '')
        assistant_teachers = request.POST.get('assistant_teachers', '')
        service_times = request.POST.get('service_times', '')
        
        if name and pastorate_id and address and head_teacher_name:
            try:
                pastorate = Pastorate.objects.get(id=pastorate_id)
                Church.objects.create(
                    name=name,
                    pastorate=pastorate,
                    address=address,
                    head_teacher_name=head_teacher_name,
                    head_teacher_phone=head_teacher_phone,
                    head_teacher_email=head_teacher_email,
                    assistant_teachers=assistant_teachers,
                    service_times=service_times
                )
                messages.success(request, f'Church "{name}" added successfully!')
            except Pastorate.DoesNotExist:
                messages.error(request, 'Selected pastorate does not exist.')
        else:
            messages.error(request, 'Please fill in all required fields.')
        
        return redirect('church_structure:index')
    
    return redirect('church_structure:index')
