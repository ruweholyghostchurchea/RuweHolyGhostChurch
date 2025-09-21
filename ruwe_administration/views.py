from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db import transaction
from .models import (
    # Church Level
    ChurchMainOffice, ChurchYouthOffice, ChurchDevelopmentOffice, 
    ChurchTravelOffice, ChurchDisciplinaryOffice,
    # Pastorate Level
    PastorateMainOffice, PastorateYouthOffice, PastorateTeachersOffice,
    # Diocese Level
    DioceseMainOffice, DioceseYouthOffice, DioceseTeachersOffice,
    # Dean Level
    DeanManagementOffice, DeanOrganizingSecretaryOffice, DeanYouthOffice,
    DeanKingsOffice, DeanArchbishopsOffice, DeanBishopsOffice, DeanPastorsOffice,
    DeanLayReadersOffice, DeanDivisionsOffice, DeanTeachersOffice, DeanWomenLeadersOffice,
    DeanEldersOffice, DeanSosoOffice, DeanCoursesOffice, DeanEcclesiasticalVestmentOffice,
    DeanEcclesiasticalCrossOffice, DeanChaplaincyOffice, DeanChurchesDataRecordsOffice,
    DeanEducationGenderEqualityOffice, DeanDevelopmentOffice, DeanDisciplinaryCommitteeOffice,
    DeanArbitrationCommitteeOffice, DeanHealthCounsellingOffice, DeanChurchesProtocolOffice,
    DeanMediaPublicityOffice
)
from .forms import (
    # Church Level Forms
    ChurchMainOfficeForm, ChurchYouthOfficeForm, ChurchDevelopmentOfficeForm,
    ChurchTravelOfficeForm, ChurchDisciplinaryOfficeForm,
    # Pastorate Level Forms
    PastorateMainOfficeForm, PastorateYouthOfficeForm, PastorateTeachersOfficeForm,
    # Diocese Level Forms
    DioceseMainOfficeForm, DioceseYouthOfficeForm, DioceseTeachersOfficeForm,
    # Dean Level Forms
    DeanManagementOfficeForm, DeanOrganizingSecretaryOfficeForm, DeanYouthOfficeForm,
    DeanKingsOfficeForm, DeanArchbishopsOfficeForm, DeanBishopsOfficeForm, DeanPastorsOfficeForm,
    DeanLayReadersOfficeForm, DeanDivisionsOfficeForm, DeanTeachersOfficeForm, DeanWomenLeadersOfficeForm,
    DeanEldersOfficeForm, DeanSosoOfficeForm, DeanCoursesOfficeForm, DeanEcclesiasticalVestmentOfficeForm,
    DeanEcclesiasticalCrossOfficeForm, DeanChaplaincyOfficeForm, DeanChurchesDataRecordsOfficeForm,
    DeanEducationGenderEqualityOfficeForm, DeanDevelopmentOfficeForm, DeanDisciplinaryCommitteeOfficeForm,
    DeanArbitrationCommitteeOfficeForm, DeanHealthCounsellingOfficeForm, DeanChurchesProtocolOfficeForm,
    DeanMediaPublicityOfficeForm
)
from church_structure.models import Church, Pastorate, Diocese
from members.models import Member


