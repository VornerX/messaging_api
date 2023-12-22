Simple Messaging API
-----
### Installation
_The first step is to clone the repository_.<br>
Then, there are two options for starting the application: using a **Docker environment** or 
**launching it manually** as a uvicorn app from the command line.
#### Using Docker environment:
1. Make sure that you have Docker (and docker-compose) installed. 
See `https://docs.docker.com/desktop/` for details.
2. If you're running a UNIX-based OS (Linux, macOS, FreeBSD, etc.) and it's your
first run, execute the following script from the root directory of the project:

```
./build.sh
```
Then start it using the command below:
```
docker-compose up
```
The default port 8000 will be exposed to 9000 on localhost, and you can access
the Swagger UI at `http://localhost:9000/docs`.

#### Alternatively, you can launch it on a host PC manually
To achieve this, you need to make the following steps:
1. Make sure that you have Python 3.9+ installed.
2. In the root directory of the app, execute the following CLI command to 
create a virtual environment:
```
python3 -m venv venv
```
3. Activate it. If you're running a UNIX-based OS, run:
```
source venv/bin/activate
```
If you're running Windows, run:
```
venv\Scripts\activate.bat
```
4. Install the requirements from the root directory:
```
pip3 install -r requirements.txt
```
5. Launch the application by running the command (you can choose any free port 
on your host):
```
python -m uvicorn messaging_api.main:app --host=localhost --port=9000 --reload
```
As in the previous setup option, you can then access it at 
`http://localhost:9000/docs`.

### Running tests
1. In the case of running the application under the Docker environment, the tests
will be launched in their own container before the application container, so you'll be able to see the test results in STDOUT.
2. If you're running the application locally, then just activate venv and 
execute the following command line to see the results:
```
pytest
```
### Usage
In the default configuration, the Swagger UI for the API can be reached at 
`http://localhost:9000/docs`. The Messaging API provides basic 
authentication using headers.

>**All requests to its endpoints (except user registration) should contain 
"username" and "password" headers to gain access to the API.**

There are four endpoints, which can be called using Swagger UI
or Postman, according to the pattern `http://localhost:9000/<URL PATH>/`:
1.  Create (register) a new user.
  * URL path: `/users/`
  * HTTP Method: `POST`
  * Example of a JSON request payload: 
  `{"username": "john_doe", "password": "derpasswort"}`
  * After successful registration, these credentials can be used as
    authentication headers for all further requests.
  * Authentication is not required.
2. Get a list of existing users.
  * URL path: `/users/`
  * HTTP Method: `GET`
  * This endpoint supports basic (optional) limit/offset pagination
    which can be used as follows: 
   `http://127.0.0.1:8000/users/?skip=0&limit=100`
  * Authentication is required.
3. Create a message from a user.
  * URL path: `/users/{user_id}/messages/` where {user_id} is the ID of an 
  existing user.
  * HTTP Method: `POST`
  * Creating messages on behalf of other users is not allowed.
  * Authentication is required.
4. Get a list of messages.
  * URL path: `/messages/` or `/messages/?user_id={user_id}`
  * HTTP Method: `GET`
  * If `user_id` is provided, the endpoint will return messages for the given
    user; otherwise, all messages will be returned.
  * Authentication is required.
