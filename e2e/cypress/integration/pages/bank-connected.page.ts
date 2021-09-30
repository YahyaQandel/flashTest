

export class BankConnected {

 private elementsIDs = {
        titleID:"#pageHead",
        bankNameFieldID: '#bank_name',
        accountNumberFieldID: '#account_number'
    };
private url = "/bank/connected";

get bankNameSpan(){
        return cy.get(this.elementsIDs.bankNameFieldID);
    }
get accountNumberSpan(){
        return cy.get(this.elementsIDs.accountNumberFieldID);
    }
}