@login_required
def administration_index(request):
    """Main administration index page with statistics and office cards"""
    
    # Calculate statistics for each level
    church_stats = {
        'main_offices': ChurchMainOffice.objects.count(),
        'youth_offices': ChurchYouthOffice.objects.count(),
        'development_offices': ChurchDevelopmentOffice.objects.count(),
        'travel_offices': ChurchTravelOffice.objects.count(),
        'disciplinary_offices': ChurchDisciplinaryOffice.objects.count(),
        'total': sum([
            ChurchMainOffice.objects.count(),
            ChurchYouthOffice.objects.count(),
            ChurchDevelopmentOffice.objects.count(),
            ChurchTravelOffice.objects.count(),
            ChurchDisciplinaryOffice.objects.count()
        ])
    }
    
    pastorate_stats = {
        'main_offices': PastorateMainOffice.objects.count(),
        'youth_offices': PastorateYouthOffice.objects.count(),
        'teachers_offices': PastorateTeachersOffice.objects.count(),
        'total': sum([
            PastorateMainOffice.objects.count(),
            PastorateYouthOffice.objects.count(),
            PastorateTeachersOffice.objects.count()
        ])
    }
    
    diocese_stats = {
        'main_offices': DioceseMainOffice.objects.count(),
        'youth_offices': DioceseYouthOffice.objects.count(),
        'teachers_offices': DioceseTeachersOffice.objects.count(),
        'total': sum([
            DioceseMainOffice.objects.count(),
            DioceseYouthOffice.objects.count(),
            DioceseTeachersOffice.objects.count()
        ])
    }
    
    # Dean level statistics (all 25 offices)
    dean_stats = {
        'management': DeanManagementOffice.objects.count(),
        'organizing_secretary': DeanOrganizingSecretaryOffice.objects.count(),
        'youth': DeanYouthOffice.objects.count(),
        'kings': DeanKingsOffice.objects.count(),
        'archbishops': DeanArchbishopsOffice.objects.count(),
        'bishops': DeanBishopsOffice.objects.count(),
        'pastors': DeanPastorsOffice.objects.count(),
        'lay_readers': DeanLayReadersOffice.objects.count(),
        'divisions': DeanDivisionsOffice.objects.count(),
        'teachers': DeanTeachersOffice.objects.count(),
        'women_leaders': DeanWomenLeadersOffice.objects.count(),
        'elders': DeanEldersOffice.objects.count(),
        'soso': DeanSosoOffice.objects.count(),
        'courses': DeanCoursesOffice.objects.count(),
        'ecclesiastical_vestment': DeanEcclesiasticalVestmentOffice.objects.count(),
        'ecclesiastical_cross': DeanEcclesiasticalCrossOffice.objects.count(),
        'chaplaincy': DeanChaplaincyOffice.objects.count(),
        'churches_data_records': DeanChurchesDataRecordsOffice.objects.count(),
        'education_gender_equality': DeanEducationGenderEqualityOffice.objects.count(),
        'development': DeanDevelopmentOffice.objects.count(),
        'disciplinary_committee': DeanDisciplinaryCommitteeOffice.objects.count(),
        'arbitration_committee': DeanArbitrationCommitteeOffice.objects.count(),
        'health_counselling': DeanHealthCounsellingOffice.objects.count(),
        'churches_protocol': DeanChurchesProtocolOffice.objects.count(),
        'media_publicity': DeanMediaPublicityOffice.objects.count(),
    }
    dean_stats['total'] = sum(dean_stats.values())
    
    # Grand total across all levels
    grand_total = church_stats['total'] + pastorate_stats['total'] + diocese_stats['total'] + dean_stats['total']
    
    # Get all churches, pastorates, and dioceses for dropdown menus
    churches = Church.objects.select_related('pastorate__diocese').all()
    pastorates = Pastorate.objects.select_related('diocese').all()
    dioceses = Diocese.objects.all()
    
    context = {
        'church_stats': church_stats,
        'pastorate_stats': pastorate_stats,
        'diocese_stats': diocese_stats,
        'dean_stats': dean_stats,
        'grand_total': grand_total,
        'churches': churches,
        'pastorates': pastorates,
        'dioceses': dioceses,
    }
    
    return render(request, 'ruwe_administration/index.html', context)


# ========================================
# GENERIC VIEW FUNCTIONS FOR CRUD OPERATIONS
# ========================================

def get_office_or_none(model_class, **kwargs):
    """Get office instance or None if it doesn't exist"""
    try:
        return model_class.objects.get(**kwargs)
    except model_class.DoesNotExist:
        return None

def handle_office_form(request, form_class, office_instance=None, template_name='', redirect_name=''):
    """Generic function to handle office forms (add/edit)"""
    if request.method == 'POST':
        form = form_class(request.POST, instance=office_instance)
        if form.is_valid():
            with transaction.atomic():
                office = form.save()
                action = 'updated' if office_instance else 'created'
                messages.success(request, f'{office.name} has been {action} successfully.')
                return redirect(redirect_name)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = form_class(instance=office_instance)
    
    return render(request, template_name, {'form': form, 'office': office_instance})


# =========================
# CHURCH LEVEL VIEWS (5)
# =========================

@login_required
def church_main_office_detail(request, church_id):
    church = get_object_or_404(Church, id=church_id)
    office = get_office_or_none(ChurchMainOffice, church=church)
    return render(request, 'ruwe_administration/church/main_detail.html', {
        'church': church, 'office': office
    })

