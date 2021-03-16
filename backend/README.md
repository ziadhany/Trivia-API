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

```
Endpoints
GET '/categories' , '/questions' , '/categories/<int:category_id>/questions'
POST ... '/questions' , '/questions/search', '/quizzes'
DELETE ... '/questions/<int:questions_id>'
```

##### GET '/categories'
```
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

##### GET '/questions' 
```
- Fetches a dictionary of questions and paginate it with page argument 
- Request Arguments: ?page=
- curl http://localhost:3000/questions?page=1  
Returns: 
categories	Object { 1: "Science", 2: "Art", 3: "Geography", … }
questions	[ {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…} ]
success	true
total_questions	16
```

##### GET '/categories/<<int:category_id>>/questions''
```
- Fetches a dictionary of questions related to the categories 
- Request Arguments: category_id , 
- curl http://localhost:3000/categories/5/questions 
Returns:  
{current_category: Entertainment,
questions:[ {…}, {…}, {…} ],
success	:true,
total_questions	: 3}
```
##### POST '/questions'' 
```
- Create a New Question
- Request Arguments: question,answer,difficulty ,category
- curl -X POST http://localhost:3000/questions -H "Content-Type: application/json" \
    -d '{"question":"What is the heaviest organ in the human body?","answer":"The Liver","difficulty":4,"category":"1"}' 
Response:  
{
  "message": "The Question Created", 
  "success": true
}
```
##### POST '/questions/search'
```
- Search for Questions 
- Request Arguments: searchTerm
- curl -X POST http://localhost:3000/questions/search -H "Content-Type: application/json" \
    -d '{"searchTerm":"did"}' 
Response:  
{  "questions": [
    {
      "answer": "Tom Cruise","category": 5, "difficulty": 4, "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "One","category": 2, "difficulty": 4, "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ], 
  "success": true, 
  "total_questions": 20
}

```
##### POST '/quizzes'
```
- play quizzes ( get a question and answer baised on category and previous questions )
- Request Arguments: [previous_questions] , quiz_category:{type,id}
- curl -X POST http://localhost:3000/quizzes -H "Content-Type: application/json" \
    -d '{"previous_questions":[],"quiz_category":{"type":"History","id":"4"}}' 
Response :-
{
  "question": {
    "answer": "Scarab", 
    "category": 4, 
    "difficulty": 4, 
    "id": 23, 
    "question": "Which dung beetle was worshipped by the ancient Egyptians?"
  }, 
  "success": true
}
```
##### DELETE '/questions/<<int:questions_id>>'
```
- DELETE a Question 
- Request Arguments: id 
- curl -X DELETE http://localhost:3000/questions/1 -H "Content-Type: application/json" 
Response :- 
 {
  "message": "The Question deleted", 
  "success": true
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