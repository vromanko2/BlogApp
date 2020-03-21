# BlogApp


### Open a terminal run following commands:

#####   git clone https://github.com/vromanko2/BlogApp.git
#####   cd BlogApp
#####   chmod +x entrypoint.sh
#####   docker-compose python web manage.py migrate
#####   docker-compose python web manage.py createsuperuser
#####   docker-compose up

### Open http://127.0.0.1:8000/admin
#####   Now, create some other users
#####   http://127.0.0.1:8000/admin/auth/user/add/
#####   And add some posts to a blog 
#####   http://127.0.0.1:8000/admin/blog_app/blog/


***
#### Testing api's: ####
http://127.0.0.1:8000/api/v1/blogs/ - returns all blogs<br/>
http://127.0.0.1:8000/api/v1/posts/ - returns all posts<br/>
http://127.0.0.1:8000/api/v1/users/ - returns all users<br/>
http://127.0.0.1:8000/api/v1/user/:id/subscribe/ - user with id=id subscribe on user, you input<br/>
http://127.0.0.1:8000/api/v1/user/:id/unsubscribe/ - user with id=id unsubscribe from user, you input<br/>
http://127.0.0.1:8000/api/v1/user/:id/news_feed - returns user's with id=id news feed<br/>
http://127.0.0.1:8000/api/v1/user/:id/create_post/ - create user's with id=id post<br/>
***

***
#### To test email sending: ####
Subscribe on somebody. Via api, admin or frontend.
Via admin: 
http://127.0.0.1:8000/admin/blog_app/usersubscribers/2/change/
Add some posts via choosed user's blog 
http://127.0.0.1:8000/admin/blog_app/blog/1/change/
You'll see an email message on console.
To send real messages, in settings.py uncomment from 138 to 145 lines.
Enter correct EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD and change some settings in your mail host.<br/>

***


### To test the app with a front-end:
#####   git clone https://github.com/vromanko2/BlogAppFront-end.git
#####   cd BlogAppFront-end
#####   docker-compose up --build