@login_required
def church_main_office_add(request, church_id):
    church = get_object_or_404(Church, id=church_id)
    if request.method == 'POST':
        form = ChurchMainOfficeForm(request.POST)
        if form.is_valid():
            office = form.save(commit=False)
            office.church = church
            office.name = f"{church.name} Main Office"
            office.save()
            form.save_m2m()
            messages.success(request, f'{office.name} has been created successfully.')
            return redirect('ruwe_administration:church_main_detail', church_id=church.id)
    else:
        form = ChurchMainOfficeForm(initial={'church': church})
    
    return render(request, 'ruwe_administration/church/main_form.html', {
        'form': form, 'church': church, 'action': 'Add'
    })

@login_required
def church_main_office_edit(request, pk):
    office = get_object_or_404(ChurchMainOffice, pk=pk)
    if request.method == 'POST':
        form = ChurchMainOfficeForm(request.POST, instance=office)
        if form.is_valid():
            office = form.save()
            messages.success(request, f'{office.name} has been updated successfully.')
            return redirect('ruwe_administration:church_main_detail', church_id=office.church.id)
    else:
        form = ChurchMainOfficeForm(instance=office)
    
    return render(request, 'ruwe_administration/church/main_form.html', {
        'form': form, 'church': office.church, 'office': office, 'action': 'Edit'
    })

@login_required
def church_youth_office_detail(request, church_id):
    church = get_object_or_404(Church, id=church_id)
    office = get_office_or_none(ChurchYouthOffice, church=church)
    return render(request, 'ruwe_administration/church/youth_detail.html', {
        'church': church, 'office': office
    })

@login_required
def church_youth_office_add(request, church_id):
    church = get_object_or_404(Church, id=church_id)
    if request.method == 'POST':
        form = ChurchYouthOfficeForm(request.POST)
        if form.is_valid():
            office = form.save(commit=False)
            office.church = church
            office.name = f"{church.name} Youth Office"
            office.save()
            form.save_m2m()
            messages.success(request, f'{office.name} has been created successfully.')
            return redirect('ruwe_administration:church_youth_detail', church_id=church.id)
    else:
        form = ChurchYouthOfficeForm(initial={'church': church})
    
    return render(request, 'ruwe_administration/church/youth_form.html', {
        'form': form, 'church': church, 'action': 'Add'
    })

@login_required
def church_youth_office_edit(request, pk):
    office = get_object_or_404(ChurchYouthOffice, pk=pk)
    if request.method == 'POST':
        form = ChurchYouthOfficeForm(request.POST, instance=office)
        if form.is_valid():
            office = form.save()
            messages.success(request, f'{office.name} has been updated successfully.')
            return redirect('ruwe_administration:church_youth_detail', church_id=office.church.id)
    else:
        form = ChurchYouthOfficeForm(instance=office)
    
    return render(request, 'ruwe_administration/church/youth_form.html', {
        'form': form, 'church': office.church, 'office': office, 'action': 'Edit'
    })

@login_required
def church_development_office_detail(request, church_id):
    church = get_object_or_404(Church, id=church_id)
    office = get_office_or_none(ChurchDevelopmentOffice, church=church)
    return render(request, 'ruwe_administration/church/development_detail.html', {
        'church': church, 'office': office
    })

@login_required
def church_development_office_add(request, church_id):
    church = get_object_or_404(Church, id=church_id)
    if request.method == 'POST':
        form = ChurchDevelopmentOfficeForm(request.POST)
        if form.is_valid():
            office = form.save(commit=False)
            office.church = church
            office.name = f"{church.name} Development Office"
            office.save()
            form.save_m2m()
            messages.success(request, f'{office.name} has been created successfully.')
            return redirect('ruwe_administration:church_development_detail', church_id=church.id)
    else:
        form = ChurchDevelopmentOfficeForm(initial={'church': church})
    
    return render(request, 'ruwe_administration/church/development_form.html', {
        'form': form, 'church': church, 'action': 'Add'
    })

@login_required
def church_development_office_edit(request, pk):
    office = get_object_or_404(ChurchDevelopmentOffice, pk=pk)
    if request.method == 'POST':
        form = ChurchDevelopmentOfficeForm(request.POST, instance=office)
        if form.is_valid():
            office = form.save()
            messages.success(request, f'{office.name} has been updated successfully.')
            return redirect('ruwe_administration:church_development_detail', church_id=office.church.id)
    else:
        form = ChurchDevelopmentOfficeForm(instance=office)
    
    return render(request, 'ruwe_administration/church/development_form.html', {
        'form': form, 'church': office.church, 'office': office, 'action': 'Edit'
    })

