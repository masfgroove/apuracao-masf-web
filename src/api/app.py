from flask import Flask, render_template, redirect, request, flash, session
from flask_mail import Mail, Message
import psycopg2
from config import email, senha

app = Flask(__name__)
app.secret_key = 'Ma@010246'
mail = Mail(app)

# Configuração do Flask-Mail
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'uesmcarnavalmaquete@gmail.com',
    "MAIL_PASSWORD": 'Ma@639639'
}
app.config.update(mail_settings)

# Dados de conexão PostgreSQL
conn_params = {
    'dbname': 'spring_react',
    'user': 'postgres',
    'password': 'yv5LNmQJ7P0Zu54N',
    'host': 'pleasingly-immense-whitethroat.data-1.use1.tembo.io',
    'port': '5432'
}

def get_db_connection():
    return psycopg2.connect(**conn_params)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT senha, nivel FROM login WHERE nome = %s', (nome,))
            user = cur.fetchone()
            cur.close()
            conn.close()

            if user and user[0] == senha:
                session['nome'] = nome
                session['nivel'] = user[1]
                flash('Login bem-sucedido!')
                return redirect('/video')
            else:
                flash('Nome ou senha incorretos.')
        except Exception as e:
            flash(f"Erro ao conectar ao banco de dados: {e}")
    
    return render_template('public/login.html')

@app.route('/logout')
def logout():
    session.pop('nome', None)
    session.pop('nivel', None)
    flash('Você foi desconectado.')
    return redirect('/')

@app.route('/')
def index():
    nome = session.get('nome')
    return render_template('public/index2.html', nome=nome)

@app.route('/video', methods=['GET'])
def video():
    nome = session.get('nome')
    nivel = session.get('nivel')
    selected_title = request.args.get('title')
    selected_year = request.args.get('year')

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = "SELECT * FROM videos "
        params = []

        if selected_title:
            query += " where title = %s"
            params.append(selected_title)

        if selected_year:
            query += " where ano = %s"
            params.append(selected_year)

        query += " ORDER BY ano DESC LIMIT 6;"
        
        cur.execute(query, tuple(params))
        videos = cur.fetchall()
        cur.close()

        cur = conn.cursor()
        cur.execute("SELECT DISTINCT title FROM videos;")
        titles = [row[0] for row in cur.fetchall()]
        cur.close()

        cur = conn.cursor()
        cur.execute("SELECT DISTINCT ano FROM videos ORDER BY ano DESC;")
        years = [row[0] for row in cur.fetchall()]
        cur.close()

        conn.close()
    except Exception as e:
        flash(f"Erro ao conectar ao banco de dados: {e}")
        videos = []
        titles = []
        years = []

    return render_template('public/index2.html', videos=videos, titles=titles, selected_title=selected_title, selected_year=selected_year, years=years, nome=nome, nivel=nivel)

@app.route('/add_video', methods=['POST'])
def add_video():
    title = request.form.get('title')
    description = request.form.get('description')
    url = request.form.get('url')
    img = request.form.get('img')
    ano = request.form.get('ano')
    tipo = request.form.get('tipo')
    
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("INSERT INTO videos (title, description, url, img, ano, tipo) VALUES (%s, %s, %s, %s, %s, %s)", 
                        (title, description, url, img, ano, tipo))
            conn.commit()
        flash('Vídeo adicionado com sucesso!')
    except Exception as e:
        flash(f"Erro ao adicionar vídeo: {e}")
    finally:
        conn.close()

    return redirect('/video')

