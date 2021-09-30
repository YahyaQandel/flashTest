import { Given, When, Then } from 'cypress-cucumber-preprocessor/steps';
import { BankApi } from '../../apis/bank.api';
import { UserApi } from '../../apis/user.api';
import { BankConnected } from '../../pages/bank-connected.page';
import { Bank } from '../../pages/bank.page';
import { Login } from '../../pages/login.page';
import { SuperUser, UserFactory } from '../../models/user';

let bankPage = new Bank();
let loginPage = new Login();
let bankConnectedPage = new BankConnected();
let accountNumber = "0";
let userapiObj = new UserApi();
let bankApi = new BankApi();
let bankName = "";
let testUser = new UserFactory();
let userApi = new UserApi();
before(()=>{
  userApi.register(testUser);
})
Given('there is no registered users', () => {
  // TODO: implement step
});

Given('there is a registered user has no bank account connected', () => {
  // TODO: implement step
});

When('user visits connect bank page', () => {
  bankPage.visit();
});

When('user visits login page', () => {
  loginPage.visit();
});


When('user logs in to system', () => {
  loginPage.perform(testUser.username,testUser.password);
});

When('fill bank field {string} and branch name {string} and account number {string} and account holder name {string}', (_bank, branchName: string, _accountNumber: string, accountHolderName: string) => {
  
  accountNumber = bankPage.generate_random_account_number();
  bankName = bankPage.get_bank();
  bankPage.fillFields(bankName,branchName,accountNumber,accountHolderName);
  cy.intercept("/bank/connected").as("connected_url")
  bankPage.connectBtn.click();
  cy.wait('@connected_url');
});

Then('user will be redirected to {string} to login', (login_page_url: string) => {
   cy.url().should(
    'equal',
    `${Cypress.config().baseUrl}${login_page_url}`
  );
});

Then('user will be redirected to {string} bank connected', (bank_connected_url: string) => {
   cy.url().should(
    'equal',
    `${Cypress.config().baseUrl}${bank_connected_url}`
  );
});

Then('bank name should be {string} and account number should be {string}', (_bank: string, _:string) => {
    bankConnectedPage.bankNameSpan.should('have.text', bankName);
    bankConnectedPage.accountNumberSpan.should('have.text', accountNumber);
    // teardown
    userapiObj.login(testUser.username,testUser.password).then(userLoginApiResponse => {
      let userToken = userLoginApiResponse.body.token;
      bankApi.deleteAccount(userToken,accountNumber);
      userapiObj.login(SuperUser.username,SuperUser.password).then(superUserLoginApiResponse => {
          let superUserToken = superUserLoginApiResponse.body.token;
          userapiObj.delete(superUserToken,testUser.username);  
      });
  });
});
