import streamlit as st 

# EDA Pkgs
import pandas as pd 
import numpy as np 


# Utils
import os
import joblib 
import hashlib
# passlib,bcrypt

# Data Viz Pkgs
import seaborn as sns
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use('Agg')

from PIL import Image

# DB
from managed_db import *
def generate_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


# Password
def verify_hashes(password,hashed_text):
    if generate_hashes(password) == hashed_text:
        return hashed_text
    return False

feature_names_best = ['emailer_for_promotion','homepage_featured','city_code','region_code', 'op_area', 'category', 'cuisine']
feature_dict = {"No":0,"Yes":1}
cuisine_dict = {"Continental":0,"Indian":1,"Italian":2,"Thai":3}
cat_dict = {"Beverages":0,"Biriyani":1,"Desert":2,"Extras":3,"Fish":4,"Other Snacks":5,"Pasta":6,"Pizza":7,"Rice Bowl":8 ,"Salad":9,"Sandwich":10,"Seafood":11,"Soup":12,"Starters":13}

def get_value(val,my_dict):
    for key,value in my_dict.items():
        if val == key:
            return value 

def get_key(val,my_dict):
    for key,value in my_dict.items():
        if val == key:
            return key

def get_fvalue(val):
    feature_dict = {"No":0,"Yes":1}
    for key,value in feature_dict.items():
        if val == key:
            return value 

# Load ML Models
def load_model(model_file):
    loaded_model = joblib.load(open(os.path.join(model_file),"rb"))
    return loaded_model

html_temp = """
        <div style="background-color:{};padding:10px;border-radius:10px">
        <h1 style="color:white;text-align:center;">FOOD DEMAND PREDICTION </h1>
        <h5 style="color:white;text-align:center;">WAREHOUSE </h5>
        </div>
        """
avatar1 ="https://www.shareicon.net/data/2016/07/26/801997_user_512x512.png"

result_temp ="""
    <div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
    <h4 style="color:white;text-align:center;">Algorithm:: {}</h4>
    <img src="https://www.shareicon.net/data/2016/07/26/801997_user_512x512.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
    <br/>
    <br/>   
    <p style="text-align:justify;color:white">{} % Prediction of future orders {}s</p>
    </div>
    """

result_temp2 ="""
    <div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
    <h4 style="color:white;text-align:center;">Algorithm:: {}</h4>
    <img src="https://www.shareicon.net/data/2016/07/26/801997_user_512x512.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
    <br/>
    <br/>   
    <p style="text-align:justify;color:white">{} % Prediction of future orders {}s</p>
    </div>
    """

prescriptive_message_temp ="""
    <div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
        <h3 style="text-align:justify;color:black;padding:10px">RECOMMENDED WAREHOUSE GOODS MODIFICATION</h3>
        <ul>
        <li style="text-align:justify;color:black;padding:10px">Recession Period Ahead</li>
        <li style="text-align:justify;color:black;padding:10px">Stock up the warehouse only with the number of orders predicted</li>
        <li style="text-align:justify;color:black;padding:10px">Don't stock up much perishable goods as they might lead to a loss due to rotting</li>
        <li style="text-align:justify;color:black;padding:10px">If the warehouse is already stocked high, check the temperature controls to prevent rotting.</li>
        <li style="text-align:justify;color:black;padding:10px">Promote the food items through email for a larger reach and thus profit</li>
        <ul>
        <h3 style="text-align:justify;color:black;padding:10px">Plan on providing free home delivery as people have just overcome from a pandemic situation</h3>
        <ul>
        <li style="text-align:justify;color:black;padding:10px">Count the stocks today</li>
        <li style="text-align:justify;color:black;padding:10px">Stock as per predicted</li>
        <li style="text-align:justify;color:black;padding:10px">Lose Less and be rewarded with happy customers!!</li>
        <ul>
    </div>
    """
descriptive_message_temp ="""
    <div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
        <h3 style="text-align:justify;color:black;padding:10px">Why Food Demand Forecasting?</h3>
        <p>The world has just recovered from a pandemic situation. If the demands of food items are less and stocks in the warehouse are more,it would lead to a loss. Also, higher demands and less warehouse stocks would lead to unhappy customer thus destroying the company's image. Hence, if the food demands in the future are predicted and perishable goods are stocked up as per upcoming predicted number of orders, the company would be at profit and customers shall be happy. Happy Food Demand Forecasting!!!</p>

    </div>
    """

@st.cache

def change_avatar():
    avatar_img = 'avatar.png'
    return avatar_img




