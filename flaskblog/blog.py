from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields
from .models import db, Post

blog = Blueprint('blog', __name__)
api = Namespace('blog', description='Blog operations')

post_model = api.model('Post', {
    'title': fields.String(required=True, description='Post title'),
    'content': fields.String(required=True, description='Post content'),
})

@api.route('/posts')
class PostList(Resource):
    @api.doc('list_posts')
    def get(self):
        """List all posts"""
        posts = Post.query.all()
        return jsonify([post.serialize() for post in posts]).json, 200

    @api.doc('create_post')
    @api.expect(post_model)
    def post(self):
        """Create a new post"""
        data = request.json
        title = data.get('title')
        content = data.get('content')

        if not title or not content:
            return {'message': 'Title and content are required'}, 400

        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()

        return {'message': 'Post created successfully', 'id': new_post.id}, 201

@api.route('/posts/<int:id>')
@api.response(404, 'Post not found')
@api.param('id', 'The post identifier')
class PostDetail(Resource):
    @api.doc('get_post')
    def get(self, id):
        """Fetch a single post by id"""
        post = Post.query.get_or_404(id)
        return post.serialize(), 200

    @api.doc('update_post')
    @api.expect(post_model)
    def put(self, id):
        """Update a post"""
        data = request.json
        title = data.get('title')
        content = data.get('content')

        if not title or not content:
            return {'message': 'Title and content are required'}, 400

        post = Post.query.get_or_404(id)
        post.title = title
        post.content = content
        db.session.commit()

        return {'message': 'Post updated successfully'}, 200

    @api.doc('delete_post')
    def delete(self, id):
        """Delete a post"""
        post = Post.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()

        return {'message': 'Post deleted successfully'}, 200

# Registering the blueprint and namespace
api.add_resource(PostList, '/posts', endpoint='posts')
api.add_resource(PostDetail, '/posts/<int:id>', endpoint='post')
