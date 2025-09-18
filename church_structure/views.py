from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Diocese, Pastorate, Church
from .forms import DioceseForm, PastorateForm, ChurchForm, MemberSearchForm
from members.models import Member

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

@login_required
def add_diocese(request):
    """Add new diocese"""
    if request.method == 'POST':
        form = DioceseForm(request.POST)
        if form.is_valid():
            diocese = form.save()
            messages.success(request, f'Diocese "{diocese.name}" added successfully!')
            return redirect('church_structure:index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DioceseForm()

    return render(request, 'church_structure/add_diocese.html', {'form': form})

@login_required
def add_pastorate(request):
    """Add new pastorate"""
    if request.method == 'POST':
        form = PastorateForm(request.POST)
        if form.is_valid():
            pastorate = form.save()
            messages.success(request, f'Pastorate "{pastorate.name}" added successfully!')
            return redirect('church_structure:index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PastorateForm()

    return render(request, 'church_structure/add_pastorate.html', {'form': form})

@login_required
def add_church(request):
    """Add new church"""
    if request.method == 'POST':
        form = ChurchForm(request.POST)
        if form.is_valid():
            church = form.save()
            messages.success(request, f'Church "{church.name}" added successfully!')
            return redirect('church_structure:index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ChurchForm()

    return render(request, 'church_structure/add_church.html', {'form': form})

@login_required
def diocese_detail(request, diocese_slug):
    """Diocese detail view with all pastorates and churches"""
    diocese = get_object_or_404(Diocese, slug=diocese_slug)
    pastorates = diocese.pastorates.filter(is_active=True).prefetch_related('churches')
    
    # Get Archbishop (member with dean_archbishop role)
    archbishop = None
    if hasattr(Member, 'church_clergy_roles'):
        archbishop = Member.objects.filter(
            church_clergy_roles__contains=['dean_archbishop'],
            membership_status='Active'
        ).order_by('-updated_at', 'first_name').first()
    
    # Get King (member with dean_king role)
    king = None
    if hasattr(Member, 'special_clergy_roles'):
        king = Member.objects.filter(
            special_clergy_roles__contains=['dean_king'],
            membership_status='Active'
        ).order_by('-updated_at', 'first_name').first()
    
    # Get Diocesan Church for this diocese
    diocesan_church = Church.objects.filter(
        pastorate__diocese=diocese,
        is_diosen_church=True,
        is_active=True
    ).order_by('-updated_at', 'name').first()

    context = {
        'page_title': f'{diocese.name} Diocese',
        'diocese': diocese,
        'pastorates': pastorates,
        'archbishop': archbishop,
        'king': king,
        'diocesan_church': diocesan_church,
    }
    return render(request, 'church_structure/diocese_detail.html', context)

@login_required
def pastorate_detail(request, pastorate_slug):
    """Pastorate detail view with all churches"""
    pastorate = get_object_or_404(Pastorate, slug=pastorate_slug)
    churches = pastorate.churches.filter(is_active=True)
    
    # Get Archbishop (member with dean_archbishop role)
    archbishop = None
    try:
        archbishop = Member.objects.filter(
            church_clergy_roles__contains=['dean_archbishop'],
            membership_status='Active'
        ).first()
    except:
        pass
    
    # Get King (member with dean_king role)
    king = None
    try:
        king = Member.objects.filter(
            special_clergy_roles__contains=['dean_king'],
            membership_status='Active'
        ).first()
    except:
        pass
    
    # Get Diocesan Church for this diocese
    diocesan_church = None
    try:
        diocesan_church = Church.objects.filter(
            pastorate__diocese=pastorate.diocese,
            is_diosen_church=True,
            is_active=True
        ).first()
    except:
        pass

    context = {
        'page_title': f'{pastorate.name} Pastorate',
        'pastorate': pastorate,
        'churches': churches,
        'archbishop': archbishop,
        'king': king,
        'diocesan_church': diocesan_church,
    }
    return render(request, 'church_structure/pastorate_detail.html', context)

@login_required
def church_detail(request, church_slug):
    """Church detail view with teachers and members"""
    church = get_object_or_404(Church, slug=church_slug)
    # Get members from this church if members app is available
    try:
        from members.models import Member
        members = Member.objects.filter(user_home_church=church, membership_status='Active')
    except ImportError:
        members = []
    
    # Get Archbishop (member with dean_archbishop role)
    archbishop = None
    try:
        archbishop = Member.objects.filter(
            church_clergy_roles__contains=['dean_archbishop'],
            membership_status='Active'
        ).first()
    except:
        pass
    
    # Get King (member with dean_king role)
    king = None
    try:
        king = Member.objects.filter(
            special_clergy_roles__contains=['dean_king'],
            membership_status='Active'
        ).first()
    except:
        pass
    
    # Get Diocesan Church for this diocese
    diocesan_church = None
    try:
        diocesan_church = Church.objects.filter(
            pastorate__diocese=church.pastorate.diocese,
            is_diosen_church=True,
            is_active=True
        ).first()
    except:
        pass
    
    # Get Mission Church for this pastorate/diocese
    mission_church = None
    try:
        mission_church = Church.objects.filter(
            pastorate__diocese=church.pastorate.diocese,
            is_mission_church=True,
            is_active=True
        ).first()
    except:
        pass

    context = {
        'page_title': f'{church.name} Church',
        'church': church,
        'members': members,
        'archbishop': archbishop,
        'king': king,
        'diocesan_church': diocesan_church,
        'mission_church': mission_church,
    }
    return render(request, 'church_structure/church_detail.html', context)

@login_required
def add_diocese(request):
    """Add new diocese"""
    if request.method == 'POST':
        form = DioceseForm(request.POST)
        if form.is_valid():
            diocese = form.save()
            messages.success(request, f'Diocese "{diocese.name}" added successfully!')
            return redirect('church_structure:index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DioceseForm()

    context = {
        'page_title': 'Add New Diocese',
        'form': form,
    }
    return render(request, 'church_structure/add_diocese.html', context)

@login_required
def diocese_detail(request, diocese_slug):
    """Diocese detail view"""
    diocese = get_object_or_404(Diocese, slug=diocese_slug)
    pastorates = diocese.pastorates.filter(is_active=True)
    
    context = {
        'page_title': f'{diocese.name} Diocese',
        'diocese': diocese,
        'pastorates': pastorates,
    }
    return render(request, 'church_structure/diocese_detail.html', context)

@login_required
def edit_diocese(request, diocese_slug):
    """Edit diocese"""
    diocese = get_object_or_404(Diocese, slug=diocese_slug)

    if request.method == 'POST':
        form = DioceseForm(request.POST, instance=diocese)
        if form.is_valid():
            diocese = form.save()
            messages.success(request, f'Diocese "{diocese.name}" updated successfully!')
            return redirect('church_structure:diocese_detail', diocese_slug=diocese.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DioceseForm(instance=diocese)

    context = {
        'page_title': f'Edit {diocese.name} Diocese',
        'form': form,
        'diocese': diocese,
    }
    return render(request, 'church_structure/edit_diocese.html', context)

@login_required
def pastorate_detail(request, pastorate_slug):
    """Pastorate detail view"""
    pastorate = get_object_or_404(Pastorate, slug=pastorate_slug)
    churches = pastorate.churches.filter(is_active=True)
    
    context = {
        'page_title': f'{pastorate.name} Pastorate',
        'pastorate': pastorate,
        'churches': churches,
    }
    return render(request, 'church_structure/pastorate_detail.html', context)

@login_required
def edit_pastorate(request, pastorate_slug):
    """Edit pastorate"""
    pastorate = get_object_or_404(Pastorate, slug=pastorate_slug)

    if request.method == 'POST':
        form = PastorateForm(request.POST, instance=pastorate)
        if form.is_valid():
            pastorate = form.save()
            messages.success(request, f'Pastorate "{pastorate.name}" updated successfully!')
            return redirect('church_structure:pastorate_detail', pastorate_slug=pastorate.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PastorateForm(instance=pastorate)

    context = {
        'page_title': f'Edit {pastorate.name} Pastorate',
        'form': form,
        'pastorate': pastorate,
    }
    return render(request, 'church_structure/edit_pastorate.html', context)

@login_required
def edit_church(request, church_slug):
    """Edit church"""
    church = get_object_or_404(Church, slug=church_slug)

    if request.method == 'POST':
        form = ChurchForm(request.POST, instance=church)
        if form.is_valid():
            church = form.save()
            messages.success(request, f'Church "{church.name}" updated successfully!')
            return redirect('church_structure:church_detail', church_slug=church.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ChurchForm(instance=church)

    context = {
        'page_title': f'Edit {church.name} Church',
        'form': form,
        'church': church,
    }
    return render(request, 'church_structure/edit_church.html', context)

@login_required
def get_pastorates(request, diocese_id):
    """Get pastorates for a specific diocese"""
    pastorates = Pastorate.objects.filter(
        diocese_id=diocese_id, 
        is_active=True
    ).values('id', 'name').order_by('name')
    return JsonResponse(list(pastorates), safe=False)

@login_required
def get_churches(request, pastorate_id):
    """Get churches for a specific pastorate"""
    churches = Church.objects.filter(
        pastorate_id=pastorate_id, 
        is_active=True
    ).values('id', 'name').order_by('name')
    return JsonResponse(list(churches), safe=False)

@login_required
def search_members(request):
    """AJAX endpoint for member search"""
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    members = Member.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(username__icontains=query) |
        Q(phone_number__icontains=query),
        membership_status='Active'
    ).values('id', 'first_name', 'last_name', 'phone_number', 'email_address')[:20]
    
    # Format for select2 or similar
    results = []
    for member in members:
        results.append({
            'id': member['id'],
            'text': f"{member['first_name']} {member['last_name']} ({member['phone_number']})",
            'phone': member['phone_number'],
            'email': member['email_address'] or ''
        })
    
    return JsonResponse(results, safe=False)

@login_required
def delete_diocese(request, diocese_slug):
    """Delete diocese"""
    diocese = get_object_or_404(Diocese, slug=diocese_slug)
    
    if request.method == 'POST':
        diocese_name = diocese.name
        diocese.delete()
        messages.success(request, f'Diocese "{diocese_name}" deleted successfully!')
        return redirect('church_structure:index')
    
    context = {
        'page_title': f'Delete {diocese.name} Diocese',
        'diocese': diocese,
    }
    return render(request, 'church_structure/delete_diocese.html', context)

@login_required
def delete_pastorate(request, pastorate_slug):
    """Delete pastorate"""
    pastorate = get_object_or_404(Pastorate, slug=pastorate_slug)
    
    if request.method == 'POST':
        pastorate_name = pastorate.name
        pastorate.delete()
        messages.success(request, f'Pastorate "{pastorate_name}" deleted successfully!')
        return redirect('church_structure:index')
    
    context = {
        'page_title': f'Delete {pastorate.name} Pastorate',
        'pastorate': pastorate,
    }
    return render(request, 'church_structure/delete_pastorate.html', context)

@login_required
def delete_church(request, church_slug):
    """Delete church"""
    church = get_object_or_404(Church, slug=church_slug)
    
    if request.method == 'POST':
        church_name = church.name
        church.delete()
        messages.success(request, f'Church "{church_name}" deleted successfully!')
        return redirect('church_structure:index')
    
    context = {
        'page_title': f'Delete {church.name} Church',
        'church': church,
    }
    return render(request, 'church_structure/delete_church.html', context)

@login_required
def edit_pastorate(request, pastorate_slug):
    """Edit pastorate"""
    pastorate = get_object_or_404(Pastorate, slug=pastorate_slug)
    
    if request.method == 'POST':
        form = PastorateForm(request.POST, instance=pastorate)
        if form.is_valid():
            pastorate = form.save()
            messages.success(request, f'Pastorate "{pastorate.name}" updated successfully!')
            return redirect('church_structure:pastorate_detail', pastorate_slug=pastorate.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PastorateForm(instance=pastorate)

    context = {
        'page_title': f'Edit {pastorate.name} Pastorate',
        'form': form,
        'pastorate': pastorate,
    }
    return render(request, 'church_structure/edit_pastorate.html', context)

@login_required
def edit_church(request, church_slug):
    """Edit church"""
    church = get_object_or_404(Church, slug=church_slug)
    
    if request.method == 'POST':
        form = ChurchForm(request.POST, instance=church)
        if form.is_valid():
            church = form.save()
            messages.success(request, f'Church "{church.name}" updated successfully!')
            return redirect('church_structure:church_detail', church_slug=church.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ChurchForm(instance=church)

    context = {
        'page_title': f'Edit {church.name} Church',
        'form': form,
        'church': church,
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

@login_required
def search_members(request):
    """AJAX endpoint for member search"""
    if request.method == 'GET':
        search_term = request.GET.get('search', '')
        if len(search_term) >= 2:
            members = Member.objects.filter(
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term) |
                Q(username__icontains=search_term) |
                Q(phone_number__icontains=search_term),
                membership_status='Active'
            ).distinct()[:20]

            member_data = []
            for member in members:
                member_data.append({
                    'id': member.id,
                    'name': member.full_name,
                    'username': member.username,
                    'phone': member.phone_number,
                    'email': member.email_address,
                    'church': member.home_church_hierarchy
                })

            return JsonResponse({'members': member_data})

    return JsonResponse({'members': []})

@login_required
def diocese_description(request, diocese_slug):
    """Diocese detailed description view"""
    diocese = get_object_or_404(Diocese, slug=diocese_slug)
    
    # Get Archbishop (member with dean_archbishop role)
    archbishop = None
    try:
        archbishop = Member.objects.filter(
            church_clergy_roles__contains=['dean_archbishop'],
            membership_status='Active'
        ).first()
    except:
        pass
    
    # Get King (member with dean_king role)
    king = None
    try:
        king = Member.objects.filter(
            special_clergy_roles__contains=['dean_king'],
            membership_status='Active'
        ).first()
    except:
        pass
    
    # Get Diocesan Church for this diocese
    diocesan_church = None
    try:
        diocesan_church = Church.objects.filter(
            pastorate__diocese=diocese,
            is_diosen_church=True,
            is_active=True
        ).first()
    except:
        pass
    
    context = {
        'page_title': f'{diocese.name} Diocese - About',
        'diocese': diocese,
        'archbishop': archbishop,
        'king': king,
        'diocesan_church': diocesan_church,
    }
    return render(request, 'church_structure/diocese_description.html', context)

@login_required
def pastorate_description(request, pastorate_slug):
    """Pastorate detailed description view"""
    pastorate = get_object_or_404(Pastorate, slug=pastorate_slug)
    
    # Get Archbishop (member with dean_archbishop role)
    archbishop = None
    try:
        archbishop = Member.objects.filter(
            church_clergy_roles__contains=['dean_archbishop'],
            membership_status='Active'
        ).first()
    except:
        pass
    
    # Get King (member with dean_king role)
    king = None
    try:
        king = Member.objects.filter(
            special_clergy_roles__contains=['dean_king'],
            membership_status='Active'
        ).first()
    except:
        pass
    
    # Get Diocesan Church for this diocese
    diocesan_church = None
    try:
        diocesan_church = Church.objects.filter(
            pastorate__diocese=pastorate.diocese,
            is_diosen_church=True,
            is_active=True
        ).first()
    except:
        pass
    
    context = {
        'page_title': f'{pastorate.name} Pastorate - About',
        'pastorate': pastorate,
        'archbishop': archbishop,
        'king': king,
        'diocesan_church': diocesan_church,
    }
    return render(request, 'church_structure/pastorate_description.html', context)

@login_required
def church_description(request, church_slug):
    """Church detailed description view"""
    church = get_object_or_404(Church, slug=church_slug)
    
    # Get Archbishop (member with dean_archbishop role)
    archbishop = None
    try:
        archbishop = Member.objects.filter(
            church_clergy_roles__contains=['dean_archbishop'],
            membership_status='Active'
        ).first()
    except:
        pass
    
    # Get King (member with dean_king role)
    king = None
    try:
        king = Member.objects.filter(
            special_clergy_roles__contains=['dean_king'],
            membership_status='Active'
        ).first()
    except:
        pass
    
    # Get Diocesan Church for this diocese
    diocesan_church = None
    try:
        diocesan_church = Church.objects.filter(
            pastorate__diocese=church.pastorate.diocese,
            is_diosen_church=True,
            is_active=True
        ).first()
    except:
        pass
    
    # Get Mission Church for this pastorate/diocese
    mission_church = None
    try:
        mission_church = Church.objects.filter(
            pastorate__diocese=church.pastorate.diocese,
            is_mission_church=True,
            is_active=True
        ).first()
    except:
        pass
    
    context = {
        'page_title': f'{church.name} Church - About',
        'church': church,
        'archbishop': archbishop,
        'king': king,
        'diocesan_church': diocesan_church,
        'mission_church': mission_church,
    }
    return render(request, 'church_structure/church_description.html', context)