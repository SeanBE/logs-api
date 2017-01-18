# Strength

[![Build Status](https://travis-ci.com/SeanBE/logs-api.svg?token=YwoffpzcxpVgFc4sk6nY&branch=master)](https://travis-ci.com/SeanBE/logs-api)

## Complete 1 a day.
- API: Fix Exercise Order with additional field.  Test needed!
- API: use factor boy.
- API: Coverage
- API: test_models
- Create User Workout relationship.
- ClIENT: Form validation.
- CLIENT: Redirect to workouts once one is created or updated.
- DOCKER: Weekly data volume backups (https://gist.github.com/SeanBE/a193150741134ee1d0c2b683480fd3f9)
- NGINX: Set up domain and SSL certificate from NameCheap.
- NGINX: Does nginx work properly as a reverse proxy?
- API: Logging format and add more logging.
- CLIENT: Recently used exercises.



- DOCKER figure out other volume without name.
- CLIENT: Workout comment if empty dont show.

- API: Identify missing issues (https://github.com/sloria/cookiecutter-flask)
- DOCKER: Be able to deploy anywhere (whether its local or remote server..)
- API: Flask notifications for events. (https://github.com/inveniosoftware/flask-notifications)
- API: Implement swagger.
- DOCKER: Use Fabric for deployment?
- DOCKER: Move all to alpine.
- API: Cache with REDIS.

@pytest.yield_fixture(scope='function')
def session(db):
    # connect to the database
    connection = db.engine.connect()
    # begin a non-ORM transaction
    transaction = connection.begin()

    # bind an individual session to the connection
    # options = dict(bind=connection, binds={})
    options = dict(bind=connection)
    session = db.create_scoped_session(options=options)

    # overload the default session with the session above
    db.session = session

    # overload session in factory classes
    for name, cls in inspect.getmembers(factories, inspect.isclass):
        if cls.__class__.__name__ == 'FactoryMetaClass':
            cls._meta.sqlalchemy_session = session

    yield session
    session.close()
    # rollback - everything that happened with the
    # session above (including calls to commit())
    # is rolled back.
    transaction.rollback()
    # return connection to the Engine
    connection.close()


@pytest.fixture()
def test_client(app):
    return app.test_client()


@pytest.fixture()
def item_data(session):
    return factories.ItemFactory.create_batch(10)


@pytest.fixture()
def item_history_data(session):
    return factories.ItemHistoryFactory.create_batch(10)


@pytest.fixture()
def api_url_data(session):
    items = factories.ItemFactory.create_batch(2)
    return {
        'items': items,
        'single_item_id': items[0].id
    }


## MAYBE
- settings_override on create_app?
- emails for user welcome
- Google Calendar Integration
- Body Weight
- Calendar (https://github.com/jinzhe/vue-calendar)
- Calendar (https://github.com/icai/vue2-calendar/blob/master/src/components/Calendar.vue)


https://github.com/nickjj/build-a-saas-app-with-flask
http://vanzaj.github.io/tdd-pytest/tdd-basics/
# @app.route('/someendpoint/' methods=['POST'])
# def some_endpoint():
#     """API endpoint for submitting data to
#
#     :return: status code 405 - invalid JSON or invalid request type
#     :return: status code 400 - unsupported Content-Type or invalid publisher
#     :return: status code 201 - successful submission
#     """
#     # Ensure post's Content-Type is supported
#     if request.headers['content-type'] == 'application/json':
#         # Ensure data is a valid JSON
#         try:
#             user_submission = json.loads(request.data)
#         except ValueError:
#             return Response(status=405)
#         ... some magic stuff happens
#         if everything_went_well:
#             return Response(status=201)
#         else:
#             return Response(status=405)

    #
    # # User submitted an unsupported Content-Type
    # else:
    #     return Response(status=400)
