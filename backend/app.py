from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={'/': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        if len(categories) == 0:
            abort(404)
        return jsonify({'success': True, 'categories': {
                       category.id: category.type for category in categories}})

    @app.route('/questions')
    def get_questions():
        try:
            questions = Question.query.all()
            categories = Category.query.all()
            if len(questions) == 0 or len(categories) == 0:
                abort(404)
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
            questions = [question.format() for question in questions]

            return jsonify({
                'success': True,
                'total_questions': len(questions),
                'categories': {category.id: category.type for category in categories},
                'questions': questions[start:end],
            }), 200
        except BaseException:
            abort(404)

    @app.route('/questions/<int:questions_id>', methods=['DELETE'])
    def delete_question(questions_id):
        try:
            Question.query.get(questions_id).delete()
            return jsonify({
                'success': True,
                'message': "The Question deleted"}), 200
        except BaseException:
            abort(404)

    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            data = request.get_json()
            question, category = data.get(
                'question', ''), data.get(
                'category', '')
            difficulty, answer = data.get(
                'difficulty', ''), data.get(
                'answer', '')

            if question == '' or category == '' or difficulty == '' or answer == '':
                return abort(422)

            question = Question(
                difficulty=difficulty,
                answer=answer,
                question=question,
                category=category)

            question.insert()
            return jsonify(
                {'success': True, 'message': "The Question Created"}), 201
        except BaseException:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        data = request.get_json()
        search_term = data.get('searchTerm', '')
        page = request.args.get('page', 1, type=int)
        if search_term == '':
            abort(422)
        else:
            questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
            questions = [question.format() for question in questions]

            if len(questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': questions[start:end],
                'total_questions': len(Question.query.all())
            }), 200

    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        page = request.args.get('page', 1, type=int)
        category = Category.query.filter_by(id=category_id).one_or_none()
        if category:
            questions = Question.query.filter_by(category=category_id).all()
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
            questions = [question.format() for question in questions]
            return jsonify({
                'success': True,
                'questions': questions[start:end],
                'total_questions': len(questions),
                'current_category': category.type}), 200
        else:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        data = request.get_json()
        previous_questions = data.get('previous_questions')
        quiz_category = data.get('quiz_category')
        if quiz_category['id'] == 0:  # all categories
            questions_by_category = Question.query.filter(Question.id.notin_(previous_questions)).all()

        else:  # specific category
            questions_by_category = Question.query. \
                filter_by(category=quiz_category['id']). \
                filter(Question.id.notin_(previous_questions)). \
                all()

        if len(previous_questions) >= len(questions_by_category):
                # some categories have less than 5 questions
                # so we complete the missing questions by random questions
                questions_all = Question.query.all()
                next_question = questions_all[random.randint(0, len(questions_all) - 1)]
        else:
            next_question = questions_by_category[random.randint(0, len(questions_by_category) - 1)]

        return jsonify(
            {'success': True, 'question': next_question.format()}), 200

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(
            {'error': '400', 'massage': 'Bad Request', 'success': False}), 400

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify(
            {'error': '404', 'massage': 'Page not found', 'success': False}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify(
            {'error': '422', 'massage': 'Page not found', 'success': False}), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify(
            {'error': '500', 'massage': 'Internal Server Error', 'success': False}), 500
    return app



if __name__ == '__main__':
    app = create_app()

    app.run(debug=True)