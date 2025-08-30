from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import models
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
    
    # Handle form submissions for adding new entities
    if request.method == 'POST':
        if 'add_diocese' in request.POST:
            # Handle diocese creation
            country = request.POST.get('country')
            name = request.POST.get('name')
            bishop_id = request.POST.get('bishop')

            if country and name:
                bishop = None
                if bishop_id:
                    try:
                        from members.models import Member
                        bishop = Member.objects.get(id=bishop_id)
                    except (Member.DoesNotExist, ImportError):
                        pass

                Diocese.objects.create(
                    country=country,
                    name=name,
                    bishop=bishop
                )
                messages.success(request, f'Diocese "{name}" added successfully!')
                return redirect('church_structure:index')
            else:
                messages.error(request, 'Diocese name and country are required.')

        elif 'add_pastorate' in request.POST:
            # Handle pastorate creation
            diocese_id = request.POST.get('diocese_id')
            name = request.POST.get('name')
            pastor_id = request.POST.get('pastor')

            if diocese_id and name:
                try:
                    diocese = Diocese.objects.get(id=diocese_id)
                    pastor = None
                    if pastor_id:
                        try:
                            from members.models import Member
                            pastor = Member.objects.get(id=pastor_id)
                        except (Member.DoesNotExist, ImportError):
                            pass

                    Pastorate.objects.create(
                        diocese=diocese,
                        name=name,
                        pastor=pastor
                    )
                    messages.success(request, f'Pastorate "{name}" added successfully!')
                    return redirect('church_structure:index')
                except Diocese.DoesNotExist:
                    messages.error(request, 'Selected Diocese not found.')
                except Exception as e:
                    messages.error(request, f'Error adding pastorate: {e}')
            else:
                messages.error(request, 'Pastorate name and associated Diocese are required.')

        elif 'add_church' in request.POST:
            # Handle church creation
            diocese_id = request.POST.get('diocese')
            pastorate_id = request.POST.get('pastorate_id')
            name = request.POST.get('name')
            address = request.POST.get('address')
            head_teacher_id = request.POST.get('head_teacher')
            teachers_ids = request.POST.getlist('teachers')
            service_times = request.POST.get('service_times')

            if pastorate_id and name and address:
                try:
                    pastorate = Pastorate.objects.get(id=pastorate_id)
                    head_teacher = None
                    if head_teacher_id:
                        try:
                            from members.models import Member
                            head_teacher = Member.objects.get(id=head_teacher_id)
                        except (Member.DoesNotExist, ImportError):
                            pass

                    church = Church.objects.create(
                        pastorate=pastorate,
                        name=name,
                        address=address,
                        head_teacher=head_teacher,
                        service_times=service_times or ''
                    )

                    # Add teachers if any were selected
                    if teachers_ids:
                        try:
                            from members.models import Member
                            teachers = Member.objects.filter(id__in=teachers_ids[:12])  # Limit to 12
                            church.teachers.set(teachers)
                        except ImportError:
                            pass
                    messages.success(request, f'Church "{name}" added successfully!')
                    return redirect('church_structure:index')
                except Pastorate.DoesNotExist:
                    messages.error(request, 'Selected Pastorate not found.')
                except Exception as e:
                    messages.error(request, f'Error adding church: {e}')
            else:
                messages.error(request, 'Church name, address, and associated Pastorate are required.')

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
        members = Member.objects.filter(user_home_church=church, is_active=True)
    except ImportError:
        members = []

    context = {
        'page_title': f'{church.name} Church',
        'church': church,
        'members': members,
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
        diocese_name = diocese.name
        diocese.delete()
        messages.success(request, f'Diocese "{diocese_name}" deleted successfully!')
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
        pastorate_name = pastorate.name
        pastorate.delete()
        messages.success(request, f'Pastorate "{pastorate_name}" deleted successfully!')
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
    """Deletediocese"""
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