import { Component } from '@angular/core';
import { BundlesComponent } from './bundles.component';
import { ServicesComponent } from './services.component';

@Component({
    selector: 'web-console',
    template: `<h1>Pelix Web Console</h1>
<bundles-table></bundles-table>
<services-table></services-table>`,
    directives: [BundlesComponent, ServicesComponent]
})
export class AppComponent {
}
