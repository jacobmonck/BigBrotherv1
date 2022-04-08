# BigBrother

A simple yet useful bot designed for large server to help aid moderation by allowing moderators quick and easy access to user's messages via Discord's search feature. 

## How it works

The infrastructure is very simple by nature as I wanted this to be as fast and easy to write as possible. With the being said here are the technologies the bot is using (so far).

- Redis - Caching layer to avoid unnessary calls to the API as well as the database. *This is not persistent storage
- PostgreSQL - Persistent disk storage where all guild information is stored and retrieved from to later be cached.
- FastAPI (API) - The core internal API serivce that allows the bot fetch information if it's not already in the cache as well as creating, updating, fetching, and deleting values in the database. 

![New Flowchart(1)](https://user-images.githubusercontent.com/77035482/162532216-11dd4167-6357-4530-82ba-597aad0bfb23.png)
