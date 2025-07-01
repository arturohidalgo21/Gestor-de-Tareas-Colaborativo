# ========== app.py ==========

from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Board, List, Card, Comment

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-segura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Ruta /login llamada")  # <-- línea para debug
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Usuario o contraseña incorrectos")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User(username=request.form['username'], password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    boards = Board.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', boards=boards, user=current_user)

@app.route('/board/create', methods=['POST'])
@login_required
def create_board():
    board_name = request.form['board_name']
    new_board = Board(name=board_name, user_id=current_user.id)
    db.session.add(new_board)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/board/<int:board_id>')
@login_required
def view_board(board_id):
    board = Board.query.get_or_404(board_id)
    if board.owner != current_user:
        flash("No tienes permiso para ver este tablero.")
        return redirect(url_for('dashboard'))
    all_users = User.query.all()
    return render_template('board.html', board=board, all_users=all_users)

@app.route('/board/<int:board_id>/add_list', methods=['POST'])
@login_required
def add_list(board_id):
    board = Board.query.get_or_404(board_id)
    if board.owner != current_user:
        flash("No tienes permiso.")
        return redirect(url_for('dashboard'))
    list_name = request.form['list_name']
    new_list = List(name=list_name, board_id=board_id)
    db.session.add(new_list)
    db.session.commit()
    return redirect(url_for('view_board', board_id=board_id))

@app.route('/list/<int:list_id>/add_card', methods=['POST'])
@login_required
def add_card(list_id):
    lista = List.query.get_or_404(list_id)
    board = lista.board
    if board.owner != current_user:
        flash("No tienes permiso.")
        return redirect(url_for('dashboard'))

    title = request.form['title']
    description = request.form['description']
    assigned_to = request.form.get('assigned_to') or None

    new_card = Card(
        title=title,
        description=description,
        list_id=list_id,
        assigned_to=int(assigned_to) if assigned_to else None
    )
    db.session.add(new_card)
    db.session.commit()
    return redirect(url_for('view_board', board_id=board.id))

@app.route('/card/<int:card_id>/move', methods=['POST'])
@login_required
def move_card(card_id):
    card = Card.query.get_or_404(card_id)
    board = card.list.board
    if board.owner != current_user:
        return jsonify({'error': 'No autorizado'}), 403

    data = request.get_json()
    new_list_id = data.get('new_list_id')
    new_list = List.query.get_or_404(new_list_id)
    if new_list.board_id != board.id:
        return jsonify({'error': 'Lista no válida'}), 400

    card.list_id = new_list_id
    db.session.commit()
    return jsonify({'success': True})

@app.route('/card/<int:card_id>/comment', methods=['POST'])
@login_required
def add_comment(card_id):
    card = Card.query.get_or_404(card_id)
    board = card.list.board
    if board.owner != current_user:
        flash("No tienes permiso.")
        return redirect(url_for('dashboard'))

    content = request.form['content']
    comment = Comment(content=content, card_id=card.id, user_id=current_user.id)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('view_board', board_id=board.id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
