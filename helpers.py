import csv
import urllib.request
import datetime
import json

from bs4 import BeautifulSoup
from flask import redirect, render_template, request, session, Flask, jsonify
from functools import wraps
from bs4 import BeautifulSoup

# app_id=8cd06460

# app_key = ebddcccc0ab9562d35ad429dc63d6e0b

def errormsg(message, code=400):
    """Renders message as an errormsg to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("errormsg.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(ingredients):
    """Look up recipes with ingredients."""

    try:

        # GET CSV
        url = f"https://api.edamam.com/search?q={ingredients}&app_id=8cd06460&app_key=ebddcccc0ab9562d35ad429dc63d6e0b"
        webpage = urllib.request.urlopen(url)

        # Parse CSV
        datareader = csv.reader(webpage.read().decode("utf-8").splitlines())

        # Ignore first row
        hits = json.loads(datareader)

        # Parse second row
        row = next(datareader)

        # Ensure stock exists
        try:
            price = float(row[4])
        except:
            return None

        # Return stock's name (as a str), price (as a float), and (uppercased) ingredients (as a str)
        return {
            "name": ingredients.upper(), # for backward compatibility with Yahoo
            "price": price,
            "ingredients": ingredients.upper()
        }

    except:
        return None

def scraper(mealtime):
    """Retrieve meal info from HUDS website"""

    # Query HUDS for table
    # try:

    #     # Retrieve HTML
    #     url = f"http://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?date=11-28-2017&type=05&meal=2"
    #     webpage = urrlib.request.urlopen(url)
    #     response = requests.get(url)
    #     html = response.content

    #     soup = BeautifulSoup(html)
    #     print (soup.prettify())

    # import libraries

    now = datetime.datetime.now()

    # specify the url
    url = f"http://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?date={now.month}-{now.day}-{now.year}&type=30&meal={mealtime}"
    print (url)

    # if int(mealtime) == 1:
    #     # specify the url
    #     url = 'http://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?date={now.month}-{now.day}-{now.year}&type=30&meal=1'

    # if int(mealtime) == 2:
    #     # specify the url
    #     url = 'http://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?date={now.month}-{now.day}-{now.year}&type=30&meal=2'
    print (mealtime)

    # query the website and return the html to the variable 'page'
    page = urllib.request.urlopen(url)

    # parse the html using beautiful soap and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')

    # Take out the <div> of name and get its value
    #name_box = soup.find('td', attrs={'class':'menu_item'})


    #name = name_box.text.strip() # strip() is used to remove starting and trailing

    #print name

    name_box = soup.find_all('tr')
    menu = []
    for tds in name_box[3:]:
    	menu_html = tds.find('a')
    	try:
    		menu_item = menu_html.text.strip()
    # 		print (menu_item)
    		menu.append(menu_item)
    	except AttributeError:
    		pass
    	except TypeError:
    		pass
    return menu