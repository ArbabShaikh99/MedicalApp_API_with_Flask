import os
from datetime import timedelta

from flask import Flask, jsonify, request, Response
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
from werkzeug.utils import secure_filename

from Medical_DataBase.uploadImg.db import db_init, db
from Medical_DataBase.uploadImg.models import Img

from Medical_DataBase.User_DB.CreateUserTable import createTables
from Medical_DataBase.User_DB.UserAddOperation import createUser
from Medical_DataBase.User_DB.ReadUserOperation import getAllUsers, getSpecificUser
from Medical_DataBase.User_DB.auth import user_auth
from Medical_DataBase.User_DB.UpdateOperation import updateUserName, upDate_User_All_Fields
from Medical_DataBase.User_DB.DeleteUserOperation import DeleteUser

from Medical_DataBase.Banner_DB.CreateBannerTable import createBannerTable
from Medical_DataBase.Banner_DB.ReadBannerOperation import getAllBanners
from Medical_DataBase.Banner_DB.AddBannerOperation import addBanner
from Medical_DataBase.Product_DB.CreateProductTable import CreateProductTable
from Medical_DataBase.Product_DB.ReadProductOperation import getAllProducts, getSpecifiProduct, searchProducts
from Medical_DataBase.Product_DB.ProductAddOperation import addProductOperation
from Medical_DataBase.Product_DB.DeleteProductOperation import deleteProduct
from Medical_DataBase.Product_DB.UpDateProductOperation import updateProductAllFields

from Medical_DataBase.Order_DB.CreateOrderTable import CreateOrderTable
from Medical_DataBase.Order_DB.ReadOrderOperation import getAllOrder, getAllOrderThroughUser, getSpecificOrder
from Medical_DataBase.Order_DB.OrderAddOperation import addOrderOperation
from Medical_DataBase.Order_DB.UpdateOrderOperation import updateOrderAllFields
from Medical_DataBase.Order_DB.DeleteOrderOperation import deleteOrder

from Medical_DataBase.UserStock_DB.AddUserStockOperation import addStockOperation
from Medical_DataBase.UserStock_DB.CreateUserStockTable import createStockTable
from Medical_DataBase.UserStock_DB.DeleteUserStckOperation import deleteStock
from Medical_DataBase.UserStock_DB.ReadUserStockOperation import getAllStockItem
from Medical_DataBase.UserStock_DB.UpdateUserStockOperation import updateStockAllFields

from Medical_DataBase.history_db.createHistoryTable import createHistoryTable
from Medical_DataBase.history_db.addHistoryOperation import addSellHistoryOperation
from Medical_DataBase.history_db.readHistoryOperation import getAllSellHistoryItem, getSpecificSellHistoryItem
from Medical_DataBase.history_db.deleteSellHistoryOperation import deleteSellHistroyItem
from Medical_DataBase.history_db.updateSalteHistoryOperation import updateSellHistoryItemFields

# ─────────────────────────────────────────────────────────────
# App setup
# ─────────────────────────────────────────────────────────────

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'medical-app-dev-secret-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
jwt = JWTManager(app)


# ─────────────────────────────────────────────────────────────
# Helper — parse JSON body safely
# ─────────────────────────────────────────────────────────────

def get_json():
    return request.get_json(force=True, silent=True) or {}


# ─────────────────────────────────────────────────────────────
# Health check
# ─────────────────────────────────────────────────────────────

@app.route('/')
def home():
    return jsonify({"status": 200, "message": "Medical App API is running"})


# ─────────────────────────────────────────────────────────────
# Image
# ─────────────────────────────────────────────────────────────

