from flask import render_template, redirect, url_for, flash, request, abort, current_app, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User, Post, Comment, Category, PostLike
from app.forms import RegistrationForm, LoginForm, PostForm, CommentForm, SearchForm

def init_app(app):
    """Route'ları uygulamaya kaydet"""
    
    @app.context_processor
    def inject_search_form():
        return dict(search_form=SearchForm())
    
    # ==================== ANA SAYFA ====================
    @app.route('/')
    @app.route('/index')
    def index():
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(
            page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False
        )
        categories = Category.query.order_by(Category.name).all()

        # Popüler yazarları like'a göre sıralayalım
        popular_authors = db.session.query(
            User, 
            db.func.count(PostLike.id).label('total_likes')
        ).join(Post, User.id == Post.user_id)\
         .join(PostLike, Post.id == PostLike.post_id)\
         .group_by(User.id)\
         .order_by(db.desc('total_likes'))\
         .limit(3)\
         .all()

        return render_template('index.html', title='Ana Sayfa', posts=posts, 
                             categories=categories, popular_authors=popular_authors)
    
    # ==================== KATEGORİ FİLTRELEME ====================
    @app.route('/category/<int:category_id>')
    def category_posts(category_id):
        category = Category.query.get_or_404(category_id)
        page = request.args.get('page', 1, type=int)
        posts = Post.query.filter_by(category_id=category_id).order_by(
            Post.date_posted.desc()
        ).paginate(page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
        categories = Category.query.order_by(Category.name).all()
        
        # Popüler yazarları like'a göre sıralayalım
        popular_authors = db.session.query(
            User, 
            db.func.count(PostLike.id).label('total_likes')
        ).join(Post, User.id == Post.user_id)\
         .join(PostLike, Post.id == PostLike.post_id)\
         .group_by(User.id)\
         .order_by(db.desc('total_likes'))\
         .limit(3)\
         .all()
        
        return render_template('index.html', title=category.name, posts=posts, 
                             categories=categories, current_category=category, 
                             popular_authors=popular_authors)
    
    # ==================== KAYIT ====================
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Hesabınız başarıyla oluşturuldu! Şimdi giriş yapabilirsiniz.', 'success')
            return redirect(url_for('login'))
        
        return render_template('register.html', title='Kayıt Ol', form=form)
    
    # ==================== GİRİŞ ====================
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Geçersiz e-posta veya şifre.', 'error')
                return redirect(url_for('login'))
            
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('index')
            flash(f'Hoş geldin, {user.username}!', 'success')
            return redirect(next_page)
        
        return render_template('login.html', title='Giriş Yap', form=form)
    
    # ==================== ÇIKIŞ ====================
    @app.route('/logout')
    def logout():
        logout_user()
        flash('Başarıyla çıkış yaptınız.', 'info')
        return redirect(url_for('index'))
    
    # ==================== YAZI OLUŞTUR ====================
    @app.route('/post/create', methods=['GET', 'POST'])
    @login_required
    def create_post():
        form = PostForm()
        if form.validate_on_submit():
            category_id = form.category.data if form.category.data != 0 else None
            post = Post(
                title=form.title.data,
                content=form.content.data,
                author=current_user,
                category_id=category_id,
                allow_comments=form.allow_comments.data
            )
            db.session.add(post)
            db.session.commit()
            flash('Yazınız başarıyla yayınlandı!', 'success')
            return redirect(url_for('post_detail', post_id=post.id))
        
        return render_template('create_post.html', title='Yeni Yazı', form=form)
    
    # ==================== YAZI DETAY ====================
    @app.route('/post/<int:post_id>')
    def post_detail(post_id):
        post = Post.query.get_or_404(post_id)
        form = CommentForm()
        comments = post.comments.order_by(Comment.date_posted.desc()).all()
        return render_template('post.html', title=post.title, post=post, 
                             form=form, comments=comments)
    
    # ==================== YAZI DÜZENLE ====================
    @app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_post(post_id):
        post = Post.query.get_or_404(post_id)
        
        if post.author != current_user:
            abort(403)
        
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            post.category_id = form.category.data if form.category.data != 0 else None
            post.allow_comments = form.allow_comments.data
            db.session.commit()
            flash('Yazınız başarıyla güncellendi!', 'success')
            return redirect(url_for('post_detail', post_id=post.id))
        
        elif request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content
            form.category.data = post.category_id or 0
            form.allow_comments.data = post.allow_comments
        
        return render_template('edit_post.html', title='Yazıyı Düzenle', form=form, post=post)
    
    # ==================== YAZI SİL ====================
    @app.route('/post/<int:post_id>/delete', methods=['POST'])
    @login_required
    def delete_post(post_id):
        post = Post.query.get_or_404(post_id)
        
        if post.author != current_user:
            abort(403)
        
        db.session.delete(post)
        db.session.commit()
        flash('Yazınız silindi.', 'info')
        return redirect(url_for('index'))
    
    # ==================== YORUM EKLE ====================
    @app.route('/post/<int:post_id>/comment', methods=['POST'])
    @login_required
    def add_comment(post_id):
        post = Post.query.get_or_404(post_id)
        
        if not post.allow_comments:
            flash('Bu yazıya yorum yapılamaz.', 'warning')
            return redirect(url_for('post_detail', post_id=post.id))
        
        form = CommentForm()
        if form.validate_on_submit():
            comment = Comment(
                body=form.body.data,
                author=current_user,
                post=post
            )
            db.session.add(comment)
            db.session.commit()
            flash('Yorumunuz eklendi!', 'success')
        
        return redirect(url_for('post_detail', post_id=post.id))
    
    # ==================== YORUM SİL ====================
    @app.route('/comment/<int:comment_id>/delete', methods=['POST'])
    @login_required
    def delete_comment(comment_id):
        comment = Comment.query.get_or_404(comment_id)
        
        if comment.author != current_user and comment.post.author != current_user:
            abort(403)
        
        post_id = comment.post_id
        db.session.delete(comment)
        db.session.commit()
        flash('Yorum silindi.', 'info')
        return redirect(url_for('post_detail', post_id=post_id))
    
    # ==================== BEĞENİ ====================
    @app.route('/post/<int:post_id>/like', methods=['POST'])
    @login_required
    def like_post(post_id):
        post = Post.query.get_or_404(post_id)
        
        existing_like = PostLike.query.filter_by(
            user_id=current_user.id, post_id=post.id
        ).first()
        
        if existing_like:
            db.session.delete(existing_like)
            db.session.commit()
            liked = False
        else:
            like = PostLike(user_id=current_user.id, post_id=post.id)
            db.session.add(like)
            db.session.commit()
            liked = True
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'liked': liked, 'like_count': post.like_count})
        
        return redirect(url_for('post_detail', post_id=post.id))
    
    # ==================== ARAMA ====================
    @app.route('/search')
    def search():
        query = request.args.get('query', '')
        page = request.args.get('page', 1, type=int)
        
        if not query:
            return redirect(url_for('index'))
        
        posts = Post.query.filter(
            db.or_(
                Post.title.ilike(f'%{query}%'),
                Post.content.ilike(f'%{query}%')
            )
        ).order_by(Post.date_posted.desc()).paginate(
            page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False
        )
        
        categories = Category.query.order_by(Category.name).all()
        return render_template('search.html', title=f'Arama: {query}', 
                             posts=posts, query=query, categories=categories)
    
    # ==================== KULLANICI PROFİLİ ====================
    @app.route('/user/<username>')
    def user_profile(username):
        user = User.query.filter_by(username=username).first_or_404()
        page = request.args.get('page', 1, type=int)
        posts = user.posts.order_by(Post.date_posted.desc()).paginate(
            page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False
        )
        return render_template('profile.html', title=user.username, user=user, posts=posts)
    
    # ==================== HATA SAYFALARI ====================
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html', title='Sayfa Bulunamadı'), 404
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html', title='Erişim Engellendi'), 403
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html', title='Sunucu Hatası'), 500


# Uygulamaya route'ları kaydet
from flask import current_app
from app import create_app

# Bu fonksiyon __init__.py'den çağrılacak
def register_routes(app):
    init_app(app)
