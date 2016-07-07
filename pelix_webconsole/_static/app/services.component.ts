import { Component, OnInit } from '@angular/core';
import { Service } from './bundle';
import { ServicesService } from './services.service';

@Component({
    providers: [ServicesService],
    selector: 'services-table',
    template: `<h2>Services</h2>
<div class="table-responsive">
<table class="table table-striped table-hover">
<thead>
    <th>ID</th>
    <th>Specifications</th>
    <th>Bundle</th>
    <th>Ranking</th>
</thead>
<tbody>
<tr *ngFor="let svc of svcSvc.services" (click)="onSelect(bundle)">
    <td>{{svc.id}}</td>
    <td>{{svc.specifications}}</td>
    <td>{{svc.providerId}}</td>
    <td>{{svc.get_ranking()}}</td>
</tr>
</tbody>
</table>
</div>
`
})
export class ServicesComponent {
    selectedService: Service;

    constructor(private svcSvc: ServicesService) { }

    ngOnInit() {
        this.getServices();
    }

    getServices() {
        this.svcSvc.getServices();
    }

    onSelect(svc: Service) {
        this.selectedService = svc;
    }
}
