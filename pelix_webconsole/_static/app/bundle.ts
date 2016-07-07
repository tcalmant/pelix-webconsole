interface Serializable<T> {
    deserialize(input: Object): T;
}

export class Service implements Serializable<Service> {
    id: number;
    specifications: string[];
    properties: any;
    providerId: number;

    deserialize(input: Object): Service {
        for (var propName in input) {
            this[propName] = input[propName];
        }
        return this;
    }

    get_ranking() : string {
        return this.properties["service.ranking"];
    }
}

export class Bundle implements Serializable<Bundle> {
    id: number;
    symbolicName: string;
    version: string;
    state: string;
    location: string;

    provided: Service[];
    consumed: Service[];

    deserialize(input: Object): Bundle {
        for (var propName in input) {
            this[propName] = input[propName];
        }

        this.provided = this.provided.map(rawSvc => new Service().deserialize(rawSvc));
        this.consumed = this.consumed.map(rawSvc => new Service().deserialize(rawSvc));
        return this;
    }
}
