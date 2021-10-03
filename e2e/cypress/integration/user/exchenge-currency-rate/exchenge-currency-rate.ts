import { Given, When, Then } from 'cypress-cucumber-preprocessor/steps';
import { BankApi } from '../../apis/bank.api';
import { UserApi } from '../../apis/user.api';
import { BankConnected } from '../../pages/bank-connected.page';
import { Bank } from '../../pages/bank.page';
import { Login } from '../../pages/login.page';
import { SuperUser, UserFactory } from '../../models/user';

import { CurrencyExchange } from '../../pages/currency-exchange.page';

let bankPage = new Bank();
let loginPage = new Login();
let bankConnectedPage = new BankConnected();
let accountNumber = "0";
let userapiObj = new UserApi();
let bankApi = new BankApi();
let bankName = "";
let testUser = new UserFactory();
let userApi = new UserApi();
let currencyExchangePage = new CurrencyExchange();
before(()=>{
  userApi.register(testUser);
})

Given('there is a registered user', () => {
  // TODO: implement step
});

When('user visits login page', () => {
  loginPage.visit();
});

When('user logs in to system', () => {
  loginPage.perform(testUser.username,testUser.password);
});

When('user visits currency exchange rate page', () => {
  currencyExchangePage.visit();
});

When('user selects base currency {string}', (baseCurrency: string) => {
  currencyExchangePage.selectBaseCurrency(baseCurrency);
});

When('user change baes currency to {string}', (baseCurrency: string) => {
  currencyExchangePage.selectBaseCurrency(baseCurrency);
});

Then('exchanged rate for currency {string} should be {string}', (currencyKey: string, rate:string ) => {
  currencyExchangePage.getRateValueForBaseCurrency(currencyKey).invoke('text').then((txt)=>{  
    expect(parseFloat(txt)).closeTo(parseFloat(rate),1)
  })
});

after(()=>{
  // teardown
    userapiObj.login(testUser.username,testUser.password).then(userLoginApiResponse => {
      userapiObj.login(SuperUser.username,SuperUser.password).then(superUserLoginApiResponse => {
          let superUserToken = superUserLoginApiResponse.body.token;
          userapiObj.delete(superUserToken,testUser.username);  
      });
    });
})
