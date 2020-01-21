## User
The authentication uses JWT:
    -When a user signs in a JWT token gets created 
    -For all the actions that require a signin the token needs to be sent in the header alongside the required data
    -to logout the token needs to be destroyed
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
