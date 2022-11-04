# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game.

### Backend

The [backend](./backend/README.md) directory contains a completed Flask and SQLAlchemy server.

> View the [Backend README](./backend/README.md) for more details.

### API Documentation

### Endpoints

**GET /categories**

General:
- Returns a list of categories, success value
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

Sample: ```curl http://127.0.0.1:5000/categories```

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

**GET '/questions?page=${integer}'**

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

Sample: ```curl http://127.0.0.1:5000/questions?page=1```

```json
{
  "Categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "Questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },

    ...

    ], 
  "Success": true, 
  "Total Questions": 19
}

```

**GET /categories/{id}/questions**

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string paginated in groups of 10.

Sample: ```curl http://127.0.0.1:5000/categories/5/questions```

```json
{
  "current category": "Entertainment", 
  "questions found": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "success": true, 
  "total questions": 3
}
```

**DELETE /questions/{id}**

- Deletes the question of the given ID if it exists.
- Request Arguments: id - integer
- Returns: Does not return anything besides the appropriate HTTP status code. 

Sample ```curl -X DELETE http://127.0.0.1:5000/questions/5 ```

```json
{
  "Deleted question": 5, 
  "Success": true, 
  "Total questions now": 17
}
```

**POST /questions/{id}**

- Sends a post request in order to add a new question

Sample: ```curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Is 'Hello World!' mostly the first program to learn?", "answer": "Yes, it is commonly the first program to learn","category" :"1", "difficulty":"1"}'```
```json
{
    "success" : true,
    "question": "Is 'Hello World!' mostly the first program to learn?",
    "answer": "Yes, it is commonly the first program to learn", 
    "category": 1, 
    "difficulty": 1
}
```
Returns: Does not return any new data besides the appropriate HTTP status code. 



**POST /questions/search**

General:
- Sends a post request in order to search for a specific question by search term

Sample ```curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"trippy"}'```

```json
{
  "error": 404, 
  "message": "resource not found", 
  "success": false
}
```

Returns: array of questions, a number of total questions that met the search term and the current category string


**POST /quizzes**

General:
- Sends a post request in order to get the next question
- Request Body:

Sample``` curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"All","id":0}, "previous_questions":[10, 6, 17]}'``` 

- Returns: a single new question object

```json
{
  "question": {
    "answer": "Agra", 
    "category": "3", 
    "difficulty": 2, 
    "id": 15, 
    "question": "The Taj Mahal is located in which Indian city?"
  }, 
  "success": true
}
```


### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format the API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will get the core skill of being able to read and understand code.

> View the [Frontend README](./frontend/README.md) for more details.
