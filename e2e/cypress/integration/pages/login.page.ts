

export class Login {
    private elementsIDs = {
        usernameFieldID: '#username',
        passowordFieldID: '#password',
        loginButtonID: '#login'
    };
    private url: string = "login";

    visit(){
        cy.visit(this.url);
    }
    perform(username:string, password:string) {
        cy.get(this.elementsIDs.usernameFieldID).type(username)
        cy.get(this.elementsIDs.passowordFieldID).type(password)
        cy.get(this.elementsIDs.loginButtonID).click()
    }
}