@login_required
def church_travel_office_detail(request, church_id):
    church = get_object_or_404(Church, id=church_id)
    office = get_office_or_none(ChurchTravelOffice, church=church)
    return render(request, 'ruwe_administration/church/travel_detail.html', {
        'church': church, 'office': office
    })

@login_required
def church_travel_office_add(request, church_id):
    church = get_object_or_404(Church, id=church_id)
    if request.method == 'POST':
        form = ChurchTravelOfficeForm(request.POST)
        if form.is_valid():
            office = form.save(commit=False)
            office.church = church
            office.name = f"{church.name} Travel Office"
            office.save()
            form.save_m2m()
            messages.success(request, f'{office.name} has been created successfully.')
            return redirect('ruwe_administration:church_travel_detail', church_id=church.id)
    else:
        form = ChurchTravelOfficeForm(initial={'church': church})
    
    return render(request, 'ruwe_administration/church/travel_form.html', {
        'form': form, 'church': church, 'action': 'Add'
    })

@login_required
def church_travel_office_edit(request, pk):
    office = get_object_or_404(ChurchTravelOffice, pk=pk)
    if request.method == 'POST':
        form = ChurchTravelOfficeForm(request.POST, instance=office)
        if form.is_valid():
            office = form.save()
            messages.success(request, f'{office.name} has been updated successfully.')
            return redirect('ruwe_administration:church_travel_detail', church_id=office.church.id)
    else:
        form = ChurchTravelOfficeForm(instance=office)
    
    return render(request, 'ruwe_administration/church/travel_form.html', {
        'form': form, 'church': office.church, 'office': office, 'action': 'Edit'
    })

@login_required
def church_disciplinary_office_detail(request, church_id):
    church = get_object_or_404(Church, id=church_id)
    office = get_office_or_none(ChurchDisciplinaryOffice, church=church)
    return render(request, 'ruwe_administration/church/disciplinary_detail.html', {
        'church': church, 'office': office
    })

@login_required
def church_disciplinary_office_add(request, church_id):
    church = get_object_or_404(Church, id=church_id)
    if request.method == 'POST':
        form = ChurchDisciplinaryOfficeForm(request.POST)
        if form.is_valid():
            office = form.save(commit=False)
            office.church = church
            office.name = f"{church.name} Disciplinary Office"
            office.save()
            form.save_m2m()
            messages.success(request, f'{office.name} has been created successfully.')
            return redirect('ruwe_administration:church_disciplinary_detail', church_id=church.id)
    else:
        form = ChurchDisciplinaryOfficeForm(initial={'church': church})
    
    return render(request, 'ruwe_administration/church/disciplinary_form.html', {
        'form': form, 'church': church, 'action': 'Add'
    })

@login_required
def church_disciplinary_office_edit(request, pk):
    office = get_object_or_404(ChurchDisciplinaryOffice, pk=pk)
    if request.method == 'POST':
        form = ChurchDisciplinaryOfficeForm(request.POST, instance=office)
        if form.is_valid():
            office = form.save()
            messages.success(request, f'{office.name} has been updated successfully.')
            return redirect('ruwe_administration:church_disciplinary_detail', church_id=office.church.id)
    else:
        form = ChurchDisciplinaryOfficeForm(instance=office)
    
    return render(request, 'ruwe_administration/church/disciplinary_form.html', {
        'form': form, 'church': office.church, 'office': office, 'action': 'Edit'
    })


# =========================
# PASTORATE LEVEL VIEWS (3)
# =========================

@login_required
def pastorate_main_office_detail(request, pastorate_id):
    pastorate = get_object_or_404(Pastorate, id=pastorate_id)
    office = get_office_or_none(PastorateMainOffice, pastorate=pastorate)
    return render(request, 'ruwe_administration/pastorate/main_detail.html', {
        'pastorate': pastorate, 'office': office
    })

@login_required
def pastorate_main_office_add(request, pastorate_id):
    pastorate = get_object_or_404(Pastorate, id=pastorate_id)
    if request.method == 'POST':
        form = PastorateMainOfficeForm(request.POST)
        if form.is_valid():
            office = form.save(commit=False)
            office.pastorate = pastorate
            office.name = f"{pastorate.name} Main Office"
            office.save()
            form.save_m2m()
            messages.success(request, f'{office.name} has been created successfully.')
            return redirect('ruwe_administration:pastorate_main_detail', pastorate_id=pastorate.id)
    else:
        form = PastorateMainOfficeForm(initial={'pastorate': pastorate})
    
    return render(request, 'ruwe_administration/pastorate/main_form.html', {
        'form': form, 'pastorate': pastorate, 'action': 'Add'
    })

