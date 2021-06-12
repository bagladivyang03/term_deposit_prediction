import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.write("""
# Term Deposit Prediction App

Instructions for uploading CSV file 

1. Age(years) - 18 to 95

2. Job - Choose one value from Job in side-panel.

3. Housing - For yes choose 1 else 0

4. Contact - Choose one value from Contact Type in side-panel.

5. Campaign(No. of times contacted) - 1 to 63

6. Previous(No. of times contacted before this campaign) - 0 to 275

7. Poutcome - Choose one value from Previous Outcome in side-panel. 
""")

st.sidebar.header('User Input Features')

st.sidebar.markdown("""
[Example CSV input file](https://github.com/bagladivyang03/term_deposit_prediction/blob/main/example_input_csv.csv)
""")

uploaded_file = st.sidebar.file_uploader(
    "Upload your input CSV file", type=["csv"])

if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
else:
    def user_input_features():
        age = st.sidebar.slider('Age', 18, 95, 20)
        job = st.sidebar.selectbox('Job', ('blue-collar', 'management',
                                          'technician',
                                          'admin.',
                                          'services',
                                          'retired',
                                          'self-employed',
                                          'entrepreneur ',
                                          'unemployed',
                                          'housemaid',
                                          'student',
                                          'unknown'))
        housing = st.sidebar.selectbox('Housing Loan', ('Yes','No'))
        contact = st.sidebar.selectbox('Contact Type',('cellular','telephone','unknown'))
        campaign = st.sidebar.slider('No. of times contacted',1,63,10)
        previous = st.sidebar.slider('No. of times contacted before this campaign',0,275,45)
        poutcome = st.sidebar.selectbox('Previous Outcome',('success','failure','other','unknown'))
        if(housing == 'Yes'):
            housing = 1
        else:
            housing = 0
        data = {
            'age' : age,
            'job' : job,
            'housing' : housing,
            'contact' : contact,
            'campaign' : campaign,
            'previous' : previous,
            'poutcome'  : poutcome
        }
        features = pd.DataFrame(data, index=[0])
        return features
    input_df = user_input_features()


rows_of_input_df = input_df.shape[0]

client_raw_data = pd.read_csv('https://raw.githubusercontent.com/bagladivyang03/term_deposit_prediction/main/term_deposit_cleaned.csv?token=ANYVWH5TDT3GTDJEXU5JO4LAZXGZK')
client = client_raw_data.drop(columns=['subscribed','Unnamed: 0','balance'],axis=1)
df = pd.concat([input_df, client],axis=0)

encode = ['job','contact','poutcome']

for col in encode:
    dummy = pd.get_dummies(df[col], prefix=col)
    df = pd.concat([df,dummy],axis=1)
    del df[col]

df = df[:rows_of_input_df]
if df.shape[1] != 23:
    st.error('Please upload file as per given instructions.')
else:
    load_clf = pickle.load(open('term_rf.pkl', 'rb'))
    prediction = load_clf.predict(df)
    prediction_proba = load_clf.predict_proba(df)






    st.subheader('User Input features')

    if uploaded_file is not None:
        st.write(df)
    else:
        st.write('Awaiting CSV file to be uploaded. Currently using example input parameters (shown below).')
        st.write(df)

    st.subheader('Prediction')
    Client_subscription = np.array(['No','Yes'])
    if(prediction.size == 1):
        st.write('Client Subscribed - '+ Client_subscription[prediction][0])
    else:
        st.write(Client_subscription[prediction])

    st.subheader('Prediction Probability')
    st.write(prediction_proba)



