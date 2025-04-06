import sqlite3;
import pandas as pd;
import ast



conn = sqlite3.connect('my_database.db');

cursor = conn.cursor();

Cus_query = "Select * from Customers";

customer_data = pd.read_sql_query(Cus_query, conn);

Product_query = "Select * from Products";
product_data = pd.read_sql_query(Product_query, conn);

# print(customer_data.head())
# print(product_data.head())

conn.close();


class CustomerProfileAgent:
    def __init__(self, cutomer_data) :
        self.customer_data = customer_data
    
    def get_costumer_profile(self, customer_id):
        customer_info = self.customer_data[self.customer_data['Customer_ID'] == customer_id]
        if customer_info.empty:
            return None
        else:
            customer_info['Browsing_History'].apply(ast.literal_eval)
            cutomer_info_dict =  customer_info.iloc[0].to_dict()
            for key, value in cutomer_info_dict.items():
                if(key == 'Browsing_History' or key == 'Purchase_History'):
                    cutomer_info_dict[key] = ast.literal_eval(value)
            
            return cutomer_info_dict;

  


# Key Features : CustomerProfileAgent
# Encapsulation: Keeps customer data and operations together.
# Error Handling: Returns None instead of crashing on invalid IDs.
# Pandas Integration: Leverages DataFrame operations for efficient filtering.
    
# Trail Run:
# agent = CustomerProfileAgent(customer_data);
# info = agent.get_costumer_profile('C100011');
# print(info) 


# Product Analysis Agent Based on Geographical Location
class ProductAnalysisAgentGL:
    def __init__(self, product_data):
        self.product_data = product_data

    def filter_products(self, customer_location, category=None):
        filtered_product = self.product_data[self.product_data['Geographical_Location']=='India']
        if category:
            filtered_product = filtered_product[filtered_product['Category']== category]
        
        return filtered_product;


# agent = CustomerProfileAgent(customer_data);
# info = agent.get_costumer_profile('C10001');
# print(info)

# p_agent = ProductAnalysisAgentGL(product_data)
# filtered_product = p_agent.filter_products(info['Location']);
# print(filtered_product);


class ProductAnalysisAgentCategorical:
    def __init__(self, product_data):
        self.product_data = product_data

    def get_filter_products(self, customer_category):
        filtered_product = self.product_data[self.product_data['Geographical_Location'] == 'India']
        filtered_product = filtered_product[filtered_product['Category'] == customer_category]
        if filtered_product.empty:
            return None
        else:
            return filtered_product;


# Converting response to Tabular Format
from io import StringIO;
def convert_recomm_to_table(response):
    df_recom = pd.read_table(StringIO(response), sep = '|').dropna(axis=1, how='all')
    df_recom = df_recom.iloc[1:-1]
    return df_recom;


# Converting string to List
import ast
def convert_string_to_list(recom):
    if recom.startswith('['): 
        product_code = ast.literal_eval(recom)
        print(product_code, type(product_code))
        
    else :
        product_code = recom.split(', ')
    
    for i in range(len(product_code)):
            if product_code[i].startswith("P") == False:
                product_code[i] = 'P' + product_code[i]
    
            # print(product_code[i])

    

    return product_code;


def getDataFrame(product_codes):
    fil_product_list = product_data[product_data['Product_ID'].isin(product_codes)]
    return fil_product_list;


# Loading Phi-4 Mini Model from Ollama
import ollama;

def get_recommendation_history(customer_data, product_data):
    History = customer_data['Purchase_History']
    promt = f"""
    Given the following customer purchase history:
    {History}
    And the following Product List:
    {product_data}
    Recommend the best 5 products that match the customer's preferences.
    Also make sure to check the Product Rating.
    Return ONLY a array of string of Product ID.
    Include NO TEXT, NO EXPLANATION, NO NOTE.
    """
    # markdown table of each column : Product_ID, Category, Subcategory, Similar_Product_List.
    response = ollama.chat(model="phi4-mini", messages=[{'role': "user", "content" : promt}])

    if type(response["message"]["content"]) != str :
         response =  get_recommendation_history(customer_data, product_data);
         return response
    resp_list = convert_string_to_list(response.message.content)
    return resp_list





def get_recomm_browsing_history(customer_data, product_data):
    History = customer_data['Browsing_History']
    promt = f"""
    Given the following customer Browsing history:
    {History}
    And the following Product List:
    {product_data}
    Recommend the best 5 products that match the customer's preferences.
    Also make sure to check the Product Rating.
    Return ONLY a array of string of Product ID.
    Include NO TEXT, NO EXPLANATION, NO NOTE.
    """
    
    response = ollama.chat(model="phi4-mini", messages=[{'role': "user", "content" : promt}])

    if type(response["message"]["content"]) != str :
         response =  get_recommendation_history(customer_data, product_data);
         return response
    
    resp_list = convert_string_to_list(response.message.content)
    return resp_list



    
def get_recomm_based_on_season(customer_data, product_data):
    Season = customer_data['Season']
    History = customer_data['Purchase_History']
    promt = f"""
    Given the following customer purchase history {History} and Season {Season}

    And the following Product List:
    {product_data}
    Recommend the best 5 products that match the customer's preferences.
    Also make sure to check the Product Rating.     
    Return ONLY a array of string of Product ID.

    Include NO TEXT, NO EXPLANATION, NO NOTE.
    """
    # markdown table of each column : Product_ID, Category, Subcategory, Similar_Product_List.
    response = ollama.chat(model="phi4-mini", messages=[{'role': "user", "content" : promt}])

    if type(response["message"]["content"]) != str :
         response =  get_recommendation_history(customer_data, product_data);
         return response
    
    resp_list = convert_string_to_list(response.message.content)
    return resp_list


