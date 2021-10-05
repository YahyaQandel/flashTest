# Flash Task

#### according to the sotries written there is no need to register users, so i created some users and set their own data to test on it.

### Users in system:-
```
username    password            role            email
admin       5LP4BdB6HKvGptcD    superuser       admin@admin.com
cayden      8JmLGgZUsWKPcKUQ    flash-user      cayden@email.com
viaan       Jvuh6MUCX5H9Veq6    flash-user      viaan@email.com
ophelia     dmRzjkAR8Uw7AJBh    flash-user      ophelia@email.com
```

## Stories
#### it is a prerequisite to have `docker` and `docker-compose` installed on your machine and a good internet connection.
#### for the all upcoming stories you just need to have good internet connection and to run
```
docker-compose up django postgres
```
 and try using insomnia or DHC chrome extension or curl if you prefer

### Story 1 ( user can login using username or email )

`Post` request to `localhost:8000/oauth/token`
```
curl --request POST  --url http://localhost:8000/oauth/token  --header 'Content-Type: application/json'  --data "{\"username\": \"ophelia\",\"password\": \"dmRzjkAR8Uw7AJBh\"}"
```
or
```
curl --request POST  --url http://localhost:8000/oauth/token  --header 'Content-Type: application/json'  --data "{\"email\": \"ophelia@email.com\",\"password\": \"dmRzjkAR8Uw7AJBh\"}"
```

### Story 2 ( user can connect his bank )

1- visit page localhost:8000/bank/connect
2- `note` user can add more than one bank account

### Story 3 ( user can upload money to his flash account )
1- user should have a connected bank account ( already set for user `cayden` in the fixtures )

2- you should login and get an `authentication token` to use it.
```
curl --request POST  --url http://localhost:8000/oauth/token  --header 'Content-Type: application/json'  --data "{\"username\": \"cayden\",\"password\": \"8JmLGgZUsWKPcKUQ\"}"
```
3- send `Post` to `http://localhost:8000/api/v1/money/upload` using the `token`
``` 
curl --request POST  --url http://localhost:8000/api/v1/money/upload  --header 'Content-Type: application/json' --header 'Authorization: Basic TOKEN'  --data "{\"amount\": \"1000\"}" 
```

### Story 4 ( user can view his own flash balance )
1- first you should login and get an `authentication token` to use it.
2- send `Get` request to `http://localhost:8000/api/v1/user/balance/`
```
curl --request GET  --url http://localhost:8000/api/v1/user/balance  --header 'Content-Type: application/json' --header 'Authorization: Bearer TOKEN'
```

### Story 5 ( user can transfer money to another user )
1- first you should login and get an `authentication token` to use it.
2- user should have a connected bank account ( already set for user `cayden` in the fixtures )
3- send `Post` request to `http://localhost:8000/api/v1/money/transfer/`
```
curl --request GET  --url http://localhost:8000/api/v1/money/transfer  --header 'Content-Type: application/json' --header 'Authorization: Bearer TOKEN' --data "{\"amount\": \"1000\",\"username\": \"viaan\"}" 
```

### Story 6 ( user can transfer money to another user )
1- login to system from `localhost:800:/login` using one of the registered users above
2- visit `localhost:800:/money/currency/exchange`
`note` if user has a balance, you can view his new balance in exchanged rate according to
selected base currency 




## tests
### unit tests
- without docker
```
source venv/bin/activate
source store-postgres-creds.sh
./manage test
```
or 
- using docker
```
docker-compose run django python3 manage.py test
```

### e2e tests
the server should be running 
`docker-compose up`
from another termianl 
- without docker

change `e2e/cypress.json`  baseurl from '`django:8000`' to '`localhost:8000`'
```
cd e2e
npm i
npx cypress run
```
- using docker
```
bash build-and-run-e2e.sh
```