import uuid
from datetime import datetime
import pymongo
from faker import Faker
import random

client = pymongo.MongoClient("mongodb://localhost:27017/")
client.drop_database('TestMoviesDB')
db = client['TestMoviesDB']

likes_collection = db['likes']
favorites_collection = db['favorites']
comments_collection = db['comments']

fake = Faker()

movie_titles = [fake.sentence(nb_words=3, variable_nb_words=True) for _ in range(10)]

max_users = 100
max_movies = 1000
max_strings = 1

print(client.list_database_names())
users=1
start_time = datetime.now()
print(start_time)
x = 0

users_list = []
while users <= max_users:
    users_list.append(str(uuid.uuid4()))
    users+=1


movies = 1
movies_list = []
while movies <= max_movies:
    movies+=1
    movies_list.append(str(uuid.uuid4()))


for users in users_list:
    user_id = users

    for movies in movies_list:
        movies_id = movies
        likes = 1
        data_likes = []
        while likes<= max_strings:
            likes+=1
            likes_doc ={
                    "user_id": user_id,
                    "movies_id": movies_id,
                    "like": random.randint(0,10)
                }
            data_likes.append(likes_doc)

        favorites = 1
        data_favorites = []
        while favorites<= max_strings:
            favorites+=1
            favorites_doc ={
                    "user_id": user_id,
                    "movies_id": movies_id
                }
            data_favorites.append(favorites_doc)

        comments = 1
        data_comments = []
        max_comments = random.randint(1,4)
        while comments<= max_comments:
            comments+=1
            comments_doc ={
                    "user_id": user_id,
                    "movies_id": movies_id,
                    "comment": fake.text(),
                }
            data_comments.append(comments_doc)
            x += 1

        likes_collection.insert_many(data_likes)
        favorites_collection.insert_many(data_favorites)
        comments_collection.insert_many(data_comments)

    # print(user_id)

end_time = datetime.now()
print(end_time)
print("Время записи")
print("Время чтения")
pipeline = [
    {
        '$group': {
            '_id': {'field1': '$user_id',
                    'field2': '$movies_id'}
        }
    }
]

result = likes_collection.aggregate(pipeline)


pipeline = [
    {
        '$match': {'user_id': users_list[1]}
    },
    {
        '$group': {
            '_id': {'field1': '$user_id',
                    'field2': '$movies_id'},
            'avgValue': {'$avg': "$likes"}
        }
    }
]

start_time = datetime.now()
result = likes_collection.aggregate(pipeline)
end_time = datetime.now()
print(f"список понравившихся пользователю фильмов (список лайков пользователя) = {end_time - start_time} ")

pipeline = [
    {
        '$match': {'movies_id': movies_list[1]}
    },
    {
        '$group': {
            '_id': {'field1': '$movies_id'},
            'avgValue': {'$avg': "$likes"}
        }
    }
]
start_time = datetime.now()
result = likes_collection.aggregate(pipeline)
end_time = datetime.now()
print(f"средняя пользовательская оценка фильма = {end_time - start_time} ")


pipeline = [
    {
        '$match': {'user_id': users_list[1]}
    },
    {
        '$group': {
            '_id': {'field1': '$user_id'},
            'count': {'$sum': 1}
        }
    }
]
start_time = datetime.now()
result = favorites_collection.aggregate(pipeline)
end_time = datetime.now()
print(f"Время запроса список закладок = {end_time - start_time} ")

import threading

test_user_id = str(uuid.uuid4())
data_likes = []
def procedure1():
    likes_doc = {
        "user_id": test_user_id,
        "movies_id": str(uuid.uuid4()),
        "likes": random.randint(0, 10)
    }
    data_likes.append(likes_doc)
    print(f"Время добавления в базу данных = {datetime.now()} ")
    likes_collection.insert_many(data_likes)

def procedure2():
    pipeline = [
        {
            '$match': {'user_id': test_user_id}
        },
        {
            '$group': {
                '_id': {'field1': '$user_id',
                        'field2': '$movies_id'},
                'avgValue': {'$avg': "$likes"}
            }
        }
    ]
    x = 0
    while x == 0:
        result = likes_collection.aggregate(pipeline)
        for post in result:
            print(f"Время появления в запросе = {datetime.now()} ")
            x+=1



thread1 = threading.Thread(target=procedure1)
thread2 = threading.Thread(target=procedure2)

thread1.start()
thread2.start()

thread1.join()
thread2.join()