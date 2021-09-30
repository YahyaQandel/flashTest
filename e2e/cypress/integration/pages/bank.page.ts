

export class Bank {
    private elementsIDs = {
        bankFieldID: '#bank',
        branchNumberFieldID: '#branch_number',
        accountNumberFieldID: '#acc_number',
        accountHolderNameFieldID: '#acc_holder',
        connectBtnID: '#connect',
    };
    private url: string = "bank/connect";

    visit(){
        cy.visit(this.url);
    }
    fillFields(bank:string, branchNumber:string, accountNumber, accountHolderName) {
        cy.get(this.elementsIDs.bankFieldID).select(bank);
        cy.get(this.elementsIDs.branchNumberFieldID).type(branchNumber);
        cy.get(this.elementsIDs.accountNumberFieldID).type(accountNumber)
        cy.get(this.elementsIDs.accountHolderNameFieldID).type(accountHolderName)
    }

    get connectBtn(){
        return cy.get(this.elementsIDs.connectBtnID);
    }

    generate_random_account_number(){
        let length = 10;
        var result           = 'C1';
        var characters       = 'X0123456789';
        var charactersLength = characters.length;
        for ( var i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
        return result;
    }
    get_bank(){
    return ["HSBC","CIB","QNB"][Math.floor(Math.random() * ["HSBC","CIB","QNB"].length)];
    }
}