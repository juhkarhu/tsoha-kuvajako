# tsoha-kuvaruutu
The app has a wall that shows posts by other users. 
Posts can be commented. 
User can be either regular user or admin. 

### Description of planned functionalities
* User can create an account, log in and log out. 
* On the front page user sees posts by other users, who and when was it uploaded, and how many comments does the post has.
* User can upload an image with the post (the image will be mandatory) and write a description about it.
* User can comment on other user's posts.
* Users have their own profile pages that shows the number of posts and comments written by the users.
* User can delete own posts and comments.
* Users can search for pictures with words that are in the respective posts.
* Users can send each other messages. 
* Admin can delete posts and comments.
* Admin can remove an account (or suspend it?)

### Installation and running. 
- Create the virtual environment:
`python3 -m venv venv`
- Enter the virtual environment:
`source venv/bin/activate`
- Install required dependencies:
`pip install -r requirements.txt`
- Create .env environment file and add some kind of SECRET_KEY and set your psql data ul to DATABASE_URL.
- Set up the database:
`psql < schema.sql`
- Run the application with:
`python run.py`


### Tilanne 29.3.2021

Crude functionality has been formed.

### Tilanne 8.4.2021

The UI has been altered and added some functionality. 

### Tilanne 23.4.2021

The image is resized before being added to the db. You get to the post by clicking the image and the data shown on the profile page has been reworked. Users can delete their own posts and comments from their profile page. 

### Tilanne 25.4.2021

Both users and admins can delete posts and comments, and admins can ban users. The implementation is harsh as there's no any kind of confirmation as of yet. 

### Current status
Done: 
Users can login (and create accounts), post and comment on other's posts and delete their own posts and comments (they remain visible to the author in the profile section). 
Image are resized before being added to the db. 
Users: deleting posts and comments.
Admin: deleting posts, comments and banning users. 

TODO: 
Messages. 

## Heroku
The app can be tested on heroku at:
https://tsoha-kuvaruutu.herokuapp.com