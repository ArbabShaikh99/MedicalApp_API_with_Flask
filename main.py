from flask import Flask,jsonify,request,Response

from werkzeug.utils import secure_filename
from Medical_DataBase.uploadImg.db import db_init,db
from Medical_DataBase.uploadImg.models import Img


from Medical_DataBase.User_DB.CreateUserTable import createTables
from Medical_DataBase.User_DB.UserAddOperation import createUser
from Medical_DataBase.User_DB.ReadUserOperation import getAllUsers,getSpecificUser
from Medical_DataBase.User_DB.auth import user_auth
from Medical_DataBase.User_DB.UpdateOperation import update_user_name,upDate_User_All_Fields
from Medical_DataBase.User_DB.DeleteUserOperation import DeleteUser

from Medical_DataBase.Product_DB.CreateProductTable import CreateProductTable
from Medical_DataBase.Product_DB.ReadProductOperation import getAllProducts,getSpecifiProduct
from Medical_DataBase.Product_DB.ProductAddOperation import addProductOperation
from Medical_DataBase.Product_DB.DeleteProductOperation import deleteProduct
from Medical_DataBase.Product_DB.UpDateProductOperation import updateProductAllFields
from Medical_DataBase.Order_DB.CreateOrderTable import CreateOrderTable
from Medical_DataBase.Order_DB.ReadOrderOperation import getAllOrder,getAllOrderThroughUser,getSpecificOrder
from Medical_DataBase.Order_DB.OrderAddOperation import addOrderOperation
from Medical_DataBase.Order_DB.UpdateOrderOperation import updateOrderAllFields 
from Medical_DataBase.Order_DB.DeleteOrderOperation import deleteOrder

from Medical_DataBase.UserStock_DB.AddUserStockOperation import addStockOperation
from Medical_DataBase.UserStock_DB.CreateUserStockTable import createStockTable
from Medical_DataBase.UserStock_DB.DeleteUserStckOperation import deleteStock
from Medical_DataBase.UserStock_DB.ReadUserStockOperation import getAllStockItem
from Medical_DataBase.UserStock_DB.UpdateUserStockOperation import updateStockAllFields

from Medical_DataBase.history_db.createHistoryTable  import createHistoryTable
from Medical_DataBase.history_db.addHistoryOperation import addSellHistoryOperation
from Medical_DataBase.history_db.readHistoryOperation import getAllSellHistoryItem,getSpecificSellHistoryItem
from Medical_DataBase.history_db.deleteSellHistoryOperation import deleteSellHistroyItem
from Medical_DataBase.history_db.updateSalteHistoryOperation import updateSellHistoryItemFields


app =Flask(__name__)

# SQLAlchemy config. Read more: https://flask-sqlalchemy.palletsprojects.com/en/2.x/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)