@login_required
def pastorate_main_office_edit(request, pk):
    office = get_object_or_404(PastorateMainOffice, pk=pk)
    if request.method == 'POST':
        form = PastorateMainOfficeForm(request.POST, instance=office)
        if form.is_valid():
            office = form.save()
            messages.success(request, f'{office.name} has been updated successfully.')
            return redirect('ruwe_administration:pastorate_main_detail', pastorate_id=office.pastorate.id)
    else:
        form = PastorateMainOfficeForm(instance=office)
    
    return render(request, 'ruwe_administration/pastorate/main_form.html', {
        'form': form, 'pastorate': office.pastorate, 'office': office, 'action': 'Edit'
    })

@login_required
def pastorate_youth_office_detail(request, pastorate_id):
    pastorate = get_object_or_404(Pastorate, id=pastorate_id)
    office = get_office_or_none(PastorateYouthOffice, pastorate=pastorate)
    return render(request, 'ruwe_administration/pastorate/youth_detail.html', {
        'pastorate': pastorate, 'office': office
    })

@login_required
def pastorate_youth_office_add(request, pastorate_id):
    pastorate = get_object_or_404(Pastorate, id=pastorate_id)
    if request.method == 'POST':
        form = PastorateYouthOfficeForm(request.POST)
        if form.is_valid():
            office = form.save(commit=False)
            office.pastorate = pastorate
            office.name = f"{pastorate.name} Youth Office"
            office.save()
            form.save_m2m()
            messages.success(request, f'{office.name} has been created successfully.')
            return redirect('ruwe_administration:pastorate_youth_detail', pastorate_id=pastorate.id)
    else:
        form = PastorateYouthOfficeForm(initial={'pastorate': pastorate})
    
    return render(request, 'ruwe_administration/pastorate/youth_form.html', {
        'form': form, 'pastorate': pastorate, 'action': 'Add'
    })

@login_required
def pastorate_youth_office_edit(request, pk):
    office = get_object_or_404(PastorateYouthOffice, pk=pk)
    if request.method == 'POST':
        form = PastorateYouthOfficeForm(request.POST, instance=office)
        if form.is_valid():
            office = form.save()
            messages.success(request, f'{office.name} has been updated successfully.')
            return redirect('ruwe_administration:pastorate_youth_detail', pastorate_id=office.pastorate.id)
    else:
        form = PastorateYouthOfficeForm(instance=office)
    
    return render(request, 'ruwe_administration/pastorate/youth_form.html', {
        'form': form, 'pastorate': office.pastorate, 'office': office, 'action': 'Edit'
    })

@login_required
def pastorate_teachers_office_detail(request, pastorate_id):
    pastorate = get_object_or_404(Pastorate, id=pastorate_id)
    office = get_office_or_none(PastorateTeachersOffice, pastorate=pastorate)
    return render(request, 'ruwe_administration/pastorate/teachers_detail.html', {
        'pastorate': pastorate, 'office': office
    })

@login_required
def pastorate_teachers_office_add(request, pastorate_id):
    pastorate = get_object_or_404(Pastorate, id=pastorate_id)
    if request.method == 'POST':
        form = PastorateTeachersOfficeForm(request.POST)
        if form.is_valid():
            office = form.save(commit=False)
            office.pastorate = pastorate
            office.name = f"{pastorate.name} Teachers Office"
            office.save()
            form.save_m2m()
            messages.success(request, f'{office.name} has been created successfully.')
            return redirect('ruwe_administration:pastorate_teachers_detail', pastorate_id=pastorate.id)
    else:
        form = PastorateTeachersOfficeForm(initial={'pastorate': pastorate})
    
    return render(request, 'ruwe_administration/pastorate/teachers_form.html', {
        'form': form, 'pastorate': pastorate, 'action': 'Add'
    })