def main():
    """Hep Mortality Prediction App"""
    st.title("Optimized Warehouse Management App")
    st.markdown(html_temp.format('royalblue'),unsafe_allow_html=True)

    menu = ["Home","Login","SignUp"]
    submenu = ["Plot","Prediction"]
    

    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.subheader("Home")
        st.text("Food Demand Prediction")
        st.markdown(descriptive_message_temp,unsafe_allow_html=True)
        
        im=Image.open('image.jpg')
        st.image(im,caption='PERISHABLE FOOD ITEMS',use_column_width=True)
        


    elif choice == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password",type='password')
        # av=Image.open('avatar.png')
        st.sidebar.markdown("![Alt Text](http://manabadi.co.in/Graphics/images/reguserEAM_icon.gif)")
        st.markdown("![Alt Text](https://s3-eu-west-1.amazonaws.com/rpf-futurelearn/programming-101-educators/Illustrations+and+animations/4.7-What-is-Abstraction.gif)")
        if st.sidebar.checkbox("Login"):
            create_usertable()
            hashed_pswd = generate_hashes(password)
            result = login_user(username,verify_hashes(password,hashed_pswd))
            # if password == "12345":
            if result:
                st.success("Welcome {}".format(username))

                activity = st.selectbox("Activity",submenu)
                if activity == "Plot":
                    st.subheader("Data Vis Plot")
                    df=pd.read_csv("data/clean_dataset.csv")
                    st.dataframe(df.head(50))
                    st.bar_chart(df['num_orders'])

                    if st.checkbox("Area Chart"):
                        all_columns = df.columns.to_list()
                        feat_choices = st.multiselect("Choose a Feature",all_columns)
                        new_df = df[feat_choices].head(50)
                        st.area_chart(new_df)
                    
                
                
                    
                        


                elif activity == "Prediction":
                    st.subheader("Predictive Analytics")

                    emailer_for_promotion = st.radio("WAS THIS FOOD ITEM PROMOTED THROUGH EMAIL?",tuple(feature_dict.keys()))
                    homepage_featured = st.radio("WAS THIS FOOD ITEM FEATURED ON THE HOMEPAGE?",tuple(feature_dict.keys()))
                    city_code = st.number_input("CITY CODE",100,900)
                    region_code = st.number_input("REGION CODE",10,99)
                    op_area = st.number_input("OPERATIONAL AREA",0.0,10.0)
                    category = st.selectbox("CATEGORY",tuple(cat_dict.keys()))
                    cuisine = st.selectbox("CUISINE",tuple(cuisine_dict.keys()))
                    feature_list = [get_fvalue(emailer_for_promotion),get_fvalue(homepage_featured),city_code,region_code,op_area,get_value(category,cat_dict),get_value(cuisine,cuisine_dict)]
                    st.write(len(feature_list))
                    st.write(feature_list)
                    pretty_result = {"emailer_for_promotion":emailer_for_promotion,"homepage_featured":homepage_featured,"city_code":city_code,"region_code":region_code,"op_area":op_area,"category":category,"cuisine":cuisine}
                    st.json(pretty_result)
                    single_sample = np.array(feature_list).reshape(1,-1)

                    model_choice = st.selectbox("Select Model",["LinearRegression","KNN","DecisionTreeRegression","GradientBoostRegression","LightGBMRegression"])
                    if st.button("Predict"):
                        st.subheader("NUMBER OF ORDERS FOR THIS FOOD ITEM IN THE SELECTED REGION SHALL BE:")
                        if model_choice == "KNN":
                            loaded_model = load_model("models/knn_regression_model.pkl")
                            prediction = loaded_model.predict(single_sample)
                
                        elif model_choice == "DecisionTreeRegression":
                            loaded_model = load_model("models/decisiontree_regression_model.pkl")
                            prediction = loaded_model.predict(single_sample)

                        elif model_choice == "GradientBoostRegression":
                            loaded_model = load_model("models/gradientboost_regression_model.pkl")
                            prediction = loaded_model.predict(single_sample)

                        elif model_choice == "LightGBMRegression":
                            loaded_model = load_model("models/lgbm_regression_model.pkl")
                            prediction = loaded_model.predict(single_sample)


                            
                        else:
                            loaded_model = load_model("models/linear_regression_model.pkl")
                            prediction = loaded_model.predict(single_sample)
                        st.write(prediction.round(0))
                        st.bar_chart(prediction)

                        if(prediction>=350):
                            st.success("THERE SHALL BE A SURGE IN THE NUMBER OF ORDERS IN THE NEAR FUTURE!")
                            st.success(" STOCK UP EARLY TO FULFIL ALL THE CUSTOMER DEMANDS")
                            st.balloons()
                        else:
                            st.warning("THERE SHALL BE A DROP IN THE NUMBER OF ORDERS IN THE NEAR FUTURE")
                            st.warning(" DO NOT STOCK UP MUCH AS IT WOULD LEAD TO A LOSS")
                            st.subheader("Follow the steps to prevent loss:")
                            st.markdown(prescriptive_message_temp,unsafe_allow_html=True)
                    

                            

                            


                    

            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        new_username = st.text_input("User name")
        new_password = st.text_input("Password", type='password')

        confirm_password = st.text_input("Confirm Password",type='password')
        if new_password == confirm_password:
            st.success("Password Confirmed")
        else:
            st.warning("Passwords not the same")
        
        if st.button("Submit"):
            create_usertable()
            hashed_new_password = generate_hashes(new_password)
            add_userdata(new_username,hashed_new_password)
            st.success("You have successfully created a new account")
            st.info("Login to Get Started")


    





if __name__ == '__main__':
    main()