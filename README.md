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
}
check the submited data and validate
OUTPUT
{
    'state':'success or failure',
    'errors':['error 1','error 2']
}
# Sign in
----------
POST