from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Diocese, Pastorate, Church

@login_required
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

@login_required
def diocese_detail(request, diocese_slug):
    """Diocese detail view with all pastorates and churches"""
    diocese = get_object_or_404(Diocese, slug=diocese_slug)
    pastorates = diocese.pastorates.filter(is_active=True).prefetch_related('churches')

    context = {
        'page_title': f'{diocese.name} Diocese',
        'diocese': diocese,
        'pastorates': pastorates,
    }
    return render(request, 'church_structure/diocese_detail.html', context)

@login_required
def pastorate_detail(request, pastorate_slug):
    """Pastorate detail view with all churches"""
    pastorate = get_object_or_404(Pastorate, slug=pastorate_slug)
    churches = pastorate.churches.filter(is_active=True)

    context = {
        'page_title': f'{pastorate.name} Pastorate',
        'pastorate': pastorate,
        'churches': churches,
    }
    return render(request, 'church_structure/pastorate_detail.html', context)

@login_required
def church_detail(request, church_slug):
    """Church detail view with teachers and members"""
    church = get_object_or_404(Church, slug=church_slug)
    # Get members from this church if members app is available
    try:
        from members.models import Member
        members = Member.objects.filter(home_church=church, is_active=True)
    except ImportError:
        members = []

    context = {
        'page_title': f'{church.name} Church',
        'church': church,
        'members': members,
    }
    return render(request, 'church_structure/church_detail.html', context)

@login_required
def edit_diocese(request, diocese_slug):
    """Edit diocese"""
    diocese = get_object_or_404(Diocese, slug=diocese_slug)

    if request.method == 'POST':
        diocese.name = request.POST.get('name', diocese.name)
        diocese.country = request.POST.get('country', diocese.country)
        diocese.bishop_name = request.POST.get('bishop_name', diocese.bishop_name)
        diocese.bishop_phone = request.POST.get('bishop_phone', diocese.bishop_phone)
        diocese.bishop_email = request.POST.get('bishop_email', diocese.bishop_email)
        diocese.description = request.POST.get('description', diocese.description)
        diocese.save()
        messages.success(request, f'Diocese "{diocese.name}" updated successfully!')
        return redirect('church_structure:diocese_detail', diocese_slug=diocese.slug)

    context = {
        'page_title': f'Edit {diocese.name} Diocese',
        'diocese': diocese,
    }
    return render(request, 'church_structure/edit_diocese.html', context)

@login_required
def edit_pastorate(request, pastorate_slug):
    """Edit pastorate"""
    pastorate = get_object_or_404(Pastorate, slug=pastorate_slug)
    dioceses = Diocese.objects.filter(is_active=True)

    if request.method == 'POST':
        pastorate.name = request.POST.get('name', pastorate.name)
        diocese_id = request.POST.get('diocese_id')
        if diocese_id:
            pastorate.diocese = get_object_or_404(Diocese, id=diocese_id)
        pastorate.pastor_name = request.POST.get('pastor_name', pastorate.pastor_name)
        pastorate.pastor_phone = request.POST.get('pastor_phone', pastorate.pastor_phone)
        pastorate.pastor_email = request.POST.get('pastor_email', pastorate.pastor_email)
        pastorate.description = request.POST.get('description', pastorate.description)
        pastorate.save()
        messages.success(request, f'Pastorate "{pastorate.name}" updated successfully!')
        return redirect('church_structure:pastorate_detail', pastorate_slug=pastorate.slug)

    context = {
        'page_title': f'Edit {pastorate.name} Pastorate',
        'pastorate': pastorate,
        'dioceses': dioceses,
    }
    return render(request, 'church_structure/edit_pastorate.html', context)

@login_required
def edit_church(request, church_slug):
    """Edit church"""
    church = get_object_or_404(Church, slug=church_slug)
    dioceses = Diocese.objects.filter(is_active=True)
    pastorates = Pastorate.objects.filter(is_active=True)

    if request.method == 'POST':
        church.name = request.POST.get('name', church.name)
        pastorate_id = request.POST.get('pastorate_id')
        if pastorate_id:
            church.pastorate = get_object_or_404(Pastorate, id=pastorate_id)
        church.address = request.POST.get('address', church.address)
        church.head_teacher_name = request.POST.get('head_teacher_name', church.head_teacher_name)
        church.head_teacher_phone = request.POST.get('head_teacher_phone', church.head_teacher_phone)
        church.head_teacher_email = request.POST.get('head_teacher_email', church.head_teacher_email)
        church.assistant_teachers = request.POST.get('assistant_teachers', church.assistant_teachers)
        church.service_times = request.POST.get('service_times', church.service_times)
        church.save()
        messages.success(request, f'Church "{church.name}" updated successfully!')
        return redirect('church_structure:church_detail', church_slug=church.slug)

    context = {
        'page_title': f'Edit {church.name} Church',
        'church': church,
        'dioceses': dioceses,
        'pastorates': pastorates,
    }
    return render(request, 'church_structure/edit_church.html', context)

@login_required
def delete_diocese(request, diocese_slug):
    """Delete diocese"""
    diocese = get_object_or_404(Diocese, slug=diocese_slug)

    if request.method == 'POST':
        name = diocese.name
        diocese.delete()
        messages.success(request, f'Diocese "{name}" deleted successfully!')
        return redirect('church_structure:index')

    context = {
        'page_title': f'Delete {diocese.name} Diocese',
        'diocese': diocese,
        'pastorates_count': diocese.pastorates.count(),
    }
    return render(request, 'church_structure/delete_diocese.html', context)

@login_required
def delete_pastorate(request, pastorate_slug):
    """Delete pastorate"""
    pastorate = get_object_or_404(Pastorate, slug=pastorate_slug)

    if request.method == 'POST':
        name = pastorate.name
        pastorate.delete()
        messages.success(request, f'Pastorate "{name}" deleted successfully!')
        return redirect('church_structure:index')

    context = {
        'page_title': f'Delete {pastorate.name} Pastorate',
        'pastorate': pastorate,
        'churches_count': pastorate.churches.count(),
    }
    return render(request, 'church_structure/delete_pastorate.html', context)

@login_required
def delete_church(request, church_slug):
    """Delete church"""
    church = get_object_or_404(Church, slug=church_slug)

    if request.method == 'POST':
        name = church.name
        church.delete()
        messages.success(request, f'Church "{name}" deleted successfully!')
        return redirect('church_structure:index')

    context = {
        'page_title': f'Delete {church.name} Church',
        'church': church,
    }
    return render(request, 'church_structure/delete_church.html', context)