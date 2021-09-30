var faker = require('faker');

export class UserFactory {
    username: string ;
    password: string ;
    email :string ;

    constructor(){
        this.username = faker.name.firstName();
        this.password = faker.internet.password();
        this.email = faker.internet.email();
    }
}   

export class SuperUser {
    static username: string = "admin";
    static password: string = "5LP4BdB6HKvGptcD";
}
