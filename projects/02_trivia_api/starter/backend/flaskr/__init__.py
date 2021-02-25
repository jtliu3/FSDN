import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)

  '''
  Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
    return response

  '''
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    try:
      categories = {category.id:category.type for category in Category.query.order_by(Category.id).all()}
      result = {
        'success': True,
        'categories': categories
      }
      return jsonify(result)
    except:
      abort(404)

  '''
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
    try:
      page = request.args.get('page', 1, type=int)
      first = QUESTIONS_PER_PAGE * (page-1)
      last = first + QUESTIONS_PER_PAGE
      questions = [question.format() for question in Question.query.order_by(Question.id).all()]
      if len(questions[first:last]) == 0:
        abort(404)
      result = {
        'success': True,
        'questions': questions[first:last],
        'total_questions': len(questions),
        'categories': {category.id:category.type for category in Category.query.order_by(Category.id).all()},
        'current_category': None
      }
      return jsonify(result)
    except:
      abort(404)

  '''
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
      if question is None:
        abort(422)
      question.delete()
      return jsonify({
          'success': True,
          'question_id': question_id,
          'total_questions': len(Question.query.all())
        })
    except:
      abort(422)

  ''' 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def insert_question():
    try:
      reqbody = request.get_json()
      question_text = reqbody.get('question',None)
      answer_text = reqbody.get('answer',None)
      category_num = reqbody.get('category',None)
      difficulty_score = reqbody.get('difficulty',None)
      if (question_text is None or answer_text is None or category_num is None or difficulty_score is None):
        abort(422)
      question = Question(question=question_text, answer=answer_text, category=category_num, difficulty=difficulty_score)
      question.insert()
      return jsonify({
          'success': True,
          'totalQuestions': len(Question.query.all())
        })
    except:
      abort(422)

  '''
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route("/questions/search", methods=['POST'])
  def search_questions():
    try:
      reqbody = request.get_json()
      search_term = reqbody.get('searchTerm', '')
      search_results = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
      questions = [question.format() for question in search_results]
      result = {
        'success': True,
        'questions': questions,
        'total_questions': len(questions),
        'current_category': None
      }
      return jsonify(result)
    except:
      abort(404)

  '''
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route("/categories/<int:category_id>/questions", methods=['GET'])
  def get_questions_by_category(category_id):
    try:
      search_results = Question.query.filter(Question.category == str(category_id)).all()
      questions = [question.format() for question in search_results]
      category = Category.query.filter(Category.id == category_id).one_or_none()
      result = {
        'success': True,
        'questions': questions,
        'total_questions': len(questions),
        'current_category': category.format()
      }
      return jsonify(result)
    except:
      abort(422)

  '''
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route("/quizzes", methods=['POST'])
  def get_quiz_questions():
    try:
      reqbody = request.get_json()
      category = reqbody.get('quiz_category', None)
      prev_questions = reqbody.get('previous_questions',[])
      if(category['id'] == 0):
        all_questions = Question.query.all()
      else:
        all_questions = Question.query.filter(Question.category == str(category['id'])).all()
      remaining_questions = [question.format() for question in all_questions if question.id not in prev_questions]
      if (len(remaining_questions) > 0):
        next_question = random.choice(remaining_questions)
        force_end = False
      else:
        next_question = None
        force_end = True
      return jsonify({
          'success': True,
          'question': next_question,
          'forceEnd': force_end
        })
    except:
      abort(422)

  '''
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Page Not Found'
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable Entity'
      }), 422

  return app

    