@login_required
def pastorate_teachers_office_edit(request, pk):
    office = get_object_or_404(PastorateTeachersOffice, pk=pk)
    if request.method == 'POST':
        form = PastorateTeachersOfficeForm(request.POST, instance=office)
        if form.is_valid():
            office = form.save()
            messages.success(request, f'{office.name} has been updated successfully.')
            return redirect('ruwe_administration:pastorate_teachers_detail', pastorate_id=office.pastorate.id)
    else:
        form = PastorateTeachersOfficeForm(instance=office)
    
    return render(request, 'ruwe_administration/pastorate/teachers_form.html', {
        'form': form, 'pastorate': office.pastorate, 'office': office, 'action': 'Edit'
    })


# =========================
# DIOCESE LEVEL VIEWS (3)
# =========================

@login_required
def diocese_main_office_detail(request, diocese_id):
    diocese = get_object_or_404(Diocese, id=diocese_id)
    office = get_office_or_none(DioceseMainOffice, diocese=diocese)
    return render(request, 'ruwe_administration/diocese/main_detail.html', {
        'diocese': diocese, 'office': office
    })

@login_required
def diocese_main_office_add(request, diocese_id):
    diocese = get_object_or_404(Diocese, id=diocese_id)
    if request.method == 'POST':
        form = DioceseMainOfficeForm(request.POST)
        if form.is_valid():
            office = form.save(commit=False)
            office.diocese = diocese
            office.name = f"{diocese.name} Main Office"
            office.save()
            form.save_m2m()
            messages.success(request, f'{office.name} has been created successfully.')
            return redirect('ruwe_administration:diocese_main_detail', diocese_id=diocese.id)
    else:
        form = DioceseMainOfficeForm(initial={'diocese': diocese})
    
    return render(request, 'ruwe_administration/diocese/main_form.html', {
        'form': form, 'diocese': diocese, 'action': 'Add'
    })

@login_required
def diocese_main_office_edit(request, pk):
    office = get_object_or_404(DioceseMainOffice, pk=pk)
    if request.method == 'POST':
        form = DioceseMainOfficeForm(request.POST, instance=office)
        if form.is_valid():
            office = form.save()
            messages.success(request, f'{office.name} has been updated successfully.')
            return redirect('ruwe_administration:diocese_main_detail', diocese_id=office.diocese.id)
    else:
        form = DioceseMainOfficeForm(instance=office)
    
    return render(request, 'ruwe_administration/diocese/main_form.html', {
        'form': form, 'diocese': office.diocese, 'office': office, 'action': 'Edit'
    })

@login_required
def diocese_youth_office_detail(request, diocese_id):
    diocese = get_object_or_404(Diocese, id=diocese_id)
    office = get_office_or_none(DioceseYouthOffice, diocese=diocese)
    return render(request, 'ruwe_administration/diocese/youth_detail.html', {
        'diocese': diocese, 'office': office
    })

@login_required
def diocese_youth_office_add(request, diocese_id):
    diocese = get_object_or_404(Diocese, id=diocese_id)
    if request.method == 'POST':
        form = DioceseYouthOfficeForm(request.POST)
        if form.is_valid():
            office = form.save(commit=False)
            office.diocese = diocese
            office.name = f"{diocese.name} Youth Office"
            office.save()
            form.save_m2m()
            messages.success(request, f'{office.name} has been created successfully.')
            return redirect('ruwe_administration:diocese_youth_detail', diocese_id=diocese.id)
    else:
        form = DioceseYouthOfficeForm(initial={'diocese': diocese})
    
    return render(request, 'ruwe_administration/diocese/youth_form.html', {
        'form': form, 'diocese': diocese, 'action': 'Add'
    })

@login_required
def diocese_youth_office_edit(request, pk):
    office = get_object_or_404(DioceseYouthOffice, pk=pk)
    if request.method == 'POST':
        form = DioceseYouthOfficeForm(request.POST, instance=office)
        if form.is_valid():
            office = form.save()
            messages.success(request, f'{office.name} has been updated successfully.')
            return redirect('ruwe_administration:diocese_youth_detail', diocese_id=office.diocese.id)
    else:
        form = DioceseYouthOfficeForm(instance=office)
    
    return render(request, 'ruwe_administration/diocese/youth_form.html', {
        'form': form, 'diocese': office.diocese, 'office': office, 'action': 'Edit'
    })

@login_required
def diocese_teachers_office_detail(request, diocese_id):
    diocese = get_object_or_404(Diocese, id=diocese_id)
    office = get_office_or_none(DioceseTeachersOffice, diocese=diocese)
    return render(request, 'ruwe_administration/diocese/teachers_detail.html', {
        'diocese': diocese, 'office': office
    })

