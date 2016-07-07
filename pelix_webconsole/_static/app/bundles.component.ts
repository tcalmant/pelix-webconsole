import { Component, OnInit } from '@angular/core';
import { Bundle } from './bundle';
import { BundlesService } from './bundles.service';

@Component({
    providers: [BundlesService],
    selector: 'bundles-table',
    template: `<h2>Bundles</h2>
<div class="table-responsive">
<table class="table table-striped table-hover">
<thead>
    <th>ID</th>
    <th>Name</th>
    <th>Version</th>
    <th>State</th>
</thead>
<tbody>
<tr *ngFor="let bundle of bndSvc.bundles" (click)="onSelect(bundle)">
    <td>{{bundle.id}}</td>
    <td>{{bundle.symbolicName}}</td>
    <td>{{bundle.version}}</td>
    <td>{{bundle.state}}</td>
</tr>
</tbody>
</table>
</div>

<div *ngIf="selectedBundle">
<h2>Bundle Details</h2>

<div class="table-responsive">
<table class="table table-striped table-hover">
<thead>
    <th>Property</th>
    <th>Value</th>
</thead>
<tbody>
<tr>
    <td>ID</td>
    <td>{{selectedBundle.id}}</td>
</tr>
<tr>
    <td>Name</td>
    <td>{{selectedBundle.symbolicName}}</td>
</tr>
<tr>
    <td>Version</td>
    <td>{{selectedBundle.version}}</td>
</tr>
<tr>
    <td>State</td>
    <td>{{selectedBundle.state}}</td>
</tr>
<tr>
    <td>Location</td>
    <td>{{selectedBundle.location}}</td>
</tr>
</tbody>
</table>
</div>

<div *ngIf="selectedBundle.provided.length">
<h3>Provided Services</h3>
<div class="table-responsive">
<table class="table table-striped table-hover">
<thead>
    <th>ID</th>
    <th>Specifications</th>
    <th>Ranking</th>
</thead>
<tbody>
<tr *ngFor="let svc of selectedBundle.provided">
<td>{{svc.id}}</td>
<td>{{svc.specifications}}</td>
<td>{{svc.get_ranking()}}</td>
</tr>
</tbody>
</table>
</div>
</div>

<div *ngIf="selectedBundle.consumed.length">
<h3>Consumed Services</h3>
<div class="table-responsive">
<table class="table table-striped table-hover">
<thead>
    <th>ID</th>
    <th>Specifications</th>
    <th>Bundle</th>
    <th>Ranking</th>
</thead>
<tbody>
<tr *ngFor="let svc of selectedBundle.consumed">
<td>{{svc.id}}</td>
<td>{{svc.specifications}}</td>
<td>{{svc.providerId}}</td>
<td>{{svc.get_ranking()}}</td>
</tr>
</tbody>
</table>
</div>
</div>
</div>
`
})
export class BundlesComponent {
    selectedBundle: Bundle;

    constructor(private bndSvc: BundlesService) { }

    ngOnInit() {
        this.getBundles();
    }

    getBundles() {
        this.bndSvc.getBundles();
    }

    onSelect(bundle: Bundle) {
        this.selectedBundle = bundle;
    }
}
