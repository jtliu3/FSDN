# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
Endpoints
GET '/categories'
GET '/questions'
DELETE '/questions/<int:question_id>'
POST '/questions'
POST '/questions/search'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a boolean success key and a categories key, that contains a object of id: category_string key:value pairs.

GET '/questions'
- Fetches a list of jsons with each question id, question string, answer, category, and difficulty paginated based on the current page
- Request Arguments: None
- Returns: An object with a boolean success key, a questions key, that contains an dictionary of question id, question string, answer, category, and difficulty, a total_questions key with the total number of returned questions in the dictionary, a categories key, that contains a object of id: category_string key:value pairs, and a current_category key of None.

DELETE '/questions/<int:question_id>'
- Deletes the question corresponding with the given question id from the database
- Request Arguments: question_id, an integer
- Returns: An object with a boolean success key, the question_id key with the question_id given, and a total_questions key with the number of questions after deletion.

POST '/questions'
- Inserts a new question with properties based on the form input
- Request Arguments: a json object with keys question, answer, category, and difficulty
- Returns: An object with a boolean success key and a totalQuestions key with the number of questions after insertion.

POST '/questions/search'
- Searches all questions in database based off of a given search term
- Request Arguments: a json object with a searchTerm key
- Returns: An object with a boolean success key, a questions key, that contains an dictionary of question id, question string, answer, category, and difficulty of the resulting question set, a total_questions key with the total number of returned questions in the dictionary, and a current_category key of None.

GET '/categories/<int:category_id>/questions'
- Gets all questions in the specified category
- Request Arguments: category_id, an integer
- Returns: An object with a boolean success key, a questions key, that contains an dictionary of question id, question string, answer, category, and difficulty of the questions in the category, a total_questions key with the total number of returned questions in the dictionary, and a current_category key of a dictionary of category id and type.

POST '/quizzes'
- Gets the questions one at a time randomly to play the quiz in the specified category, or all if nothing specified, ending when all questions have been played
- Request Arguments: a json object with the specified quiz_category, if any, and a list of previous_questions, if any
- Returns: An object with a boolean success key, a question key that contains an dictionary of question id, question string, answer, category, and difficulty of the next random question of the quiz, and a forceEnd boolean flagging if the quiz questions have all been played.
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```