import { BankFactory } from "../models/bank";

export class BankApi {
    private deleteApiUrl: string = '/api/v1/bank/disconnect';
    private connectApiUrl: string = '/api/v1/bank/connect';
    deleteAccount(userToken: any, account_number: string) {
        const options = {
            url: `${Cypress.config().baseUrl}${this.deleteApiUrl}?account_number=${account_number}`,
            method: 'DELETE',
            retryOnStatusCodeFailure: true,
            headers: { 'Authorization': 'Bearer ' + `${userToken}` }
        };
        return cy.request(options);
    }

    connectAccount(userToken: any, bank: BankFactory) {
        const options = {
            url: `${Cypress.config().baseUrl}${this.connectApiUrl}`,
            method: 'POST',
            body: {...bank},
            retryOnStatusCodeFailure: true,
            headers: { 'Authorization': 'Bearer ' + `${userToken}` }
        };
        return cy.request(options);
    }
}