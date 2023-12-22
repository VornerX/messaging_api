Simple Messaging API
-----
### Installation
There two options of starting the application: using a **Docker environment** or 
**launch it manually** as uvicorn app from the command line.
#### Using Docker environment:
1. Make sure that you have Docker (and docker-compose as well) installed. 
See here `https://docs.docker.com/desktop/` for details.
2. If you're running UNIX-based OS (Linux, macOS, FreeBSD, etc.) and it's a
first run, execute the following script from the root directory of a project
```
./build.sh
```
And then start it, using the command below:
```
docker-compose up
```
The default port 8000 will be exposed to 9000 on localhost and you can access
the Swagger UI by the address of `http://localhost:9000/docs`

#### Alternatively you can launch it on a host PC manually
To achive it, you need to make the following steps:
1. Make sure that you have Python 3.9+ installed.
2. In a root directory of an app execute the following CLI command to 
create virtual env
```
python3 -m venv venv
```
3. Activate it. If you're running UNIX-based OS run
```
source venv/bin/activate
```
If you're running Windows, run
```
venv\Scripts\activate.bat
```
4. Install the requirements from the root directory:
```
pip3 install -r requirements.txt
```
5. Launch the application, by running command (you can choose any free port 
on your host)
```
python -m uvicorn messaging_api.main:app --host=localhost --port=9000 --reload
```
As in a previous option of a setup you can access it then on 
`http://localhost:9000/docs`.

### Running tests
1. In a case of running the application under the Docker environment, the tests
will be launched in their own container, before the container of an 
application, so you'll be able to see the test results in STDOUT.
2. If you're running the application locally, then just activate venv and 
execute in command line to see the results:
```
pytest
```
### Usage
In a default configuration, the Swagger UI for API can be reached by the 
following URL `http://localhost:9000/docs`. Messaging API provides a basic 
authentication using headers.

>**All requests to its endpoints (except user registration) should contain 
"username" and "password" headers in order to get access to the API.**

There are four endpoints, which can be called using Swagger UI
or Postman, according to the pattern `http://localhost:9000/<URL PATH>/`:
1.  Create (register) new user.
  * URL path: `/users/`
  * HTTP Method: `POST`
  * Example of JSON request payload: 
  `{"username": "john_doe", "password": "derpasswort"}`
  * After successfull registration these credentials can be used as
    an authentication headers for all further requests.
  * Authentication is not required.
2. Get list of existing users.
  * URL path: `/users/`
  * HTTP Method: `GET`
  * This endpoint supports basic (optional) limit/offset pagination
    which can be used in a following way: 
   `http://127.0.0.1:8000/users/?skip=0&limit=100`
  * Authentication required.
3. Create a message from user.
  * URL path: `/users/{user_id}/messages/` where {user_id} is ID of an 
  existent user.
  * HTTP Method: `POST`
  * Creating messages on behalf of other users is not allowed.
  * Authentication required.
4. Get list of messages.
  * URL path: `/messages/` or `/messages/?user_id={user_id}`
  * HTTP Method: `GET`
  * If `user_id` is provided an endpoint will return messages for the given
    user, otherwise all messages will be returned.
  * Authentication required.