import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

import { Bundle } from './bundle';

@Injectable()
export class BundlesService {
    bundles: Bundle[];

    constructor(private http: Http) { }

    getBundles() {
        this.http.get("./api/v1/page/bundles").subscribe(
            response => this.bundles = response.json().map(rawBnd => new Bundle().deserialize(rawBnd)),
            error => console.log(error));
    }
}
