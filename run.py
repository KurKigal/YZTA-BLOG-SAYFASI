from app import create_app, db
from app.models import User, Category, Post, Comment, PostLike

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Category': Category, 
        'Post': Post, 
        'Comment': Comment,
        'PostLike': PostLike
    }

if __name__ == '__main__':
    app.run(debug=True)
