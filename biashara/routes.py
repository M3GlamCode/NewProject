from biashara import app, db, bcrypt
from flask import render_template, flash, redirect, url_for, request
from biashara.forms import RegistrationForm, LoginForm, BusinessRegistration, SearchForm, UpdateProfileForm, UpdateBusinessForm, ReviewForm
from biashara.models import User, Business, Reviews
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
@app.route('/home', methods=['POST', 'GET'])
def home():
	businesses = Business.query.all()
	form = SearchForm()
	if form.validate_on_submit():
		myquery = form.search.data
		businesses = Business.query.filter_by(business_category=myquery).all()
		if not businesses:
			form = SearchForm()
			return render_template('nullsearches.html', form=form)
	return render_template('home.html', title="Home", businesses=businesses, form=form)

@app.route('/add', methods=['POST', 'GET'])
@login_required
def add():
	form = BusinessRegistration()
	if form.validate_on_submit():
		business = Business(business_name=form.business_name.data, business_category=form.business_category.data, 
							business_email=form.business_email.data, description=form.description.data, 
							address=form.address.data, reviewer=current_user)
		db.session.add(business)
		db.session.commit()
		flash('Business registered', 'success')
		return redirect(url_for('home'))
	return render_template('add.html', title="Add Business", form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		#generating a hashed password and storing the data filled in the form to the db
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Account created successfully! You can now login', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title="Register", form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()	
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user)
			#after login_required is user
			next_page = request.args.get('next')
			flash('You are now logged in!', 'success')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Çheck your email and password!', 'danger')
	return render_template('login.html', title="Login", form=form)

@app.route('/profile', methods=['POST', 'GET'])
def profile():
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	#business = Business.query.get_or_404(business_id)
	form = UpdateProfileForm()
	#displaying posts by the current user only
	#user = User.query.get_or_404(current_user.id)
	businesses = current_user.businesses
	if form.validate_on_submit():
		if form.username.data == current_user.username and form.email.data == current_user.email:
			pass
		else:
			current_user.username = form.username.data
			current_user.email = form.email.data
			db.session.commit()
			flash('Your account has been updated', 'success')
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	return render_template('profile.html', title="Profile", image_file=image_file, 
							businesses=businesses, form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route('/profile/<int:business_id>/update', methods=['POST', 'GET'])
def edit_business(business_id):
	business = Business.query.get_or_404(business_id)
	businessform = UpdateBusinessForm()
	if businessform.validate_on_submit():
		business.business_name = businessform.business_name.data
		business.business_category = businessform.business_category.data
		business.business_email = businessform.business_email.data
		business.description = businessform.description.data
		business.address = businessform.address.data
		db.session.commit()
		flash('Business updated', 'success')
		return redirect(url_for('profile'))
	elif request.method == 'GET':
		businessform.business_name.data = business.business_name
		businessform.business_category.data = business.business_category
		businessform.business_email.data = business.business_email
		businessform.description.data = business.description
		businessform.address.data = business.address
	return render_template('editbusiness.html', business=business, businessform=businessform)

@app.route('/profile/<int:business_id>/delete', methods=['POST', 'GET'])
def delete_business(business_id):
	business = Business.query.get_or_404(business_id)
	db.session.delete(business)
	db.session.commit()
	flash('Business deleted!', 'success')
	return redirect(url_for('profile'))

@app.route('/reviews/<int:business_id>', methods=['GET'])
def read_reviews(business_id):
	business = Business.query.get_or_404(business_id)
	form = ReviewForm()
	reviews = Reviews.query.filter_by(business_id=business_id).all()
	return render_template('reviews.html', business=business, reviews=reviews, form=form)

@app.route('/reviews/<int:business_id>/write', methods=['POST', 'GET'])
def write_review(business_id):
	form = ReviewForm()
	business = Business.query.filter_by(id=business_id).first_or_404()

	if form.validate_on_submit():
		review = Reviews(reviews=form.business_review.data, business_id=business.id, user_id=current_user.id)
		db.session.add(review)
		db.session.commit()
		flash('successfully posted review!', 'success')
		return redirect(url_for('read_reviews', business_id=business_id))
	return render_template('writereview.html', business=business, form=form)