from django.shortcuts import render, redirect
from datetime import timedelta
from django.http import HttpResponse
from .models import Assets
from .forms import AddAssetForm, EditAssetForm, RevalueForm
from transactions.models import Transactions
from .services import GetDepreciation

import datetime


def AssetTable(request):
    context = {
        'assets': Assets.objects.all()
    }
    return render(request, 'assettable.html', context, {'title': 'Assets'})


def AssetView(request, asset_id):
    context_view = {
        'asset_view': Assets.objects.get(id=asset_id),
        'audit_trail': Transactions.objects.filter(assets_transact=asset_id),
    }

    return render(request, 'assetview.html', context_view, {'title': 'View Asset'})


def AssetAdd(request):
    if request.method == 'POST':
        form = AddAssetForm(request.POST)
        if form.is_valid():
            revalued_asset = form.save(commit=False)

            # Whether to display asset in table or not
            if revalued_asset.status == 'Archived':
                revalued_asset.display = 0
            else:
                revalued_asset.display = 1

            # Compute depreciation hahahha sira toh
            revalued_asset.balance = revalued_asset.acquisition_cost
            revalued_asset.counter = revalued_asset.project_life
            revalued_asset.dep_value = (revalued_asset.acquisition_cost - revalued_asset.salvage_value) / revalued_asset.project_life

            revalued_asset.it_dep_date = [revalued_asset.date_acquired] * revalued_asset.counter
            revalued_asset.it_accrued = [0] * revalued_asset.counter
            revalued_asset.it_balance = [0] * revalued_asset.counter

            revalued_asset.it_dep_date[0] = revalued_asset.date_acquired
            revalued_asset.it_accrued[0] = revalued_asset.dep_value
            revalued_asset.it_balance[0] = revalued_asset.acquisition_cost

            month = 1
            for month in range(revalued_asset.counter):
                revalued_asset.it_dep_date[month] = revalued_asset.it_dep_date[month-1] + datetime.timedelta(30)
                revalued_asset.it_accrued[month] = revalued_asset.it_accrued[month-1] + revalued_asset.dep_value
                revalued_asset.it_balance[month] = revalued_asset.acquisition_cost - revalued_asset.it_accrued[month]

            # Save
            revalued_asset.save()
            return redirect('/assets/view/' + str(revalued_asset.id))
    else:
        form = AddAssetForm()
    return render(request, 'addasset.html', {'form': form}, {'title': 'Add an Asset'})


def AssetEdit(request, asset_id):
    if request.method == 'POST':
        form = EditAssetForm(request.POST, instance=Assets.objects.all().get(id=asset_id))
        if form.is_valid():
            form.save()
            return redirect('/assets/view/' + str(asset_id))
    else:
        form = EditAssetForm(instance=Assets.objects.all().get(id=asset_id))
    return render(request, 'editasset.html', {'form': form}, {'title': 'Edit an Asset'})


def Revalue(request, asset_id):
    if request.method == 'POST':
        form = RevalueForm(request.POST, instance=Assets.objects.all().get(id=asset_id))
        if form.is_valid():
            revalued_asset = form.save(commit=False)

            revalued_asset.balance = revalued_asset.acquisition_cost
            revalued_asset.counter = revalued_asset.project_life
            revalued_asset.dep_value = (revalued_asset.acquisition_cost - revalued_asset.salvage_value) / revalued_asset.project_life

            revalued_asset.it_dep_date.clear()
            revalued_asset.it_accrued.clear()
            revalued_asset.it_balance.clear()

            revalued_asset.it_dep_date = [revalued_asset.date_acquired] * revalued_asset.counter
            revalued_asset.it_accrued = [0] * revalued_asset.counter
            revalued_asset.it_balance = [0] * revalued_asset.counter

            revalued_asset.it_dep_date[0] = revalued_asset.date_acquired
            revalued_asset.it_accrued[0] = revalued_asset.dep_value
            revalued_asset.it_balance[0] = revalued_asset.acquisition_cost

            month = 1
            for month in range(revalued_asset.counter):
                revalued_asset.it_dep_date[month] = revalued_asset.it_dep_date[month-1] + datetime.timedelta(30)
                revalued_asset.it_accrued[month] = revalued_asset.it_accrued[month-1] + revalued_asset.dep_value
                revalued_asset.it_balance[month] = revalued_asset.acquisition_cost - revalued_asset.it_accrued[month]

            return redirect('/assets/view/' + str(asset_id))
    else:
        form = RevalueForm(instance=Assets.objects.all().get(id=asset_id))
    return render(request, 'revalue.html', {'form': form}, {'title': 'Revalue Asset'})


def AssetArchive(request):
    return render(request, 'archive.html', {'title': 'Archived Assets'})
