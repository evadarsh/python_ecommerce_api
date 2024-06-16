from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Path to your product data .json file
data_file = "products.json"


def load_data():
  "Loads product data from JSON file"
  try:
    with open(data_file, "r", encoding="utf-8") as f:
      return json.load(f)
  except FileNotFoundError:
    return []



def save_data(data):
  "Saves product data to JSON file"
  with open(data_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)


@app.route("/api/products", methods=["GET"])
def get_all_products():
  "Gets all products"
  products = load_data()
  return jsonify(products)


@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id):
  "Gets a product by its ID"
  products = load_data()
  for product in products:
    if product["id"] == product_id:
      return jsonify(product)
  return jsonify({"message": "Product not found"}), 404


@app.route("/api/products", methods=["POST"])
def create_product():
  "Creates a new product"
  products = load_data()
  new_product = request.get_json()

  if not new_product or not new_product.get("name") or not new_product.get("price"):
    return jsonify({"message": "Missing required fields"}), 400

  new_id = 1
  if products:
    new_id = max(product["id"] for product in products) + 1

  new_product["id"] = new_id
  products.append(new_product)
  save_data(products)
  return jsonify(new_product), 201


@app.route("/api/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
  "Updates a product by its ID"
  products = load_data()
  updated_product = request.get_json()

  found = False
  for i, product in enumerate(products):
    if product["id"] == product_id:
      found = True
      products[i] = updated_product
      break

  if not found:
    return jsonify({"message": "Product not found"}), 404

  save_data(products)
  return jsonify(updated_product)


@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
  "Deletes a product by its ID"
  products = load_data()

  found = False
  for i, product in enumerate(products):
    if product["id"] == product_id:
      found = True
      del products[i]
      break

  if not found:
    return jsonify({"message": "Product not found"}), 404

  save_data(products)
  return jsonify({"message": "Product deleted"})


if __name__ == "__main__":
  app.run(debug=True)
