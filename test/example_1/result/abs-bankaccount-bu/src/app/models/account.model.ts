export class Account {
    public id: number;
    public rekening: string;
    public interest: number;
    public balance: number;
    public customerId: number;

    constructor(obj ? : any) {
        this.id = obj && obj.id || null;
        this.rekening = obj && obj.rekening || null;
        this.interest = obj && obj.interest || null;
        this.balance = obj && obj.balance || null;
        this.customerId = obj && obj.customerId || null;
    }


}