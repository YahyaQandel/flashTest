import { Given, When, Then } from 'cypress-cucumber-preprocessor/steps';
import { UserApi } from '../../apis/user.api';
import {Login} from "../../pages/login.page"
import {UserFactory, SuperUser} from "../../models/user"
import { BankFactory } from '../../models/bank';
import { BankApi } from '../../apis/bank.api';

let loginPage = new Login()
let userApi = new UserApi()
let bankApi = new BankApi()
let userObj = {"username":"","password":""}
let testUser = new UserFactory();
let bank = new BankFactory();

before(()=>{
  userApi.register(testUser);
  console.log('reg:user')
  console.log(testUser)
})
Given('there is a registered user without connecting his bank account', (a: string) => {
  // user already in system fixtures
});

Given('that user has connected his bank account', (a: string) => {
   userApi.login(testUser.username,testUser.password).then(apiResponse => {
      let userToken = apiResponse.body.token;
      bankApi.connectAccount(userToken, bank);
  });
});

When('user visits login page', () => {
  loginPage.visit();
});

When('user logs in to system', () => {
  loginPage.perform(testUser.username,testUser.password);
});


Then('user will be redirected to {string} that verifies he has connected his bank account', (logged_in_url: string) => {
  cy.url().should(
    'equal',
    `${Cypress.config().baseUrl}${logged_in_url}`
  );
});

Then('user will be redirected to {string} that verifies he didnt connect his bank account', (logged_in_url: string) => {
  cy.url().should(
    'equal',
    `${Cypress.config().baseUrl}${logged_in_url}`
  );
});

after(()=>{
 userApi.login(SuperUser.username,SuperUser.password).then(apiResponse => {
      let userToken = apiResponse.body.token;
      userApi.delete(userToken, testUser.username);
  });
})