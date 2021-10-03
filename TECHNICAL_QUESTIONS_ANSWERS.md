#### 1. What would you add to your solution if you had more time?
- more test cases to cover bank validation e2e for example.
- refactor some functionalty and encapulste it inside its appropriate class
- enanhce how views handle reqeusts, could make use of mixins and serializer validations
- dockerize e2e tests to run independent
- create a CD playbook or the system to get deployed easily
- separate the ui from system ( using React/Angular )
- enhance the ui styling

#### 2. What is the best approach you found to structuring your apps ? Please give an example of the folder outline and discuss pros and cons of this structure.
- as it appears in the application strucure i have used the 3 applications ( money, bank , user) and it was confusing at beginning where to include some functionality as it could fit in both apps as it itersects through both of them
- separating the apis urls form template urls so it is easier for future reference to specify where to add new pages/endpoints.
- if i have time i would separate the views also ( api views / template views)

#### 3. What was the most useful feature added to the latest version of your chosen language? Please include a snippet of code that shows how you've used it (ifapplicable).
- Nothing till now ( actually don't remember )

#### 4. How would you track down a performance issue in production? Have you ever had to do this?
- it is a long procedure actually, the traditioanl way is to have a dump of the running database on production itself and run it locally and try to reproduce the performance issue.
- yes i have faced that alot but without a big scale data.

#### 5. How would you monitor and trace issues in a distributed systems environment?
- i will use a montering tool ( openTelemetry ) to measure the performance of system requests and responses for example injecting its tracing code on each service to trace the requests coming from - to that service.
- i have never done that in person but now managing a team that is doing a full system microservices tracing.

