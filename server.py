
from flask import Flask, request, abort
from mock_data import catalog
import json
import random
from config import db


app = Flask(__name__)

me = {
    "name": "Brandon",
    "last": "Webster",
    "age": 28,
    "hobbies": [],
    "address":
        {

            "street": "Evergreen",
            "number": 30,
            "city": "San Diego"
    }
}


@app.route("/", methods=['GET'])
def home():
    return "Hello from Python"


@app.route("/test")
def any_name():
    return "I'm a test function."


@app.route("/about")
def about():
    return me["name"] + " " + me["last"]


@app.route("/api/catalog")
def get_catalog():
    cursor = db.products.find({})
    results = []
    for product in cursor:
        product["_id"] = str(prodcut["_id"])
        results.append(product)

    return json.dumps(catalog)


@app.route("/api/catalog", methods=["post"])
def save_product():
    product = request.get_json()
    print(product)

    if not 'title' in product or len(product["title"]) < 5:
        return abort(400, "Title is required, and should be at least 5 chars long")

    if not "price" in product:
        return abort(400, "Price is required")

    if not isinstance(product["price"], float) and not isinstance(product["price"], int):
        return abort(400, "Price should be a valid number")

    if product["price"] <= 0:
        return abort(400, "Price should be greater than zero")

    db.products.insert_one(product)

    print("----SAVED----")
    print(product)

    return json.dumps(product)


@app.route("/api/cheapest")
def get_cheapest():
    # find the cheapest product on the catalog list
    cursor = db.products.find({})
    cheap = catalog[0]
    for product in catalog:
        if product["price"] < cheap["price"]:
            cheap = product

    cheap["_id"] = str(cheap["_id"])
    # return it as json
    return json.dumps(cheap)


@app.route("/api/product/<id>")
def get_product(id):
    # validate id is valid ObjectId
    if(not ObjectId.is_valid(id)):
        return abort(400, "id is not a valid ObjectID")

    result = db.products.find_one({"_id": ObjectId(id)})
    if not result:
        return abort(404)  # 404 = not found
    result["_id"] = str(result["_id"])
    return json.dumps(result)


@app.route("/api/catalog/<category>")
def get_by_category(category):
    result = []
    cursor = db.products.find({"category": category})
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        result.append(prod)

    return json.dumps(result)

# /api/categories
# return list of unqiue items
@app.route("/api/categories")
def get_categories():
    result = []
    for product in catalog:
        cat = product["category"]
        if cat not in result:
            result.append(cat)

    return json.dumps(result)

# GET /api/reports/prodCount


@app.route("/api/reports/prodCount")
def get_prod_count():
    count = len(catalog)
    return json.dumps(count)


@app.route("/api/reports/total")
def get_total():
    total = 0

    # print the title of each product
    for prod in catalog:
        totalProd = prod["price"] * prod["stock"]
        total += totalProd

    return json.dumps(total)


# /api/reports/highestInvestment
@app.route("/api/reports/highestinvestment")
def get_highest_investment():
    highest = catalog[0]

    for prod in catalog:
        prod_invest = prod["price"] * prod["stock"]
        high_invest = highest["price"] * highest["stock"]

        if prod_invest > high_invest:
            highest = prod

    return json.dumps(highest)


# POST /api/couponCodes
@app.route("/api/couponCodes", methods=["POST"])
def save_coupon():
    couponCode = request.get_json()

    if not "code" in couponCode:
        return abort(400, "code is required")

    if not "discount" in couponCode:
        return abort(400, "discount is required")

    db.couponCodes.insert_one(couponCode)

    couponCode["_id"] = str(couponCode["_id"])
    return json.dumps(couponCode)


# Get /api/couponCodes/<code>
# retrieve specific couponCodes by its code
@app.route("/api/couponCodes/<code>")
def valid_coupon(code):
    print(code)

    # get from db
    coupon = db.couponCodes.find_one({"code": code})
    if not coupon:
        return abort(404)

    coupon["_id"] = str(coupon["_id"])

    return json.dumps(coupon)


# start the server
app.run(debug=True)
