# banksdb api

Api to search indian banks or branches. <br/>
***
## Tech Stack <br/>

1. Django
2. Django Rest framework
3. PostgresDB
4. Redis ( for caching)

## Features

1. Full text search
2. Postgres indexes ( for faster queries, No one hates indexes )
3. Caching ( you know why 🔥🚀)
4. Postgres triggers
5. Pagination ( Your client (frontend) would love you for this)

***

The project uses native full text faetures provided by postgresql. There are two types of full text search 

1. using __search ( by django) for searching on single column.
2. using Search Ranking, Search Vector and Search Query. 

The second full text search ranks the results on the basis of the rank provided by postgres for each result. Greater the rank higher the result will be in result.

For optimizing search queries I have used [GIN indexes](https://www.postgresql.org/docs/9.5/gin-intro.html#:~:text=GIN%20stands%20for%20Generalized%20Inverted,appear%20within%20the%20composite%20items.) over the search column. This made my queries run 2x faster. It's simple to create a GIN index.
```sql
CREATE INDEX INDEX_NAME ON TABLE_NAME USING GIN(COLUMN_NAME)
```
As per postgres docs gin indexes are 2-3x faster than other indexes available in postgres ( GIST and Btree) but uses more space. <br/>
Also I added a trigger to db which will automatically generate a search vetor on any insert or update query
***
## Using the app

1. Set environment variables in a .env file in project root
```
SECRET_KEY
DB_NAME
DB_HOST
DB_USER
DB_PASSWORD
REDIS_HOST
REDIS_PASSWORD
DEBUG
```
2. Add data to your database, get data from [here](https://github.com/snarayanank2/indian_banks)
```shell
psql psql -h DB_HOST -p DB_PORT -U DB_USER -d DB_NAME -f FILENAME.sql
```
You can get the sql file from the above repo

3. Migrate db ( fingers crossed 🤞🏻)
```
python mange.py makemigrations
python manage.py migrate
```
4. Run the server
```
python manage.py runserver
```
5. Run test (Optional)
```
python manage.py test
```
SetUp a local postgres instance for testing and add the credentials in settings.py

***
## Endpoints

1. /api/branches/autocomplete/?q=<search_tern>&offset=<page_number>&limit=<page_size> <br/>
Autocomplete endpoint, searches over the branch column of branches table and returns the result.

2. /api/branches/search/?q=<search_term>&city=<city_name>&offset=<page_number>&limit=<page_size> <br/>
Searches all the db columns in bracnes table in the given city with the given search term.

3. /api/banks/:id <br/>
Returns bank with id :id from the banks table.


***
## Deployment

Freebie Stuff 💁🏻‍♀️🙋‍♀️
1. Heroku ( free, deployed django project there)
2. Clever Cloud ( free postgres add on)
3. Redis labs redis cloud ( free redis instance)

All these things are included in AWS Free tier but i don't want to share my card details 😅 ( I don't have a card 🥲).

***
## Known Issues
1.  Partial word search
Postgres full text search is OP ❤️‍🔥 but it dosen't perform well with partial words. E.g will give no result for eas but will give results for east. <br />
**Solution**
Use something advance like Elasticsearch for full text search or path or write some custom plugin to leverage postgres FTS for partial words.

***
## Improvements
1. Add API docs ( maybe swagger ), due to time constraints I am considering this as future work.


***

## Closing words
I really enjoyed creating this project and learend lot's of new things while creating it.

P.S Today (21 May, 2021) is my bithday 🥳