@login_required
def diocese_teachers_office_add(request, diocese_id):
    diocese = get_object_or_404(Diocese, id=diocese_id)
    if request.method == 'POST':
        form = DioceseTeachersOfficeForm(request.POST)
        if form.is_valid():
            office = form.save(commit=False)
            office.diocese = diocese
            office.name = f"{diocese.name} Teachers Office"
            office.save()
            form.save_m2m()
            messages.success(request, f'{office.name} has been created successfully.')
            return redirect('ruwe_administration:diocese_teachers_detail', diocese_id=diocese.id)
    else:
        form = DioceseTeachersOfficeForm(initial={'diocese': diocese})
    
    return render(request, 'ruwe_administration/diocese/teachers_form.html', {
        'form': form, 'diocese': diocese, 'action': 'Add'
    })

@login_required
def diocese_teachers_office_edit(request, pk):
    office = get_object_or_404(DioceseTeachersOffice, pk=pk)
    if request.method == 'POST':
        form = DioceseTeachersOfficeForm(request.POST, instance=office)
        if form.is_valid():
            office = form.save()
            messages.success(request, f'{office.name} has been updated successfully.')
            return redirect('ruwe_administration:diocese_teachers_detail', diocese_id=office.diocese.id)
    else:
        form = DioceseTeachersOfficeForm(instance=office)
    
    return render(request, 'ruwe_administration/diocese/teachers_form.html', {
        'form': form, 'diocese': office.diocese, 'office': office, 'action': 'Edit'
    })


# ====================================
# DEAN/HEADQUARTERS LEVEL VIEWS (25)
# ====================================

def create_dean_office_views(model_class, form_class, template_prefix):
    """Factory function to create standard dean office views"""
    
    @login_required
    def detail_view(request):
        office = get_office_or_none(model_class)
        return render(request, f'ruwe_administration/dean/{template_prefix}_detail.html', {'office': office})
    
    @login_required
    def add_view(request):
        if request.method == 'POST':
            form = form_class(request.POST)
            if form.is_valid():
                office = form.save()
                messages.success(request, f'{office.name} has been created successfully.')
                return redirect(f'ruwe_administration:dean_{template_prefix}_detail')
        else:
            form = form_class()
        
        return render(request, f'ruwe_administration/dean/{template_prefix}_form.html', {
            'form': form, 'action': 'Add'
        })
    
    @login_required
    def edit_view(request, pk):
        office = get_object_or_404(model_class, pk=pk)
        if request.method == 'POST':
            form = form_class(request.POST, instance=office)
            if form.is_valid():
                office = form.save()
                messages.success(request, f'{office.name} has been updated successfully.')
                return redirect(f'ruwe_administration:dean_{template_prefix}_detail')
        else:
            form = form_class(instance=office)
        
        return render(request, f'ruwe_administration/dean/{template_prefix}_form.html', {
            'form': form, 'office': office, 'action': 'Edit'
        })
    
    return detail_view, add_view, edit_view

# Create views for all 25 Dean offices
dean_management_office_detail, dean_management_office_add, dean_management_office_edit = create_dean_office_views(
    DeanManagementOffice, DeanManagementOfficeForm, 'management'
)

dean_organizing_secretary_office_detail, dean_organizing_secretary_office_add, dean_organizing_secretary_office_edit = create_dean_office_views(
    DeanOrganizingSecretaryOffice, DeanOrganizingSecretaryOfficeForm, 'organizing_secretary'
)

dean_youth_office_detail, dean_youth_office_add, dean_youth_office_edit = create_dean_office_views(
    DeanYouthOffice, DeanYouthOfficeForm, 'youth'
)

dean_kings_office_detail, dean_kings_office_add, dean_kings_office_edit = create_dean_office_views(
    DeanKingsOffice, DeanKingsOfficeForm, 'kings'
)

dean_archbishops_office_detail, dean_archbishops_office_add, dean_archbishops_office_edit = create_dean_office_views(
    DeanArchbishopsOffice, DeanArchbishopsOfficeForm, 'archbishops'
)

dean_bishops_office_detail, dean_bishops_office_add, dean_bishops_office_edit = create_dean_office_views(
    DeanBishopsOffice, DeanBishopsOfficeForm, 'bishops'
)

dean_pastors_office_detail, dean_pastors_office_add, dean_pastors_office_edit = create_dean_office_views(
    DeanPastorsOffice, DeanPastorsOfficeForm, 'pastors'
)

