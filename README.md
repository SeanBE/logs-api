# Strength

[![Build Status](https://travis-ci.com/SeanBE/strength.svg?token=YwoffpzcxpVgFc4sk6nY&branch=master)](https://travis-ci.com/SeanBE/strength)

## Complete 1 a day.
- API: test_models and test_mixins
- API: Fix Exercise Order with additional field. Create User Workout relationship.
- ClIENT: Form validation.
- CLIENT: Redirect to workouts once one is created or updated.
- DOCKER: Weekly data volume backups.
- NGINX: Set up domain and SSL certificate from NameCheap.
- NGINX: Does nginx work properly as a reverse proxy?
- API: Logging format and add more logging.
- CLIENT: Recently used exercises.

- API: Identify missing issues (https://github.com/sloria/cookiecutter-flask)
- DOCKER: Be able to deploy anywhere (whether its local or remote server..)
- API: Flask notifications for events. (https://github.com/inveniosoftware/flask-notifications)
- API: Implement swagger.
- DOCKER: Use Fabric for deployment?
- DOCKER: Move all to alpine.
- API: Cache with REDIS.

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
