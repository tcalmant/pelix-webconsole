import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

import { Service } from './bundle';

@Injectable()
export class ServicesService {
    services: Service[];

    constructor(private http: Http) { }

    getServices() {
        this.http.get("./api/v1/page/services").subscribe(
            response => this.services = response.json().map(svcRaw => new Service().deserialize(svcRaw)),
            error => console.log(error));
    }
}
