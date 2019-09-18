from server import db

class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img = db.Column(db.String())
    descricao = db.Column(db.String())
    valor = db.Column(db.Numeric(10,2))

    def __init__(self, img, descricao, valor):
        self.img = img
        self.descricao = descricao
        self.valor = valor