@app.route('/getImg/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return jsonify({"status": 404, "message": "Image not found"}), 404
    return Response(img.img, mimetype=img.mimetype)


# ─────────────────────────────────────────────────────────────
# User Routes
# ─────────────────────────────────────────────────────────────

@app.route('/signUp', methods=['POST'])
def signup():
    try:
        data = get_json()
        name     = data.get('name', '').strip()
        password = data.get('password', '')
        email    = data.get('email', '').strip().lower()
        phone    = data.get('phone', '').strip()
        address  = data.get('address', '').strip()
        pin_code = data.get('pinCode', '').strip()

        if not all([name, password, email, phone, address, pin_code]):
            return jsonify({"status": 400, "message": "All fields are required"})

        if len(password) < 6:
            return jsonify({"status": 400, "message": "Password must be at least 6 characters"})

        user_id = createUser(
            name=name, password=password, email=email,
            phone_Number=phone, address=address, pinCode=pin_code
        )

        if not user_id:
            return jsonify({"status": 400, "message": "Failed to create account"})

        # Auto-login: return token immediately so the app doesn't need a second /Login call
        token = create_access_token(identity=user_id)
        user_dict = {
            "user_id": user_id,
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "pin_code": pin_code,
            "is_approved": 0,
            "is_blocked": False,
            "level": 1,
            "created_at": str(__import__('datetime').date.today())
        }
        return jsonify({
            "status": 200,
            "message": "Account created successfully",
            "token": token,
            "user": user_dict
        })

    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


@app.route('/Login', methods=['POST'])
def login():
    try:
        data     = get_json()
        email    = data.get('email', '').strip().lower()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({"status": 400, "message": "Email and password are required"})

        user_dict = user_auth(email=email, password=password)

        if user_dict is None:
            return jsonify({"status": 400, "message": "Invalid email or password"})

        token = create_access_token(identity=user_dict['user_id'])

        return jsonify({
            "status": 200,
            "message": "Login successful",
            "token": token,
            "user": user_dict
        })

    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


@app.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    return getSpecificUser(userID=user_id)


@app.route('/getSpecificUser', methods=['POST'])
@jwt_required()
def get_specific_user():
    try:
        current_user_id = get_jwt_identity()
        data = get_json()
        requested_id = data.get('userID', current_user_id)
        return getSpecificUser(userID=requested_id)
    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


@app.route('/getAllUsers', methods=['GET'])
@jwt_required()
def get_all_users():
    return getAllUsers()


@app.route('/UpDateUserDetails', methods=['PATCH'])
@jwt_required()
def update_user_details():
    try:
        current_user_id = get_jwt_identity()
        data = get_json()

        allowed_fields = {'name', 'email', 'phone', 'address', 'isApproved', 'block', 'level'}
        update_fields = {k: v for k, v in data.items() if k in allowed_fields}

        if not update_fields:
            return jsonify({"status": 400, "message": "No valid fields to update"})

        upDate_User_All_Fields(userID=current_user_id, **update_fields)
        return jsonify({"status": 200, "message": "User updated successfully"})

    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


@app.route('/updateUserName', methods=['PATCH'])
@jwt_required()
def update_user_name():
    try:
        current_user_id = get_jwt_identity()
        data = get_json()
        new_name = data.get('name', '').strip()

        if not new_name:
            return jsonify({"status": 400, "message": "Name is required"})

        is_updated = updateUserName(userId=current_user_id, name=new_name)
        if is_updated:
            return jsonify({"status": 200, "message": "Name updated successfully"})
        else:
            return jsonify({"status": 400, "message": "Update failed"})

    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


@app.route('/DeleteUser', methods=['DELETE'])
@jwt_required()
def delete_user():
    try:
        current_user_id = get_jwt_identity()
        is_deleted = DeleteUser(UserID=current_user_id)

        if is_deleted:
            return jsonify({"status": 200, "message": "Account deleted successfully"})
        else:
            return jsonify({"status": 400, "message": "Delete failed"})

    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


# ─────────────────────────────────────────────────────────────
# App Config (public — no auth required)
# ─────────────────────────────────────────────────────────────

@app.route('/getConfig', methods=['GET'])
def get_config():
    return jsonify({
        "status": 200,
        "delivery_charge": 250,
        "store_pickup_charge": 0
    })

# ─────────────────────────────────────────────────────────────
# Product Routes (read is public, write is protected)
# ─────────────────────────────────────────────────────────────

@app.route('/getBanners', methods=['GET'])
def get_banners():
    return getAllBanners()


@app.route('/addBanner', methods=['POST'])
@jwt_required()
def add_banner():
    try:
        data = get_json()
        title         = data.get('title', '').strip()
        subtitle      = data.get('subtitle', '').strip()
        image_id      = data.get('image_id')
        color_hex     = data.get('color_hex', '#1B6CA8').strip()
        display_order = data.get('display_order', 0)

        if not all([title, subtitle, image_id]):
            return jsonify({"status": 400, "message": "title, subtitle and image_id are required"})

        banner_id = addBanner(title, subtitle, image_id, color_hex, display_order)
        if banner_id:
            return jsonify({"status": 200, "message": "Banner added", "banner_id": banner_id})
        return jsonify({"status": 400, "message": "Failed to add banner"})
    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


@app.route('/getProduct', methods=['GET'])
def get_products():
    return getAllProducts()


@app.route('/searchProduct', methods=['GET'])
def search_product():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])
    return searchProducts(query)


