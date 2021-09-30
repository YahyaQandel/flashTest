var faker = require('faker');

export class BankFactory {
    private bank_name: string ;
    private branch_number: string ;
    private account_number:string ;
    private account_holder_name:string ;

    constructor(){
        this.bank_name = this.get_bank();
        this.branch_number = faker.datatype.number().toString();
        this.account_number = `${faker.datatype.number().toString()}${faker.datatype.number().toString()}`;
        this.account_holder_name = faker.name.findName();
    }

    get_bank(){
        return ["HSBC","CIB","QNB"][Math.floor(Math.random() * ["HSBC","CIB","QNB"].length)];
    }
}  