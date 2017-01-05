# demo django products application

#### this is currently live at https://django-products-app.herokuapp.com/

#### Repo link: https://github.com/cubohan/django-products-app

##### Tech stack:
  (backend) django (python)
  (frontend) jquery
  (deployment) heroku

#### User stories:
  <****>As a User: (DEMO credentials: username: user; password: pass) Also, just signup and create new!
    (GOTO ~root url to automatically test this)
    -sign up and verify mail
    -login and view lists of products

  <****>As an Admin: (DEMO credentials: username: root; password: pass)
    (GOTO ~root/admin)
    -signup
    -CRUD everything including Users, Accounts, Products etc

#### Notable code:
  visit https://github.com/cubohan/django-products-app/tree/master/populate
    -This is the population script framework of sorts that I made for this assignment which is extensible
      and helps is writing easy, fail-safe population scripts for any Model
