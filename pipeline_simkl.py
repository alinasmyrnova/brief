import requests
import pandas as pd
import sqlite3

response = requests.get("https://api.simkl.com/movies/trending/?extended=overview,theater,metadata,tmdb,genres&client_id=efafd58c88fce887a56526ee9f06389f3d572f5d131ea235d6db8debf38be633")
data = response.json ()


extracted_data = []

for movie in data:
    extracted_data.append({
        'title': movie['title'],
        'release_date': movie['release_date'],
        'country': movie['country'],
        'genres': ', '.join(movie['genres']),
        'imdb_rate': movie['ratings']['imdb']['rating'],
        'simkl_rate': movie['ratings']['simkl']['rating'],
        'runtime': movie['runtime'],
        'watched': movie['watched']
    })

# Create DataFrame
df = pd.DataFrame(extracted_data)
print(df.head())

# Transform

# Filling missing values 
df ['imdb_rate'].fillna ('NaN', inplace = True)
df ['runtime'].fillna ('NaN', inplace = True)

# Transform to float
df['imdb_rate'] = pd.to_numeric(df['imdb_rate'], errors='coerce') 

#Transform date and create new column
df['release_date']= pd.to_datetime(df['release_date'])
df['release_year'] = df['release_date'].dt.year

# Convert runtime to float
time_extract = df['runtime'].str.extract(r'(\d+)h\s*(\d+)m')
df['runtime'] = pd.to_numeric(time_extract[0]) * 60 + pd.to_numeric(time_extract[1])


# Load

df.to_csv("./movies_simkl.csv")
connection = sqlite3.connect("./db")
df.to_sql("movies_simkl", connection, if_exists="replace")