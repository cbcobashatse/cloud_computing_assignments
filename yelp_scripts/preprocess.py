'''
Pieces of code in this file were used to preprocess
the data scraped from Yelp and format it so that it
can be uploaded to DynamoDB and OpenSearch
'''


import pandas as pd
import json

african_restaurants_df = pd.read_csv('restaurant_records/african_restaurant_records.csv')
american_restaurants_df = pd.read_csv('restaurant_records/american_restaurant_records.csv')
caribbean_restaurants_df = pd.read_csv('restaurant_records/caribbean_restaurant_records.csv')
chinese_restaurants_df = pd.read_csv('restaurant_records/chinese_restaurant_records.csv')
french_restaurants_df = pd.read_csv('restaurant_records/french_restaurant_records.csv')
indian_restaurants_df = pd.read_csv('restaurant_records/indian_restaurant_records.csv')
thai_restaurants_df = pd.read_csv('restaurant_records/thai_restaurant_records.csv')

all_restaurant_df = pd.read_csv('restaurant_records/all_restaurant_records.csv')

african_restaurants_json = pd.read_json('json_records/african_restaurant_records.json')
american_restaurants_json = pd.read_json('json_records/american_restaurant_records.json')
caribbean_restaurants_json = pd.read_json('json_records/caribbean_restaurant_records.json')
chinese_restaurants_json = pd.read_json('json_records/chinese_restaurant_records.json')
french_restaurants_json = pd.read_json('json_records/french_restaurant_records.json')
indian_restaurants_json = pd.read_json('json_records/indian_restaurant_records.json')
thai_restaurants_json = pd.read_json('json_records/thai_restaurant_records.json')


cuisines = ['african', 'american', 'caribbean', 'chinese', 'french', 'indian', 'thai']
restaurant_dfs = [african_restaurants_df, american_restaurants_df, caribbean_restaurants_df,
                  chinese_restaurants_df, french_restaurants_df, indian_restaurants_df, thai_restaurants_df]
restaurant_jsons = [african_restaurants_json, american_restaurants_json, caribbean_restaurants_json,
                  chinese_restaurants_json, french_restaurants_json, indian_restaurants_json, thai_restaurants_json]

count = 0
for i in range(len(restaurant_jsons)):
    restaurant_json = restaurant_jsons[i]
    cuisine = cuisines[i]
    for index, row in restaurant_json.iterrows():
        count += 1
        # part_1 = str({"index": {"_index": "restaurants", "_type":"Restaurant", "_id": count}})
        part_1 = str({"index": {"_index": "restaurants", "_id": count}})
        part_2 = str({"RestaurantID": row["business_id"], "Cuisine": row["cuisine"]})
        # print(part_1)
        # print(part_2)
        with open("restaurants.json", "a") as jsonfile:
            jsonfile.write(part_1)
            jsonfile.write("\n")
            jsonfile.write(part_2)
            jsonfile.write("\n")

    print(count)


#--------------------generate JSON file for ElasticSearch
# {"index": {"_index": "Restaurant", "_id": 1}}
# {"RestaurantID": "business_id", "Cuisine": "thai"}
# part_1 = '{"index": {"_index": "Restaurant", "_id": 1}}'
# part_2 = '{"RestaurantID": "business_id", "Cuisine": "thai"}'
# with open('restaurants.json', 'a') as jsonfile:
#     jsonfile.write(part_1)
#     jsonfile.write('\n')
#     jsonfile.write(part_2)
#     jsonfile.write('\n')


#--------------------save restaurants to individual cuisine JSON files
# for i in range(len(restaurant_dfs)):
#     restaurant_df = restaurant_dfs[i]
#     cuisine = cuisines[i]
#     restaurant_df = restaurant_df.fillna("Value Unknown")
#     restaurant_json = restaurant_df.to_json(orient='records')
#     parsed = json.loads(restaurant_json)
#     json_records = json.dumps(parsed, indent=4)

#     # create JSON file with all restaurant records
#     filename = 'json_records/' + cuisine + '_restaurant_records.json'
#     with open(filename, 'w') as jsonfile:
#         jsonfile.write(json_records)


#----------------------combine all restaurants in one common file
#----------------------while removing duplicates and filling Nan values with "Value Unknown"
# all_restaurant_df = pd.concat(restaurant_dfs).reset_index().drop(columns='index')
# all_restaurant_df = all_restaurant_df.drop_duplicates()
# all_restaurant_df = all_restaurant_df.fillna("Value Unknown")
# filename = 'restaurant_records/all_restaurant_records.csv'
# all_restaurant_df.to_csv(filename, index=False)


#---------------------double check that there are no duplicate restaurants
# for restaurant_df in restaurant_dfs:
#     restaurant_df = restaurant_df.drop_duplicates()



#-------------------------include the type of cuisine in the dataframes

# # for each restaurant_df or for each cuisine
# for i in range(len(restaurant_dfs)):
#     restaurant_df = restaurant_dfs[i]
#     cuisine = cuisines[i]

#     # find the number of rows (data points) and have a list of such size with that cuisine as value
#     num_rows = restaurant_df.shape[0]
#     cuisine_list = []
#     for i in range(num_rows):
#         cuisine_list.append(cuisine)

#     # add this list as a new column to the restaurant-df
#     restaurant_df['cuisine'] = cuisine_list

#     # update the csv file
#     filename = 'restaurant_records/' + cuisine + '_restaurant_records.csv'
#     restaurant_df.to_csv(filename, index=False)


#---------------dropping unknown values rows from the data
#---------------will assess if I need to drop these

# # identifying rows that have unknown values
# cols = african_restaurants_df.columns
# rows_to_drop = []
# for col in cols:
#     rows_unknow_val = list(african_restaurants_df[african_restaurants_df[col] == 'Value Unknown'].index)
#     rows_to_drop += rows_unknow_val
# rows_to_drop = list(set(rows_to_drop))

# # drop rows with unknown values
# dropped_unknown_df = african_restaurants_df.drop(index=rows_to_drop).reset_index().drop(columns='index')