dean_lay_readers_office_detail, dean_lay_readers_office_add, dean_lay_readers_office_edit = create_dean_office_views(
    DeanLayReadersOffice, DeanLayReadersOfficeForm, 'lay_readers'
)

dean_divisions_office_detail, dean_divisions_office_add, dean_divisions_office_edit = create_dean_office_views(
    DeanDivisionsOffice, DeanDivisionsOfficeForm, 'divisions'
)

dean_teachers_office_detail, dean_teachers_office_add, dean_teachers_office_edit = create_dean_office_views(
    DeanTeachersOffice, DeanTeachersOfficeForm, 'teachers'
)

dean_women_leaders_office_detail, dean_women_leaders_office_add, dean_women_leaders_office_edit = create_dean_office_views(
    DeanWomenLeadersOffice, DeanWomenLeadersOfficeForm, 'women_leaders'
)

dean_elders_office_detail, dean_elders_office_add, dean_elders_office_edit = create_dean_office_views(
    DeanEldersOffice, DeanEldersOfficeForm, 'elders'
)

dean_soso_office_detail, dean_soso_office_add, dean_soso_office_edit = create_dean_office_views(
    DeanSosoOffice, DeanSosoOfficeForm, 'soso'
)

dean_courses_office_detail, dean_courses_office_add, dean_courses_office_edit = create_dean_office_views(
    DeanCoursesOffice, DeanCoursesOfficeForm, 'courses'
)

dean_ecclesiastical_vestment_office_detail, dean_ecclesiastical_vestment_office_add, dean_ecclesiastical_vestment_office_edit = create_dean_office_views(
    DeanEcclesiasticalVestmentOffice, DeanEcclesiasticalVestmentOfficeForm, 'ecclesiastical_vestment'
)

dean_ecclesiastical_cross_office_detail, dean_ecclesiastical_cross_office_add, dean_ecclesiastical_cross_office_edit = create_dean_office_views(
    DeanEcclesiasticalCrossOffice, DeanEcclesiasticalCrossOfficeForm, 'ecclesiastical_cross'
)

dean_chaplaincy_office_detail, dean_chaplaincy_office_add, dean_chaplaincy_office_edit = create_dean_office_views(
    DeanChaplaincyOffice, DeanChaplaincyOfficeForm, 'chaplaincy'
)

dean_churches_data_records_office_detail, dean_churches_data_records_office_add, dean_churches_data_records_office_edit = create_dean_office_views(
    DeanChurchesDataRecordsOffice, DeanChurchesDataRecordsOfficeForm, 'churches_data_records'
)

dean_education_gender_equality_office_detail, dean_education_gender_equality_office_add, dean_education_gender_equality_office_edit = create_dean_office_views(
    DeanEducationGenderEqualityOffice, DeanEducationGenderEqualityOfficeForm, 'education_gender_equality'
)

dean_development_office_detail, dean_development_office_add, dean_development_office_edit = create_dean_office_views(
    DeanDevelopmentOffice, DeanDevelopmentOfficeForm, 'development'
)

dean_disciplinary_committee_office_detail, dean_disciplinary_committee_office_add, dean_disciplinary_committee_office_edit = create_dean_office_views(
    DeanDisciplinaryCommitteeOffice, DeanDisciplinaryCommitteeOfficeForm, 'disciplinary_committee'
)

dean_arbitration_committee_office_detail, dean_arbitration_committee_office_add, dean_arbitration_committee_office_edit = create_dean_office_views(
    DeanArbitrationCommitteeOffice, DeanArbitrationCommitteeOfficeForm, 'arbitration_committee'
)

dean_health_counselling_office_detail, dean_health_counselling_office_add, dean_health_counselling_office_edit = create_dean_office_views(
    DeanHealthCounsellingOffice, DeanHealthCounsellingOfficeForm, 'health_counselling'
)

dean_churches_protocol_office_detail, dean_churches_protocol_office_add, dean_churches_protocol_office_edit = create_dean_office_views(
    DeanChurchesProtocolOffice, DeanChurchesProtocolOfficeForm, 'churches_protocol'
)

dean_media_publicity_office_detail, dean_media_publicity_office_add, dean_media_publicity_office_edit = create_dean_office_views(
    DeanMediaPublicityOffice, DeanMediaPublicityOfficeForm, 'media_publicity'
)