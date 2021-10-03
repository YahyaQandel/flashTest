

export class CurrencyExchange {
    private elementsIDs = {
        currencyFieldID: '#currency',
        currencyRowID: '#curr_key_rate_',
        currencyKeyFieldID: '#curr_key_',
        currencyRateFieldID: '#currency_rate_',
        getRatesBtn: '#get_rates'
    };
    private url: string = "money/currency/exchange";

    visit(){
        cy.visit(this.url);
    }
    selectBaseCurrency(currency){
        cy.get(this.elementsIDs.currencyFieldID).select(currency);
        cy.get(this.elementsIDs.getRatesBtn).click();
    }
    
    getRateValueForBaseCurrency(currency){
        return cy.get(`${this.elementsIDs.currencyRateFieldID}${currency}`)
    }
}