def get_message(customer_info):
    History = customer_info['Purchase_History'];
    prompt = f"""
    Given the Following Customer Information:
    {customer_info}
    Create a clever message based on his last order:
    {History}
    RETURN ONLY THE MESSAGE.
    """
    response = ollama.chat(model="phi4-mini", messages=[{'role': "user", "content" : prompt}])
    print(response.message.content, type(response.message))
    return(response.message.content);

def get_final_recomm(prod_list, product_data):
    promt = f"""
    Given the following Product ID Liked by the customer:
    {prod_list}
    And the following Product Data:
    {product_data}
    Recommend 200 similar products from the Product data.
    Make sure they are not the same products as {prod_list}.
    Also make sure to check the Product Rating.
    Return ONLY a array of string of Product ID.
    Include NO TEXT, NO EXPLANATION, NO NOTE.
    """
    
    response = ollama.chat(model="phi4-mini", messages=[{'role': "user", "content" : promt}])

    if type(response["message"]["content"]) != str :
         response =  get_recommendation_history(customer_data, product_data);
         return response
    
    resp_list = convert_string_to_list(response.message.content)
    return resp_list


def get_info(customer_id):
    agentC = CustomerProfileAgent(customer_data)
    customerInfo = agentC.get_costumer_profile(customer_id)
    return customerInfo;

def get_product_data(info, product_data):
    agentP = ProductAnalysisAgentCategorical(product_data);
    filteredProducts = agentP.get_filter_products(info['Browsing_History'][0])
    return filteredProducts;
    


# agent = CustomerProfileAgent(customer_data);
# info = agent.get_costumer_profile('C1000');
# res = get_recomm_based_on_season(info, product_data)   
# print(res)

# ---------------------------------------------------------------------------------------------------

# Trail Run
# agent = CustomerProfileAgent(customer_data);
# info = agent.get_costumer_profile('C1000');
# print(info)

# agentP = ProductAnalysisAgentCategorical(product_data);
# filteredProducts = agentP.get_filter_products(info['Browsing_History'][0])

# recomm = get_recommendation_history(info, filteredProducts);
# print(recomm, type(recomm))

# df = getDataFrame(recomm)
# print(df)


# # Convert This Product code into dataframe

# fil_aL = getDataFrame(product_code)
# print(fil_aL)
        
# -------------------------------------------------------------------------------------------------------
# Running Python Script in React

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app);

@app.route('/api/login', methods = ['POST'])
def login():
    customer_id = request.json.get('customerID')
    
    if not customer_id:
        return jsonify({'error': 'Customer ID is Required'}), 400


    agentC = CustomerProfileAgent(customer_data)
    customerInfo = agentC.get_costumer_profile(customer_id)
    

    if customerInfo == None :
        return jsonify({'error' : 'No customer found'}), 300

    return jsonify({
        'message' : f'Data for {customer_id}',
        'data' : customerInfo
    })

@app.route('/api/user/Recomm1/<customer_id>')
def get_profile(customer_id):
    customerInfo = get_info(customer_id)
    message = get_message(customerInfo)

    if customerInfo == None :
        return jsonify({'error' : 'No customer found'}), 300

    return jsonify(message)

@app.route('/api/user/LastPurchase/<customer_id>')
def get_last_purchase_data(customer_id):
    customerInfo = get_info(customer_id)
    filter_data = get_product_data(customerInfo, product_data)
    product_recom = get_recommendation_history(customerInfo, filter_data)
    print(product_recom)
    p_df = getDataFrame(product_recom)
    if customerInfo == None :
        return jsonify({'error' : 'No customer found'}), 300
    p_data = p_df.to_dict(orient='records')
    # print(p_data)
    return jsonify(p_data)


@app.route('/api/user/BrowsingHistory/<customer_id>')
def get_browsing_history_data(customer_id):
    customerInfo = get_info(customer_id)
    filter_data = get_product_data(customerInfo, product_data)
    product_recom = get_recomm_browsing_history(customerInfo, filter_data)
    print(product_recom)
    p_df = getDataFrame(product_recom)
    if customerInfo == None :
        return jsonify({'error' : 'No customer found'}), 300
    p_data = p_df.to_dict(orient='records')
    return jsonify(p_data)

@app.route('/api/user/Season/<customer_id>')
def get_season_data(customer_id):
    customerInfo = get_info(customer_id)
    filter_data = get_product_data(customerInfo, product_data)
    product_recom = get_recomm_based_on_season(customerInfo, filter_data)
    print(product_recom)
    p_df = getDataFrame(product_recom)
    if customerInfo == None :
        return jsonify({'error' : 'No customer found'}), 300
    p_data = p_df.to_dict(orient='records')
    return jsonify(p_data)

@app.route('/api/recommendInterestedData', methods = ['POST'])
def get_interested_data():
    interested_products = request.json.get('interested_products')
    print("Here is the list of product ", interested_products, type(interested_products))
    product_recom = get_final_recomm(interested_products, product_data)
    p_df = getDataFrame(product_recom)
    p_data = p_df.to_dict(orient='records')
    return jsonify(p_data)
    

    

if __name__ == ('__main__'):
    app.run(debug=True)


    
    

