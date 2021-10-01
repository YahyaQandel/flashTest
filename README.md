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

#### for the all upcoming stories you just needs to have good internet connection and to run
#### `docker-compose up` and try using insomnia or DHC chrome extension or curl if you prefer

## Story 1 ( user can login using username or email )

`post` request to `localhost:8000/oauth/token`
```
curl --request POST  --url http://localhost:8000/oauth/token  --header 'Content-Type: application/json'  --data "{\"username\": \"ophelia\",\"password\": \"pass_#_user\"}"
```
or
```
curl --request POST  --url http://localhost:8000/oauth/token  --header 'Content-Type: application/json'  --data "{\"email\": \"ophelia@email.com\",\"password\": \"pass_#_user\"}"
```

## Story 2 ( user can connect his bank )

visit page localhost:8000/bank/connect
`note` user can add more than one bank account

## Story 3 ( user can upload money to his flash account )
1- user should have a connected bank account ( already set for user `cayden` in the fixtures )
2- you should login and get an `authentication token` to use it.
```
curl --request POST  --url http://localhost:8000/oauth/token  --header 'Content-Type: application/json'  --data "{\"username\": \"cayden\",\"password\": \"8JmLGgZUsWKPcKUQ\"}"
```
3- send `post` to `http://localhost:8000/api/v1/money/upload` using the `token`
``` 
curl --request POST  --url http://localhost:8000/api/v1/money/upload  --header 'Content-Type: application/json' --header 'Authorization: Basic TOKEN'  --data "{\"amount\": \"1000\"}" 
```

## Story 4 ( user can view his own flash balance )
1- first you should login and get an `authentication token` to use it.
2- send `Get` request to `http://localhost:8000/api/v1/user/balance/`
```
curl --request GET  --url http://localhost:8000/api/v1/user/balance  --header 'Content-Type: application/json' --header 'Authorization: Bearer TOKEN'
```

