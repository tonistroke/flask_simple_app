from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Diccionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(200), nullable=False)
    meaning = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Word %r>' % self.id



def index():
  return "Hello World"

if __name__ == "__main__":
  app.run(debug = True)

#AddWord---------------------------------------------------------------------


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        n_word = request.form['word']
        new_word = Diccionario(meaning = n_word)
        n_meaning = request.form['meaning']
        new_meaning = Diccionario(meaning = n_meaning)

        try:
          db.session.add(new_word)
          db.session.add(new_meaning)
          db.session.commit()
            return redirect('/')
        except:
          return "A ocurrido un error al intentar añadir la palabra"

    else:
      words = Diccionario.query.order_by(Diccionario.id).all()
        return render_template('index.html', words=words)



#DeleteWord------------------------------------------------------------------

@app.route('/delete/<int:id>')
def delete(id):
    word_to_delete = Diccionario.query.get_or_404(id)

    try:
        db.session.delete(word_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "A ocurrido un error al intentar eliminar la palabra"


#updatewordndMeaning---------------------------------------------------------

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    word = Diccionario.query.get_or_404(id)

    if request.method == 'POST':
        word.word = request.form['word']
        word.meaning = request.form['meaning']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "A ocurrido un error al intentar actualizar la palabra"

    else:
        return render_template('update.html', word=word)


if __name__ == "__main__":
    app.run(debug=True)