@app.route('/getSpecificProduct', methods=['POST'])
def get_specific_product():
    try:
        data = get_json()
        product_id = data.get('ProductID', '')
        if not product_id:
            return jsonify({"status": 400, "message": "ProductID is required"})
        return getSpecifiProduct(ProductID=product_id)
    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


@app.route('/addProduct', methods=['POST'])
@jwt_required()
def add_product():
    try:
        name        = request.form.get('product_name', '')
        category    = request.form.get('product_category', '')
        price       = request.form.get('product_price', '')
        stock       = request.form.get('product_stock', '')
        expiry_date = request.form.get('product_expiry_date', '')
        rating      = request.form.get('product_rating', '')
        description = request.form.get('product_description', '')
        power       = request.form.get('product_power', '')

        if not all([name, category, price, stock, expiry_date, rating, description, power]):
            return jsonify({"status": 400, "message": "All product fields are required"})

        pic = request.files.get('pic')
        if not pic:
            return jsonify({"status": 400, "message": "Product image is required"})

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return jsonify({"status": 400, "message": "Invalid image file"})

        img = Img(img=pic.read(), name=filename, mimetype=mimetype)
        db.session.add(img)
        db.session.commit()

        product_id = addProductOperation(
            name=name, category=category, price=price, stock=stock,
            expiry_date=expiry_date, rating=rating, description=description,
            image=img.id, power=power
        )

        if product_id:
            return jsonify({"status": 200, "message": "Product added successfully", "product_id": product_id})
        else:
            return jsonify({"status": 400, "message": "Failed to add product"})

    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


@app.route('/deleteProduct', methods=['DELETE'])
@jwt_required()
def delete_product():
    try:
        data = get_json()
        product_id = data.get('ProductID', '')
        if not product_id:
            return jsonify({"status": 400, "message": "ProductID is required"})

        is_deleted = deleteProduct(productId=product_id)
        if is_deleted:
            return jsonify({"status": 200, "message": "Product deleted successfully"})
        else:
            return jsonify({"status": 400, "message": "Product not found"})

    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


@app.route('/updateProducts', methods=['PATCH'])
@jwt_required()
def update_product():
    try:
        data = get_json()
        product_id = data.get('ProductID', '')
        if not product_id:
            return jsonify({"status": 400, "message": "ProductID is required"})

        allowed_fields = {
            'product_name', 'product_category', 'product_price',
            'product_stock', 'product_expiry_date', 'product_rating',
            'product_description', 'product_power'
        }
        update_fields = {k: v for k, v in data.items() if k in allowed_fields}

        if not update_fields:
            return jsonify({"status": 400, "message": "No valid fields to update"})

        updateProductAllFields(productId=product_id, **update_fields)
        return jsonify({"status": 200, "message": "Product updated successfully"})

    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


# ─────────────────────────────────────────────────────────────
# Order Routes
# ─────────────────────────────────────────────────────────────

