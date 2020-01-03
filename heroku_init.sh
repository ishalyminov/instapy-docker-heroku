NAME=$1
echo $NAME
heroku create $NAME

heroku buildpacks:add heroku/python
heroku plugins:install heroku-config

cat .env | xargs heroku config:set

