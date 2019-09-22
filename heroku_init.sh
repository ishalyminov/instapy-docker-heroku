NAME=$1
echo $NAME
heroku create $NAME

heroku buildpacks:add heroku/python
heroku plugins:install heroku-config

heroku config:push

