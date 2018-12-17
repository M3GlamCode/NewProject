from biashara import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):		
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(25), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	businesses = db.relationship('Business', backref="posted_by", lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.password}')"

class Business(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	business_name = db.Column(db.String(10), nullable=False)
	business_category = db.Column(db.String(10))
	business_email = db.Column(db.String(120), nullable=False)
	description = db.Column(db.Text(200), nullable=False)
	address = db.Column(db.String(60), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Business('{self.business_name}', '{self.business_category}', '{self.business_email}', '{self.description}', '{self.address}')"
		
class Reviews(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	reviewer = db.Column(db.String(10), nullable=False)
	reviews = db.Column(db.Text(200), nullable=False)
	business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)


	def __repr__(self):
		return f"Reviews('{self.reviewer}, {self.reviews}')"
		