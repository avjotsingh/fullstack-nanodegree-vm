from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

## set up the database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()

## Display all restaurants
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('ShowRestaurants.html', restaurants = restaurants)

## Return a JSON of all the restaurants
@app.route('/restaurants/JSON')
def restauransJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurants = [restaurant.serialize for restaurant in restaurants])

## Create a new restaurant
@app.route('/restaurant/new/', methods = ['GET', 'POST'])
def newRestaurant():
	if request.method == "POST":
		newRestaurant = Restaurant(name = request.form['restaurant_name'])
		session.add(newRestaurant)
		session.commit()
		flash("New Restaurant Created!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('NewRestaurant.html')

## Edit an existing restaurant
@app.route('/restaurant/<int:restaurant_id>/edit/', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == "POST":
		restaurant.name = request.form['restaurant_name']
		session.add(restaurant)
		session.commit()
		flash("Restaurant Successfully Edited!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('EditRestaurant.html', restaurant = restaurant)

## Delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete/', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == "POST":
		session.delete(restaurant)
		session.commit()
		flash("Restaurant Successfully Deleted!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('DeleteRestaurant.html', restaurant = restaurant)

## Show a restaurant menu
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return render_template('ShowMenu.html', restaurant = restaurant, menuItems = menuItems)

## Return a JSON of all the menu items of a particular restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def menuItemsJSON(restaurant_id):
	menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return jsonify(MenuItems = [item.serialize for item in menuItems])

## Return a JSON of a particular menu item of a particular restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).filter_by(id = menu_id).one()
	return jsonify(MenuItem = menuItem.serialize)

## Create a new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == "POST":
		newMenuItem = MenuItem(name = request.form['name'], description = request.form['description'], 
			course = request.form['course'], price = request.form['price'], restaurant = restaurant)
		session.add(newMenuItem)
		session.commit()
		flash("New Menu Item Created!")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('NewMenuItem.html', restaurant = restaurant)

## Edit an existing menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menuItem = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).filter_by(id = menu_id).one()
	if request.method == "POST":
		if request.form['name'] != "":
			menuItem.name = request.form['name']
		if request.form['description'] != "":
			menuItem.description = request.form['description']
		if request.form['course'] != "":
			menuItem.course = request.form['course']
		if request.form['price'] != "":
			menuItem.price = request.form['price']
		session.add(menuItem)
		session.commit()
		flash("Menu Item Successfully Edited!")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('EditMenuItem.html', restaurant = restaurant, menuItem = menuItem)	

## Delete an existing menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menuItem = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).filter_by(id = menu_id).one()
	if request.method == "POST":
		session.delete(menuItem)
		session.commit()
		flash("Menu Item Successfully Deleted!")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('DeleteMenuItem.html', restaurant = restaurant, menuItem = menuItem)

if __name__ == "__main__":
	app.secret_key = 'super_secrer_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)