@app.route('/order', methods=['POST'])
@jwt_required()
def create_order():
    try:
        data = get_json()
        current_user_id = get_jwt_identity()

        required = [
            'product_id', 'product_name', 'product_category', 'product_image_id',
            'user_name', 'product_quantity', 'product_price', 'subtotal_price',
            'delivery_charge', 'tax_charge', 'total_price', 'order_date',
            'user_address', 'user_pincode', 'user_mobile', 'user_email', 'order_status'
        ]
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({"status": 400, "message": f"Missing fields: {', '.join(missing)}"})

        order_id = addOrderOperation(
            user_id=current_user_id,
            product_id=data.get('product_id'),
            product_name=data.get('product_name'),
            user_name=data.get('user_name'),
            isApproved=data.get('isApproved', 0),
            product_quantity=data.get('product_quantity'),
            product_price=data.get('product_price'),
            totalPrice=data.get('total_price'),
            orderDate=data.get('order_date'),
            product_category=data.get('product_category'),
            product_image_id=data.get('product_image_id'),
            subtotal_price=data.get('subtotal_price'),
            tax_charge=data.get('tax_charge'),
            delivery_charge=data.get('delivery_charge'),
            user_email=data.get('user_email'),
            user_address=data.get('user_address'),
            user_mobile=data.get('user_mobile'),
            user_pinCode=data.get('user_pincode'),
            order_status=data.get('order_status'),
            order_cancel_status=data.get('order_cancel_status', 'no'),
            user_street=data.get('user_street', ''),
            user_city=data.get('user_city', ''),
            user_state=data.get('user_state', ''),
            discountPrice=data.get('discount_price', 0),
            shipped_date=data.get('shipped_date', ''),
            out_of_delivery_date=data.get('out_of_delivery_date', ''),
            delivered_date=data.get('delivered_date', '')
        )

        if order_id:
            return jsonify({"status": 200, "message": "Order placed successfully"})
        else:
            return jsonify({"status": 400, "message": "Failed to place order"})

    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


@app.route('/getAllOrders', methods=['GET'])
@jwt_required()
def get_all_orders():
    return getAllOrder()


@app.route('/getAllOrderThroughUser', methods=['GET'])
@jwt_required()
def get_orders_for_user():
    try:
        user_id = get_jwt_identity()
        return getAllOrderThroughUser(user_id=user_id)
    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


@app.route('/getSpecificOrder', methods=['POST'])
@jwt_required()
def get_specific_order():
    try:
        data = get_json()
        order_id = data.get('order_id', '')
        if not order_id:
            return jsonify({"status": 400, "message": "order_id is required"})
        return getSpecificOrder(orderId=order_id)
    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


@app.route('/updateOrder', methods=['PATCH'])
@jwt_required()
def update_order():
    try:
        data = get_json()
        order_id = data.get('orderId', '')
        if not order_id:
            return jsonify({"status": 400, "message": "orderId is required"})

        update_fields = {k: v for k, v in data.items() if k != 'orderId'}

        is_updated = updateOrderAllFields(order_id, **update_fields)
        if is_updated:
            return jsonify({"status": 200, "message": "Order updated successfully"})
        else:
            return jsonify({"status": 400, "message": "Order not found"})

    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


@app.route('/deleteOrder', methods=['DELETE'])
@jwt_required()
def delete_order():
    try:
        data = get_json()
        order_id = data.get('order_id', '')
        if not order_id:
            return jsonify({"status": 400, "message": "order_id is required"})

        is_deleted = deleteOrder(orderId=order_id)
        if is_deleted:
            return jsonify({"status": 200, "message": "Order deleted successfully"})
        else:
            return jsonify({"status": 400, "message": "Order not found"})

    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


@app.route('/cancelOrder', methods=['PATCH'])
@jwt_required()
def cancel_order():
    try:
        data = get_json()
        order_id = data.get('order_id', '')
        if not order_id:
            return jsonify({"status": 400, "message": "order_id is required"})

        is_updated = updateOrderAllFields(order_id, order_status='cancelled', order_cancel_status='yes')
        if is_updated:
            return jsonify({"status": 200, "message": "Order cancelled successfully"})
        else:
            return jsonify({"status": 400, "message": "Order not found"})
    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


# ─────────────────────────────────────────────────────────────
# Stock Routes
# ─────────────────────────────────────────────────────────────

@app.route('/stock', methods=['POST'])
@jwt_required()
def add_stock():
    try:
        data = get_json()
        current_user_id = get_jwt_identity()

        required = ['product_id', 'order_id', 'product_name', 'user_name', 'certified', 'stocks', 'price', 'product_category']
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({"status": 400, "message": f"Missing fields: {', '.join(missing)}"})

        stock_id = addStockOperation(
            user_id=current_user_id,
            user_name=data.get('user_name'),
            product_id=data.get('product_id'),
            category=data.get('product_category'),
            product_name=data.get('product_name'),
            certified=data.get('certified'),
            price=data.get('price'),
            stock=data.get('stocks'),
            order_id=data.get('order_id')
        )

        if stock_id:
            return jsonify({"status": 200, "message": "Stock added successfully"})
        else:
            return jsonify({"status": 400, "message": "Failed to add stock"})

    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


