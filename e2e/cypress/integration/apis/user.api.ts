import { UserFactory } from "../models/user";

export class UserApi {
    private loginUrl: string = '/oauth/token';
    private registerUrl: string = '/api/v1/user/register';
    private deleteUrl: string = '/api/v1/user/delete';

    login(username: string, password:string) {
        const options = {
            url: `${Cypress.config().baseUrl}${this.loginUrl}`,
            method: 'POST',
            body: { username: username, password: password },
            retryOnStatusCodeFailure: true,
            headers: { 'Content-Type': 'application/json' }
        };
        return cy.request(options);
    }

    register(user: UserFactory) {
        const options = {
            url: `${Cypress.config().baseUrl}${this.registerUrl}`,
            method: 'POST',
            body: { ...user },
            retryOnStatusCodeFailure: true,
            headers: { 'Content-Type': 'application/json' }
        };
        return cy.request(options);
    }

    delete(userToken: any, username: string) {
        const options = {
            url: `${Cypress.config().baseUrl}${this.deleteUrl}?username=${username}`,
            method: 'DELETE',
            retryOnStatusCodeFailure: true,
            headers: { 'Authorization': 'Bearer ' + `${userToken}` }
        };
        return cy.request(options);
    }
}