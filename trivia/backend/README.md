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

## API Reference
### Getting Started
Base URL: This project runs locally. The backend app is hosted at the default `https://127.0.0.5000` which is set as a proxy in the frontend configuration.
Authentication: Does require authentication

### Error Handling
Errors are returned as JSON in the following format
```
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```
The API return the following error when request fails:
- 404: resource not found
- 422: unprocessable
- 405: method not allowed
- 400: bad request
- 500: internal server error

### Endpoints
#### GET /questions
- Questions are retrieved on this route. Depending on page argument value in request the route handler returns questions paginated, number of total questions and categories of these paginated questions. 
- Sample `curl http://127.0.0.1:5000/questions?page=2`
```
{
  "categories": [
    3,
    2,
    2,
    2,
    2,
    1,
    1,
    1,
    4
  ],
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "total questions": 19
}
```
#### GET /categories
- All categories are retrieved on this route.
- Sample `curl http://127.0.0.1:5000/categories`
```
{
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"
}
```
#### DELETE /questions/{question_id}
- Deletes a question with id `question_id` and return JSON with property "success" set to True.
- Sample `curl -X DELETE http://127.0.0.1:5000/questions/3`
```
{
    "success": True
}
```
#### POST /questions
- Add a new question to database. The required request body contains question, answer and categories. Returns JSON with property "success" set to True.
- Sample `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question": "Who built the pyramids?", "answer": "The pharoahs", "category": 4, "difficulty": 3}' `
On windows the json body should be written with double quotations instead of single quotations with backslaches `-d "{\"question\": \"..\" ..}"`
```
{
    "success": True
}
```
#### POST /search
- Search questions based on a search term sent in JSON request body. It returns questions including this term and total number of questions.
- Sample `curl -X POST http://127.0.0.1:5000/search -H "Content-Type: application/json" -d '{"searchTerm": "Where"}`
On windows `-d "{\"searchTerm\": \"What\"}"`
```
{
  "current_category": null,
  "questions": [
    "What boxer's original name is Cassius Clay?",
    "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
    "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
    "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
    "What is the largest lake in Africa?",
    "What is the heaviest organ in the human body?"
  ],
  "total_question": 6
}
```
#### GET /categories/{question_category}
- Get all questions based on a particular category.
- Sample `curl http://127.0.0.1:5000/categories/3`
```
{
  "questions": [
    "What is the largest lake in Africa?",
    "In which royal palace would you find the Hall of Mirrors?",
    "The Taj Mahal is located in which Indian city?"
  ]
}
```

#### POST /quizzes
- A random question is sent based on optional categories and previous questions sent that should not include this question
- Sample `curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions": ["Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?", "Which country won the first ever soccer World Cup in 1930?"]}'`
On windows -d `"{\"previous_questions\": [\"\", \"\"]}"`
```
{
  "question": "How many paintings did Van Gogh sell in his lifetime?"
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```