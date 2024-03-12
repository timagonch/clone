import pickle


with open('./pickle/sorted_top_recommendations.pkl', 'rb') as file:
    df_recom = pickle.load(file)
#check what are the types of the columns
print(df_recom.dtypes)


