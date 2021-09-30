import { UserApi } from "../apis/user.api";
import { BankFactory } from "../models/bank";

export class BankApi {
    private deleteApiUrl: string = '/bank/disconnect';
    private connectApiUrl: string = '/bank/connect';
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