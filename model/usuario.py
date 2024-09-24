from sql_alchemy import banco

class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(80), nullable=False)
    nivel = banco.Column(banco.Integer, nullable=False)
    ativado = banco.Column(banco.String(1), default='N')

    def __init__(self, login, senha, email, nivel, ativado):
        self.login = login
        self.senha = senha
        self.email = email
        self.nivel = nivel
        self.ativado = ativado

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'email': self.email,
            'nivel': self.nivel,
            'ativado': self.ativado
            }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    @classmethod
    def delete_by_id(cls, user_id):
        try:
            user = cls.find_user(user_id)  
            if user:
                banco.session.delete(user)  
                banco.session.commit()  
                return True  
            return False  
        except Exception as e:
            banco.session.rollback()  
            print(f"Erro ao deletar o usuário: {e}")
            return False

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
        
    