@app.route('/update_video', methods=['POST'])
def update_video():
    codigo = request.form.get('codigo')
    title = request.form.get('title')
    description = request.form.get('description')
    url = request.form.get('url')
    img = request.form.get('img', None)
    ano = request.form.get('ano', None)
    tipo = request.form.get('tipo', None)

    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE videos
                SET title = %s, description = %s, url = %s, img = %s, ano = %s, tipo = %s
                WHERE codigo = %s
            """, (title, description, url, img, ano, tipo, codigo))
            conn.commit()
        flash('Vídeo atualizado com sucesso!')
    except Exception as e:
        flash(f"Erro ao atualizar o vídeo: {e}")
    finally:
        conn.close()

    return redirect('/video')

@app.route('/delete_video', methods=['POST'])
def delete_video():
    codigo = request.form['codigo']
    
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM videos WHERE codigo = %s", (codigo,))
            conn.commit()
        flash('Vídeo excluído com sucesso!')
    except Exception as e:
        flash(f"Erro ao excluir o vídeo: {e}")
    finally:
        conn.close()
    
    return redirect('/video')

@app.route('/sobre')
def sobre():
    return render_template('/public/sobre.html')

@app.route('/projetos')
def projetos():
    return render_template('/public/projetos.html')

@app.route('/escolas')
def escolas():
    return render_template('/public/escolas.html')

@app.route('/escolas2')
def escolas2():
    return render_template('/public/escolas2.html')

@app.route('/java')
def java():
    return render_template('/public/java.html')

@app.route('/contato')
def contato():
    return render_template('/public/contato.html')

@app.route('/imagemp1')
def imagemp1():
    return render_template('/public/imagemp1.html')

@app.route('/cadastrar_post')
def cadastrar_post():
    nome = session.get('nome')
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT codigo,autor,created_at,data_publicacao,title,content,imagem FROM post order by codigo desc')
        posts = cur.fetchall()
        cur.close()

        cur = conn.cursor()
        cur.execute('SELECT  codigo,autor,created_at,data_publicacao,title,content,imagem FROM post order by codigo desc')
        recent_posts = cur.fetchall()
        cur.close()




        conn.close()
    except Exception as e:
        flash(f"Erro ao conectar ao banco de dados: {e}")
        posts = []
        recent_posts = []

    return render_template('public/add_post.html', posts=posts, recent_posts=recent_posts, nome=nome)

@app.route('/desfiles', methods=['GET'])
def desfiles():
    selected_option = request.args.get('sellist1')
    return render_template('/public/desfiles.html', selected_option=selected_option)

@app.route('/imagemp2')
def imagemp2():
    return render_template('/public/imagemp2.html')

@app.route('/posts', methods=['GET'])
def posts():
    nome = session.get('nome')
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT codigo, autor, created_at, data_publicacao, imagem, title, content FROM post order by codigo desc')
        posts = cur.fetchall()
        cur.close()

        cur = conn.cursor()
        cur.execute('SELECT codigo, title, created_at FROM post order by codigo desc')
        recent_posts = cur.fetchall()
        cur.close()

        conn.close()
    except Exception as e:
        flash(f"Erro ao conectar ao banco de dados: {e}")
        posts = []
        recent_posts = []

    return render_template('public/posts.html', posts=posts, recent_posts=recent_posts, nome=nome)

@app.route('/post/<int:codigo>', methods=['GET'])
def post_detail(codigo):
    nome = session.get('nome')
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM post WHERE codigo = %s', (codigo,))
        post = cur.fetchone()
        cur.close()

        cur = conn.cursor()
        cur.execute('SELECT codigo, title, created_at FROM post order by codigo desc')
        recent_posts = cur.fetchall()
        cur.close()

        conn.close()

        if post is None:
            flash('Post não encontrado.')
            return redirect('/posts')
    
    except Exception as e:
        flash(f"Erro ao conectar ao banco de dados: {e}")
        return redirect('/posts')

    return render_template('public/post_detail.html', post=post, recent_posts=recent_posts, nome=nome)

@app.route('/add_post', methods=['POST'])
def add_post():
    autor = request.form.get('autor')
    data_publicacao = request.form.get('data_publicacao')
    title = request.form.get('title')
    content = request.form.get('content')
    imagem = request.form.get('imagem', None)
    
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO public.post (autor, data_publicacao, title, content, imagem)
                VALUES (%s, %s, %s, %s, %s)
            """, (autor, data_publicacao, title, content, imagem))
            conn.commit()
        flash('Notícia cadastrada com sucesso!')
    except Exception as e:
        flash(f"Erro ao cadastrar notícia: {e}")
    finally:
        conn.close()

    return redirect('/posts')

@app.route('/manage_post', methods=['POST'])
def manage_post():
    codigo = request.form.get('codigo')
    title = request.form.get('title')
    autor = request.form.get('autor')
    content = request.form.get('content')
    imagem = request.form.get('imagem', None)
    data_publicacao = request.form.get('data_publicacao', None)
    action = request.form.get('action')
    
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            if action == 'add':
                cur.execute("""
                    INSERT INTO post (title, autor, content, imagem, data_publicacao, created_at)
                    VALUES (%s, %s, %s, %s, %s, NOW())
                """, (title, autor, content, imagem, data_publicacao))
                flash('Notícia cadastrada com sucesso!')
            elif action == 'update':
                cur.execute("""
                    UPDATE post
                    SET title = %s, autor = %s, content = %s, imagem = %s, data_publicacao = %s
                    WHERE codigo = %s
                """, (title, autor, content, imagem, data_publicacao, codigo))
                flash('Notícia atualizada com sucesso!')
            elif action == 'delete':
                cur.execute("DELETE FROM post WHERE codigo = %s", (codigo,))
                flash('Notícia excluída com sucesso!')
            else:
                flash('Ação não reconhecida.')
            conn.commit()
    except Exception as e:
        flash(f"Erro ao gerenciar a notícia: {e}")
    finally:
        conn.close()
    
    return redirect('/posts')


class Contato:
    @staticmethod
    def enviar_email(assunto, mensagem, destinatario):
        try:
            msg = Message(subject=assunto,
                          body=mensagem,
                          recipients=[destinatario],
                          sender=app.config.get("MAIL_USERNAME"))
            mail.send(msg)
            flash('E-mail enviado com sucesso!')
        except Exception as e:
            flash(f"Erro ao enviar e-mail: {e}")

if __name__ == '__main__':
    app.run(debug=True)
