from server import db

class Games(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String())
    categoria = db.Column(db.String())
    console = db.Column(db.String())

    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console
    
    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome, 
            'categoria': self.categoria,
            'console': self.console
        }