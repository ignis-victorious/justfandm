
### add user ###
POST http://0.0.0.0:8000/users/ 
Content-Type: application/json

{
    "username": "test",
    "email": "test@gmail.com",
    "full_name": "test user",
    "bio": "test bio",
    "password": "test123"
}

###
POST http://0.0.0.0:8000/users/
Content-Type: application/json

{
    "username": "test2",
    "email": "test2@gmail.com",
    "full_name": "test user",
    "bio": "test bio",
    "password": "test123"
}

### get user ###
GET http://0.0.0.0:8000/users/ 


### get user by id ###