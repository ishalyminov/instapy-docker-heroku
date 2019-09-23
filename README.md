# [ [ [Instapy] Docker] Heroku]
Run Instapy on Heroku in a Docker Container

<img src="instapy_heroku.jpg" alt="drawing" width="200"/>

Run your InstaPy in the Heroku cloud.

# How To

1. [Install Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) on your system and do
```bash
$ heroku login
```
2. Log in to Heroku container service
```bash
$ heroku container:login
```
3. Create the `.env` file (make sure Instagram credentials and proxy server parameters are set) - use `env_sample` as an example

4. Create a new Heroku app for your bot:
```bash
$ ./heroku_init.sh <your-app-name>
```
5. Push the code to Heroku and release it into your app:
```bash
$ heroku container:push instapy && heroku container:release heroku
```

6. Start the app:
```bash
$ heroku ps:scale instapy=1
```

7. Observe your Instagram grow!
```bash
$ heroku logs --tail
```