@app.route('/getAllStock', methods=['GET'])
@jwt_required()
def get_all_stock():
    return getAllStockItem()


@app.route('/stockUpdate', methods=['PATCH'])
@jwt_required()
def update_stock():
    try:
        data = get_json()
        stock_id = data.get('stock_id', '')
        if not stock_id:
            return jsonify({"status": 400, "message": "stock_id is required"})

        update_fields = {k: v for k, v in data.items() if k != 'stock_id'}
        is_updated = updateStockAllFields(stock_id, **update_fields)

        if is_updated:
            return jsonify({"status": 200, "message": "Stock updated successfully"})
        else:
            return jsonify({"status": 400, "message": "Stock not found"})

    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


@app.route('/deleteStock', methods=['DELETE'])
@jwt_required()
def delete_stock():
    try:
        data = get_json()
        stock_id = data.get('stock_id', '')
        if not stock_id:
            return jsonify({"status": 400, "message": "stock_id is required"})

        is_deleted = deleteStock(stockId=stock_id)
        if is_deleted:
            return jsonify({"status": 200, "message": "Stock deleted successfully"})
        else:
            return jsonify({"status": 400, "message": "Stock not found"})

    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


# ─────────────────────────────────────────────────────────────
# Sell History Routes
# ─────────────────────────────────────────────────────────────

@app.route('/sell_history', methods=['POST'])
@jwt_required()
def add_sell_history():
    try:
        data = get_json()
        current_user_id = get_jwt_identity()

        required = ['product_id', 'quantity', 'remaining_stock', 'date_of_sell', 'total_amount', 'price', 'product_name', 'user_name', 'product_category']
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({"status": 400, "message": f"Missing fields: {', '.join(missing)}"})

        history_id = addSellHistoryOperation(
            user_id=current_user_id,
            user_name=data.get('user_name'),
            product_id=data.get('product_id'),
            product_category=data.get('product_category'),
            product_name=data.get('product_name'),
            price=data.get('price'),
            remaining_stock=data.get('remaining_stock'),
            date_of_sell=data.get('date_of_sell'),
            total_amount=data.get('total_amount'),
            quantity=data.get('quantity')
        )

        if history_id:
            return jsonify({"status": 200, "message": "Sell history recorded"})
        else:
            return jsonify({"status": 400, "message": "Failed to record sell history"})

    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


@app.route('/getAllSellHistory', methods=['GET'])
@jwt_required()
def get_all_sell_history():
    return getAllSellHistoryItem()


@app.route('/getSpecificSellHistory', methods=['POST'])
@jwt_required()
def get_specific_sell_history():
    try:
        data = get_json()
        sell_id = data.get('sell_id', '')
        if not sell_id:
            return jsonify({"status": 400, "message": "sell_id is required"})
        return getSpecificSellHistoryItem(sell_id=sell_id)
    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


@app.route('/updateSellHistory', methods=['PATCH'])
@jwt_required()
def update_sell_history():
    try:
        data = get_json()
        sell_id = data.get('sell_id', '')
        if not sell_id:
            return jsonify({"status": 400, "message": "sell_id is required"})

        update_fields = {k: v for k, v in data.items() if k != 'sell_id'}
        is_updated = updateSellHistoryItemFields(sell_id, **update_fields)

        if is_updated:
            return jsonify({"status": 200, "message": "Sell history updated successfully"})
        else:
            return jsonify({"status": 400, "message": "Record not found"})

    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


@app.route('/deleteSellHistory', methods=['DELETE'])
@jwt_required()
def delete_sell_history():
    try:
        data = get_json()
        sell_id = data.get('sell_id', '')
        if not sell_id:
            return jsonify({"status": 400, "message": "sell_id is required"})

        is_deleted = deleteSellHistroyItem(sell_Id=sell_id)
        if is_deleted:
            return jsonify({"status": 200, "message": "Sell history deleted successfully"})
        else:
            return jsonify({"status": 400, "message": "Record not found"})

    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})


# ─────────────────────────────────────────────────────────────
# App entry
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    createTables()
    createBannerTable()
    CreateProductTable()
    CreateOrderTable()
    createStockTable()
    createHistoryTable()
    app.run(debug=True)
