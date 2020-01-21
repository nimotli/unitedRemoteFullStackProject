## About
# Schema
The tables i've userd are 
    -User that contains email and password for auth, name  and positionn as a 2D coordinates "x-y"
    -Shop it contains shop name, shop type and position as a 2D coordinates "x-y"
    -UserShop it contains the user id as a foreign key, shop id as a foreign key and interraction (0 for dislike, 1 for like)
The distance (needed for displaying the shops) is calculated as follow:
    sqr( (userX - shopX)^2 + (userY - shopY)^2)
    userX and userY are the coordinates of the user
    shopX and shopY are the coordinates of the shop

Since the project requirement didn't specify where i should the coordinates or the distance, i thaught i'd get them as an attribute of the shop and the user, but the better solution would have been getting the location data from the user the getting the nearby shop using google API and then calculate the distance and sort.

# Authentication
The authentication uses JWT:
    -When a user signs in a JWT token gets created 
    -For all the actions that require a signin the token needs to be sent in the header alongside the required data
    -to logout the token needs to be destroyed

## User
# Sign up 
--------
POST /user/add
INPUT
{
    'id':'the id of the user',
    'email':'the email',
    'password':'the encrypted password',
    'name':'for display'
    'position':'for display'
}
OUTPUT
{
    'state':'success or failure',
    'errors':['error 1','error 2']
}
# Sign in
----------
POST /home
INPUT
{
    'email':'the email',
    'password':'the password',
}
OUTPUT
{
    'accessToken':'the jwt token',
}
# Get All Users
----------
GET /user
HEADER
{
    'accessToken':'the jwt token'
}

OUTPUT
{
    'users':[
        {'email':'',
        'password':'the hashed password',
        'name':'',
        'position':''},{}...
    ],
}
# Get User by public id
----------
GET /user/<userId>
HEADER
{
    'accessToken':'the jwt token'
}
INPUT
{
    'public_id':'the public id of the user',
}
OUTPUT
{
    'email':'',
    'password':'the hashed password',
    'name':'',
    'position':''
}
# DELETE User by public id
----------
DELETE /user/<userId>
HEADER
{
    'accessToken':'the jwt token'
}
INPUT
{
    'public_id':'the public id of the user',
}
OUTPUT
{
    'message':'deleted',
    'state':'success/failure',
}
## Shop

# Get all shops
----------
GET /shop
HEADER
{
    'accessToken':'the jwt token'
}
OUTPUT
{
    'shops':[
        {'shopType':'the type of the shop',
        'name':'',
        'position':''},{},...
    ]
}
# Get a shop
----------
GET /shop/<shopid>
HEADER
{
    'accessToken':'the jwt token'
}
INPUT
{
    'shop_id':'the id of the shop',
}
OUTPUT
{
    'shopType':'the type of the shop',
    'name':'',
    'position':''
}
# Like a shop
----------
POST /like
HEADER
{
    'accessToken':'the jwt token'
}
INPUT
{
    'shop_id':'the id of the shop',
}
OUTPUT
{
    'state':'success/failure',
    'message':'liked',
}
## UserShops
this table is to keep track of which shop has been liked by which user (since its a many to many ralation a third table is needed)
# Get all UserShop
GET /userShop
HEADER
{
    'accessToken':'the jwt token'
}
OUTPUT
{
    'userShops':[
        {'user':'the id of the user FK',
        'shop':'the id of the shop FK',
        'interraction':'the interraction 1 for like 0 for dislike'},{},...
    ]
}
