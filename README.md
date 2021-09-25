# Flash Task

#### according to the sotries written there is no need to register users, so i created some users and set their own data to test on it.

### Users in system:-
```
username    password            role            email
admin       5LP4BdB6HKvGptcD    superuser       admin@admin.com
cayden      test!!!pass         flash-user      cayden@email.com
viaan       test!!!pass         flash-user      viaan@email.com
ophelia     pass_#_user         flash-user      ophelia@email.com
```

#### for the all upcoming stories you just needs to have good internet connection and to run
#### `docker-compose up` and try using insomnia or DHC chrome extension or curl if you prefer

## Story 1 ( user can login using username or email )

send `post` request to `localhost:8000/oauth/token`
```
body {"username":"cayden","password":"test!!!pass"}
or
body {"email":"cayden@email.com","password":"test!!!pass"}
```
