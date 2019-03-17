from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.http import HttpResponse
from .models import Assets
from .forms import AddAssetForm, EditAssetForm, RevalueForm
from transactions.models import Transactions
from .services import GetDepreciation
from . import urls

import datetime


@login_required
def AssetTable(request):
    context = {
        'assets': Assets.objects.filter(display=1)
    }
    return render(request, 'assettable.html', context, {'title': 'Assets'})


@login_required
def AssetAdd(request):
    if request.method == 'POST':
        form = AddAssetForm(request.POST)
        if form.is_valid():
            new_asset = form.save(commit=False)

            # Whether to display asset in table or not
            if new_asset.status == 'Archived':
                new_asset.display = 0
            else:
                new_asset.display = 1

            # Compute depreciation hahahha sira toh
            new_asset.counter = new_asset.project_life
            new_asset.dep_value = (new_asset.acquisition_cost - new_asset.salvage_value) / new_asset.project_life
            new_asset.balance = new_asset.acquisition_cost

            new_asset.it_dep_value = []
            new_asset.it_dep_date = []
            new_asset.it_accrued = []
            new_asset.it_balance = []

            new_asset.it_dep_value.append(new_asset.dep_value)
            new_asset.it_dep_date.append(new_asset.date_acquired)
            new_asset.it_accrued.append(float(0.00))
            new_asset.it_balance.append(new_asset.acquisition_cost)

            # Save
            new_asset.save()
            return redirect('/assets/view/' + str(new_asset.id))
    else:
        form = AddAssetForm()

    context = {
        'form': form,
        'title': 'Add an Asset',
    }
    return render(request, 'addasset.html', context)


@login_required
def AssetView(request, asset_id):
    asset = Assets.objects.get(id=asset_id)
    now = datetime.date.today()
    limit = datetime.timedelta(30)

    # Depreciation computes everytime the asset is viewed
    while True:
        if now < (asset.it_dep_date[-1] + limit):
            break
        elif now > (asset.it_dep_date[-1] + limit):
            gap = int((now - asset.it_dep_date[-1]) / limit)
            for i in range(gap):
                if asset.it_balance[-1] <= 0:
                    asset.it_balance.append(0.00)
                    break
                else:
                    asset.it_dep_date.append(asset.it_dep_date[-1] + limit)
                    asset.it_accrued.append(asset.it_accrued[-1] + asset.dep_value)
                    asset.it_balance.append(asset.balance - asset.it_accrued[-1])
                    asset.it_dep_value.append(asset.dep_value)
            break
        break

    asset.balance = asset.it_balance[-1]
    dep_values = zip(asset.it_dep_date, asset.it_dep_value, asset.it_accrued, asset.it_balance)
    
    asset.save()

    context_view = {
        'asset_view': Assets.objects.get(id=asset_id),
        'audit_trail': Transactions.objects.filter(assets_transact__id__contains=asset_id).order_by('date_added'),
        'dep_values': dep_values,
        'title': 'View Asset',
    }

    return render(request, 'assetview.html', context_view)


@login_required
def AssetEdit(request, asset_id):
    if request.method == 'POST':
        form = EditAssetForm(request.POST, instance=Assets.objects.all().get(id=asset_id))
        if form.is_valid():
            form.save()
            return redirect('/assets/view/' + str(asset_id))
    else:
        form = EditAssetForm(instance=Assets.objects.all().get(id=asset_id))

    context = {
        'form': form,
        'asset': Assets.objects.get(id=asset_id),
        'title': 'Edit an Asset',
    }
    return render(request, 'editasset.html', context)



@login_required
def Revalue(request, asset_id):
    if request.method == 'POST':
        form = RevalueForm(request.POST, instance=Assets.objects.all().get(id=asset_id))
        if form.is_valid():
            form.save()
            return redirect('/assets/view/' + str(asset_id) + '/revalue/true/')
    else:
        form = RevalueForm(instance=Assets.objects.all().get(id=asset_id))
        
    context = {
        'form': form,
        'asset': Assets.objects.get(id=asset_id),
        'title': 'Revalue an Asset',
    }
    return render(request, 'revalue.html', context)


@login_required
def RevalueAlgo(request, asset_id):
    asset_to_revalue = Assets.objects.get(id=asset_id)
    asset_to_revalue.balance = asset_to_revalue.acquisition_cost
    asset_to_revalue.counter = asset_to_revalue.project_life
    asset_to_revalue.dep_value = (asset_to_revalue.acquisition_cost - asset_to_revalue.salvage_value) / asset_to_revalue.project_life

    asset_to_revalue.save()
    return redirect('/assets/view/' + str(asset_id))


@login_required
def AssetArchive(request, asset_id):
    asset_to_archive = Assets.objects.get(id=asset_id)
    asset_to_archive.status = 'Archived'
    asset_to_archive.display = 0
    asset_to_archive.save()
    return redirect('/assets/view/' + str(asset_id))


@login_required
def AssetRecover(request, asset_id):
    asset_to_recover = Assets.objects.get(id=asset_id)
    asset_to_recover.status = 'In Storage'
    asset_to_recover.display = 1
    asset_to_recover.save()
    return redirect('/assets/view/' + str(asset_id))


@login_required
def ArchivedAssetsTable(request):
    context = {
        'assets': Assets.objects.filter(display=0),
        'title': 'Archived Assets',
    }
    return render(request, 'assettablearchive.html', context)


@login_required
def DeleteAsset(request, asset_id):
    asset_to_delete = Assets.objects.get(id=asset_id)
    asset_to_delete.delete()
    return redirect('/assets/')