export class Customer {
    public address: string;
    public phone: string;
    public name: string;
    public id: number;
    public email: string;

    constructor(obj ? : any) {
        this.address = obj && obj.address || null;
        this.phone = obj && obj.phone || null;
        this.name = obj && obj.name || null;
        this.id = obj && obj.id || null;
        this.email = obj && obj.email || null;
    }


}