from flask import Flask, render_template, redirect, request, flash
from flask_mail import Mail, Message
from config import email, senha

app = Flask(__name__)
mail = Mail(app)
app.secret_key = 'Ma@010246'

mail_settings = {
    "MAIL_SERVER":'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": email,
    "MAIL_PASSWORD": senha
}

app.config.update(mail_settings)
mail = Mail(app)

class Contato:
    def __init__(self, nome, email, mensagem):
        self.nome = nome
        self.email = email
        self.mensagem = mensagem

@app.route('/')
def index():
    return render_template('/public/index.html')

@app.route('/sobre')
def sobre():
    return render_template('/public/sobre.html')

@app.route('/projetos')
def projetos():
    return render_template('/public/projetos.html')

@app.route('/java')
def java():
    return render_template('/public/java.html')


@app.route('/contato')
def contato():
    return render_template('/public/contato.html')

@app.route('/imagemp1')
def imagemp1():
    return render_template('/public/imagemp1.html')

@app.route('/imagemp2')
def imagemp2():
    return render_template('/public/imagemp2.html')


@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        formContato = Contato(
            request.form["nome"], 
            request.form["email"],
            request.form["mensagem"]
        )

        msg = Message(
            subject = f'{formContato.nome} te enviou uma mensagem no portfÃ³lio',
            sender = app.config.get("MAIL_USERNAME"),
            recipients = ['marcoantonio639639@gmail.com', app.config.get("MAIL_USERNAME")],
            body = f'''

            {formContato.nome} com o e-mail {formContato.email}, te enviou a seguinte mensagem:

            {formContato.mensagem}

            '''
        )
        mail.send(msg)
        flash('Mensagem enviada com sucesso!')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)