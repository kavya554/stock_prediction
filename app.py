import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
from keras.models import load_model
import streamlit as st

start='2012-01-01'
end='2021-12-31'

st.title('Predict Stock Trend')

user_input=st.text_input('Enter stock ticker','MSFT')
df=data.DataReader(user_input,'yahoo',start,end)

#describing data

st.subheader('Data from 2012-2021')
st.write(df.describe())

#visualization
st.subheader('Closing Price vs Time chart')
fig=plt.figure(figsize=(12,6))
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Closing Price vs Time chart with 100MA')
ma100=df.Close.rolling(100).mean()
fig=plt.figure(figsize=(12,6))
plt.plot(ma100)
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Closing Price vs Time chart with 100MA & 200MA ')
ma100=df.Close.rolling(100).mean()
ma200=df.Close.rolling(200).mean()
fig=plt.figure(figsize=(12,6))
plt.plot(ma100,'g')
plt.plot(ma200,'r')
plt.plot(df.Close,'b')
st.pyplot(fig)

#splitting data into training and testing
data_training=pd.DataFrame(df['Close'][0:int(len(df)*0.70)])  # we are only interested in close column so only splitting that
data_testing=pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])


# scaling
from sklearn.preprocessing import MinMaxScaler
scaler=MinMaxScaler(feature_range=(0,1))   #Transform features by scaling each feature to a given range.

data_training_array=scaler.fit_transform(data_training)



#Load the model
model=load_model('keras_model01.h5')


#Testing part
past_100_days=data_training.tail(100)
final_df=pd.concat([past_100_days,data_testing],ignore_index=True)
input_data=scaler.fit_transform(final_df)

x_test=[]
y_test=[]

for i in range(100,input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i,0])

x_test,y_test=np.array(x_test),np.array(y_test)

#making predictions

y_predicted=model.predict(x_test)

scaler=scaler.scale_
scale_factor=1/scaler[0]
y_predicted=y_predicted*scale_factor
y_test=y_test*scale_factor

#final graph
st.subheader('Prediction vs Original')
fig2=plt.figure(figsize=(12,6))
plt.plot(y_test,'b',label='Original Price')
plt.plot(y_predicted,'r',label='Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)