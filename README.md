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
