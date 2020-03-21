# BlogApp


### Open a terminal run following commands:

##### git clone https://github.com/vromanko2/BlogApp.git
##### cd BlogApp
##### chmod +x entrypoint.sh
##### docker-compose python web manage.py migrate
##### docker-compose python web manage.py createsuperuser
##### docker-compose up

### Open http://127.0.0.1:8000/admin
##### Now, create some other users
##### http://127.0.0.1:8000/admin/auth/user/add/
##### And add some posts to a blog 
##### http://127.0.0.1:8000/admin/blog_app/blog/

##### But to test the app with a front-end:
##### git clone https://github.com/vromanko2/BlogAppFront-end.git
##### cd BlogAppFront-end
##### docker-compose up --build