@app.route('/getImg/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)


@app.route("/")
def home():
    return "Hello, Flask!"


# --------------- User Routes ----------------------


        # name = request.form['name']
        # password = request.form['password']
        # email = request.form['email']
        # phone = request.form['phone']
        # address = request.form['address']
        # pinCode = request.form['pinCode']
@app.route('/signUp', methods=['POST'])
def signup():
    try:
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        pinCode = request.form['pinCode']

        data = createUser(name=name, password=password, email=email, phone_Number=phone,
                          address=address, pinCode=pinCode)

        if data:
            return jsonify({"status": 200, "message": data})
        else:
            return jsonify({"status": 400, "message": data })

    except Exception as e:
        return jsonify({"status": 400, "message": str(e)})



@app.route('/Login' ,methods=['POST'])
def login():
    try:
         email= request.form['email']
         password = request.form['password']

         loginData = user_auth(email=email  ,password=password)

         if loginData:
          return jsonify({"status" : 200 , "message":loginData[1]})
         else:
           return jsonify({"status" : 400 , "message":"Email and Password not same"})
        
    except Exception as e:
         return jsonify({"status" : 400 , "message":str(e)})

   
@app.route('/UpDateUserDetails',methods=['PATCH'])
def UpDateUserNameMain():
    try:
        UserID =request.form['userID']
        allfields=request.form.items()
        updateUser = {}

        for key , value in allfields:
            if key!='userID':
             updateUser[key] =value

        upDate_User_All_Fields(userID=UserID,**updateUser)

        return jsonify({"status":200,"message":"Data update"})
    except Exception as e:
            return jsonify({"status":400,"message":str(e)})
    

@app.route('/updateUserName',methods=['PATCH'])
def updateUserNameMain():
     try:
          newName = request.form['updateName']
          userId = request.form['userId']

          isUpdate = update_user_name(userId = userId,name = newName)
               
          if(isUpdate):  
                return jsonify({"status":200,"message":"User Name Updated Successfully"})
          else:
                return jsonify({"status":400,"message":"User Id not found!"})
     
     except Exception as e:
          return jsonify({"status":400,"message":str(e)})
     
    

    

@app.route('/getSpecificUser',methods=['POST'])
def getSpecificUserMain():
    try:
        userID =request.form['userID']
        getUserInfo = getSpecificUser(userID=userID)
        return getUserInfo
    except Exception as e:
        return jsonify({"status":400,"message": str(e)})



@app.route('/getAllUsers', methods=['GET'])
def getAllUser():
    return getAllUsers()


@app.route('/DeleteUser', methods=['DELETE'])
def deleteUser():
    try:
        UserID = request.form['UserID']
        isDeleted = DeleteUser(UserID=UserID)

        if(isDeleted) :
            return jsonify({"Status":200,"message":"User Data Deleted Successfully"})
        else:
            return jsonify({"status":400,"message":"User Id not found!"})
        
    except Exception as e:
        return jsonify({"status":400, "message" :str(e)})



# Route to get user status
@app.route('/getUserStatus/<userId>', methods=['GET'])
def get_user_status(userId):
    user = query_db('SELECT * FROM Users WHERE user_id = ?', (userId,), one=True)
    if user:
        return jsonify(dict(user)), 200
    else:
        return jsonify({"message": "User not found"}), 404




# -------------------- Product Routes -------------------------------

    

    

@app.route('/addProduct',methods=['POST'])
def addProduct():
    try:
        name = request.form['product_name']
        category = request.form['product_category']
        price = request.form['product_price']
        stock = request.form['product_stock']
        expiry_date = request.form['product_expiry_date']
        rating = request.form['product_rating']
        description = request.form['product_description']
        power = request.form['product_power']       

    
        pic = request.files['pic']
        if not pic:
           return 'No pic uploaded!', 400

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
             return 'Bad upload!', 400

        img = Img(img=pic.read(), name=filename, mimetype=mimetype)
        db.session.add(img)
        db.session.commit()
    
        if(validate_product(name,category,price,stock,expiry_date,rating,description,power)):
               product_id = addProductOperation(
                name=name,
                category=category,
                price=price,
                stock=stock,
                expiry_date=expiry_date,
                rating=rating,
                description=description,
                image=img.id,
                power=power
            )
        else:
             return jsonify({"status": 400, "message": "Mandatory field empty"})
                 
        if product_id:
              return jsonify({"status" : 200,"message" : product_id})
        else:
            return jsonify({"status" : 400,"message":product_id})
    except Exception as e:
           return jsonify({"status":400,"message":str(e)})      

def validate_product(name,category,price,stock,expiry_date,rating,description,power):
    if not name or not category or not price or not stock or not expiry_date or not rating or not description or not power:
        return 0
    else:
         return 1
         
         

        


@app.route('/getProduct',methods=['GET'])
def getProducts():
    return getAllProducts()

     

@app.route('/getSpecificProduct',methods=['POST'])
def getSpecificProductMain():
    try:
        ProductID =request.form['ProductID']
        getProductInfo = getSpecifiProduct(ProductID=ProductID)
        return getProductInfo
    except Exception as e:
        return jsonify({"status":400,"message":str(e)})
    

@app.route('/deleteProduct',methods=['DELETE'])
def deleteProductOperation():
     try:
          ProductId = request.form['ProductID']
          isDeleted = deleteProduct(productId=ProductId)

          if isDeleted:  
                return jsonify({"status":200,"message":"Product Deleted Successfully"})
          else:
                return jsonify({"status":400,"message":"Product Id not found!"})
     
     except Exception as e:
          return jsonify({"status":400,"message":str(e)})

@app.route('/updateProducts' ,methods=['PATCH'])
def UpdateProductsOperation():
    try:
        ProductID =request.form['ProductID']
        allfields=request.form.items()
        updateProduct = {}

        for key , value in allfields:
            if key!='ProductID':
             updateProduct[key] =value

            updateProductAllFields(productId=ProductID ,**updateProduct)

        return jsonify({"status":200,"message":"Product update"})
    except Exception as e:
            return jsonify({"status":400,"message":str(e)})
        



# ------------------------ ORDER Routes -------------------



@app.route('/order',methods=['POST'])
def order():

    try:
        user_id = request.form['user_id']  #field name
        product_id = request.form['product_id']
        product_name = request.form['product_name']
        product_category = request.form['product_category']
        product_image_id = request.form['product_image_id']
        user_name = request.form['user_name']
        isApproved = request.form['isApproved']
        quantity = request.form['product_quantity']
        price = request.form['product_price']
        subtotalPrice = request.form['subtotal_price']
        deliveryCharge = request.form['delivery_charge']
        taxCharge = request.form['tax_charge']
        totalPrice = request.form['total_price']
        orderDate = request.form['order_date']
        user_address = request.form['user_address']
        user_pinCode = request.form['user_pincode']
        user_mobile = request.form['user_mobile']
        user_email = request.form['user_email']
        order_status = request.form['order_status']
        order_cancel_status = request.form['order_cancel_status']
        user_street = request.form['user_street']
        user_city = request.form['user_city']
        user_state = request.form['user_state']
        discountPrice = request.form['discount_price']
        shipped_date = request.form['shipped_date']
        out_of_delivery_date = request.form['out_of_delivery_date']
        delivered_date = request.form['delivered_date']

        orders = addOrderOperation(
             user_id=user_id,
                product_id=product_id,product_name=product_name,user_name=user_name,isApproved=isApproved,
                product_quantity=quantity,product_price=price,totalPrice=totalPrice,orderDate=orderDate,
                product_category=product_category,product_image_id = product_image_id, subtotal_price=subtotalPrice,
                tax_charge=taxCharge,delivery_charge=deliveryCharge,user_email=user_email,user_address=user_address,
                user_mobile=user_mobile,user_pinCode=user_pinCode,order_status=order_status,order_cancel_status=order_cancel_status,
                user_street=user_street,user_city=user_city,user_state=user_state,discountPrice=discountPrice,
                shipped_date=shipped_date,out_of_delivery_date=out_of_delivery_date,delivered_date=delivered_date
        )
        if orders:
            return jsonify({"status" : 200,"message" : "Order Add Suceesfully"})
        else:
            return jsonify({"status" : 400,"message":"NO Add Order"})
        
    except Exception as e:
        return jsonify({"status":400,"message":str(e)})



@app.route('/getAllOrders',methods=['GET'])
def getOrder():
     return getAllOrder()

@app.route('/getSpecificOrder',methods=['POST'])
def getSpecificOrderMain():
     try:
          orderId = request.form['order_id']
          getOrderInfo = getSpecificOrder(orderId = orderId)
          return getOrderInfo
     
     except Exception as e:
        return jsonify({"status":400,"message":str(e)})
     
@app.route('/getAllOrderThroughUser',methods=['POST'])
def getAllOrderThroughUserMain():
     try:
          userId = request.form['user_id']
          getAllOrderThroughUserList = getAllOrderThroughUser(user_id = userId)
          return getAllOrderThroughUserList
     
     except Exception as e:
        return jsonify({"status":400,"message":str(e)})
    


   

@app.route('/updateOrder',methods=['PATCH'])
def updateOrderOperation():
     try:
          orderId = request.form['orderId']

          allFields = request.form.items()
          updateOrder = {}

          for key,value in allFields:
               if key != 'orderId':
                    updateOrder[key] = value

          isUpdated = updateOrderAllFields(orderId,**updateOrder)

          if(isUpdated):  
                 return jsonify({"status":200,"message":"data updated Successfull"})
          else:
                return jsonify({"status":400,"message":"Order Id not found!"})
                    
     except Exception as e:
          return jsonify({"status":400,"message":str(e)})



@app.route('/deleteOrder',methods=['DELETE'])
def deleteOrderOperation():
    try:
          orderId = request.form['order_id']
          isDeleted = deleteOrder(orderId=orderId)

          if(isDeleted):  
                return jsonify({"status":200,"message":"Order Deleted Successfully"})
          else:
                return jsonify({"status":400,"message":"Order Id not found!"})
     
    except Exception as e:
          return jsonify({"status":400,"message":str(e)})
    


# --------------------------- USER STOCK Routes -----------------------


@app.route('/stock',methods=['POST'])
def stock():

    try:
        user_id = request.form['user_id']  
        product_id = request.form['product_id']
        order_id = request.form['order_id']
        product_name = request.form['product_name']
        user_name = request.form['user_name']
        certified = request.form['certified']
        stock = request.form['stocks']
        price = request.form['price']
        category = request.form['product_category']

        if(validate_stock_data(user_id,product_id,product_name,user_name,certified,stock,price,category,order_id)):
            stockId = addStockOperation(
                user_id=user_id,
                user_name=user_name,
                product_id=product_id,
                category=category,
                product_name=product_name,
                certified=certified,
                price=price,
                stock=stock,
                order_id=order_id
           )
        else:
             return jsonify({"status": "Invalid User", "message": "Mandatory field empty"})
                 
        if stockId:
            return jsonify({"status" : 200,"message" : "Stock Product added."})
        else:
            return jsonify({"status" : 400 ,"message":"Something went wrong."})
        
    except Exception as e:
        return jsonify({"status":400,"message":str(e)})
    
def validate_stock_data(user_id,product_id,product_name,user_name,certified,stock,price,category,order_id):
    if not user_id or not product_id or not product_name or not user_name or not certified or not stock or not price or not category or not order_id:
        return 0
    else:
         return 1

@app.route('/getAllStock',methods=['GET'])
def getAllStock():
     return getAllStockItem()

@app.route('/stockUpdate',methods=['PATCH'])
def stockUpdateOperation():
    try:
        stockId = request.form['stock_id']

        allFields = request.form.items()
        updateStock = {}

        for key,value in allFields:
                    if key != 'stock_id':
                            updateStock[key] = value

        isUpdated = updateStockAllFields(stockId,**updateStock)
        if(isUpdated):  
                    return jsonify({"status":200,"message":"Stock updated Successfull"})
        else:
                    return jsonify({"status":400,"message":"Stock Id not found!"})
                          
    except Exception as e:
              return jsonify({"status":400,"message":str(e)})

@app.route('/deleteStock',methods=['DELETE'])
def deleteStockOperation():
    try:
          stockId = request.form['stock_id']
          isDeleted = deleteStock(stockId=stockId)

          if(isDeleted):  
                return jsonify({"status":200,"message":"Stock Deleted Successfully"})
          else:
                return jsonify({"status":400,"message":"Stock Id not found!"})
     
    except Exception as e:
          return jsonify({"status":400,"message":str(e)})

# --------------------------- History Routes -----------------------



@app.route('/sell_history',methods=['POST'])
def sell_History():
    try:
        user_id = request.form['user_id']  #field name
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        remaining_stock = request.form['remaining_stock']
        date_of_sell = request.form['date_of_sell']
        total_amount = request.form['total_amount']
        price = request.form['price']
        product_name = request.form['product_name']
        user_name = request.form['user_name']
        product_category = request.form['product_category']

        if(validate_history_data(user_id,product_id,product_name,user_name,quantity,remaining_stock,price,product_category,date_of_sell,total_amount)):
            stockId = addSellHistoryOperation(
                user_id=user_id,
                user_name=user_name,
                product_id=product_id,
                product_category=product_category,
                product_name=product_name,
                price=price,
                remaining_stock=remaining_stock,
                date_of_sell=date_of_sell,
                total_amount=total_amount,
                quantity=quantity
           )
        else:
             return jsonify({"status": 400, "message": "Mandatory field empty"})
                 
        if stockId:
            return jsonify({"status" : 200,"message" : stockId})
        else:
            return jsonify({"status" : 400 ,"message":"Something went wrong."})
        
    except Exception as e:
        return jsonify({"status":400,"message":str(e)})
    
def validate_history_data(user_id,product_id,product_name,user_name,quantity,remaining_stock,price,product_category,date_of_sell,total_amount):
    if not user_id or not product_id or not product_name or not user_name or not quantity or not remaining_stock or not price or not product_category or not date_of_sell or not total_amount:
        return 0
    else:
         return 1

@app.route('/getAllSellHistory',methods=['GET'])
def getAllSellHistoryOperation():
    return getAllSellHistoryItem()


@app.route('/getSpecificSellHistory',methods=['POST'])
def getSpecificSellHistoryProduct():
    try:
          sellId = request.form['sell_id']
          getSellHistoryInfo = getSpecificSellHistoryItem(sell_id=sellId)
          return getSellHistoryInfo
     
    except Exception as e:
        return jsonify({"status":400,"message":str(e)})

@app.route('/updateSellHistory',methods=['PATCH'])
def updateSellHistoryItem():
    try:
        sellId = request.form['sell_id']

        allFields = request.form.items()
        updateSellItem = {}

        for key,value in allFields:
                    if key != 'sell_id':
                            updateSellItem[key] = value

        isUpdated = updateSellHistoryItemFields(sellId,**updateSellItem)
        if(isUpdated):  
            return jsonify({"status":200,"message":"Sell history updated Successfull"})
        else:
            return jsonify({"status":400,"message":"Sell Id not found!"})
                          
    except Exception as e:
        return jsonify({"status":400,"message":str(e)})

@app.route('/deleteSellHistory',methods=['DELETE'])
def deleteSellHistoryOperation():
    try:
          sell_id = request.form['sell_id']
          isDeleted = deleteSellHistroyItem(sell_Id=sell_id)

          if(isDeleted):  
                return jsonify({"status":200,"message":"History Sell item Deleted Successfully"})
          else:
                return jsonify({"status":400,"message":"Sell Id not found!"})
     
    except Exception as e:
          return jsonify({"status":400,"message":str(e)})


if __name__ =="__main__":
    createTables()
    CreateProductTable()
    CreateOrderTable()
    createStockTable()
    createHistoryTable()

    
    app.run(debug=True)