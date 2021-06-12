from flask import jsonify
from flask import request
from flask import abort
from flask_restful import Resource
from database.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity

## /users routes
class UsersApi(Resource):
    def get(self):
        users = User.objects()
        return jsonify(users)

    def delete(self):
        users = User.objects().delete()
        return jsonify({message: "all users deleted" % userId})

## /users/<userId> routes
class UserApi(Resource):
    def get(self, userId):
        try:
            user = User.objects.get(id=userId)
            return jsonify(user)
        except Exception as e:
            print(e)
            return {'error': 'User not found : %s' % e}, 404
    
    def put(self, userId):
        body = request.json
        try:
            User.objects.get(id=userId).update(**body)
            return jsonify(User.objects.get(id=userId))
        except Exception as e:
            print(e)
            return {'error': 'User update failed : %s' % e}, 400  

    def delete(self, userId):
        try:
            User.objects.get(id=userId).delete()
            return jsonify({message: "user %s deleted" % userId})
        except Exception as e:
            print(e)
            return {'error': 'Couldnt delete user : %s' % e}, 400

## /users/me
class UserMeApi(Resource):
    @jwt_required()
    def get(self):
        try:
            # extract info from the jwt token
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            return jsonify(user)
        except Exception as e:
            print(e)
            return {'error': 'Internal error : %s' % e}, 500     

## /users/recipes
class UserRecipesApi(Resource):
    @jwt_required()
    def put(self):
        body = request.json
        try:
            # extract info from the jwt token
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            for r in body["recipes"]:
                ## appeller strapi pour récupérer la recette
                user.recipes.append(r)
            user.save()
            return jsonify(user)
        except Exception as e:
            print(e)
            return {'error': 'Internal error : %s' % e}, 500     