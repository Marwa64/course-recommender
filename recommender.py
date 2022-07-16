import random

import numpy as np
import pandas as pd
import warnings

from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

from database_connection import get_database


def recommend_course(skill, user_id):
    dbname = get_database()
    ratings = []
    courses = []
    recommended = []

    ratingsdb = dbname["ratings"]
    rat = ratingsdb.find()

    coursesdb = dbname["courses"]
    cou = coursesdb.find()


    for item in rat:
        ratings.append({
            "rating": item["rating"],
            "user_id": item["user_id"],
            "course_id": item["course_id"],

        })

    for item in cou:
        courses.append({
            "course_id": item["course_id"],
            "skill": item["skill"],
            "course_name": item["course_name"],
            "course_url": item["course_url"],

        })

    user = dbname["users"].find_one({"user_id": user_id})


    if user['course_rated'] < 4:
        for i in range(9):
            recommended.append(random.choice(courses))

    else:
        warnings.simplefilter(action='ignore', category=FutureWarning)
        ratingsdf = pd.DataFrame(ratings)
        coursesdf = pd.DataFrame(courses)

        X, user_mapper, course_mapper, user_inv_mapper, course_inv_mapper = create_matrix(ratingsdf)



        course_titles = dict(zip(coursesdf['course_id'], coursesdf['course_name']))
        course_id = "62cf49457510c13118c1e0c0"

        similar_ids = find_similar_courses(course_id, X, course_mapper,course_inv_mapper,k=8)
        course_title = course_titles[course_id]


        print(f"Since you watched {course_title}")
        for i in similar_ids:
            item = list(filter(lambda item: item['course_id'] == i, courses))
            recommended.append(item)

    return recommended








def create_matrix(df):

    N = len(df['user_id'].unique())
    M = len(df['course_id'].unique())

    # Map Ids to indices
    user_mapper = dict(zip(np.unique(df["user_id"]), list(range(N))))
    course_mapper = dict(zip(np.unique(df["course_id"]), list(range(M))))

    # Map indices to IDs
    user_inv_mapper = dict(zip(list(range(N)), np.unique(df["user_id"])))
    course_inv_mapper = dict(zip(list(range(M)), np.unique(df["course_id"])))

    user_index = [user_mapper[i] for i in df['user_id']]
    course_index = [course_mapper[i] for i in df['course_id']]

    X = csr_matrix((df["rating"], (course_index, user_index)), shape=(M, N))

    return X, user_mapper, course_mapper, user_inv_mapper, course_inv_mapper


def find_similar_courses(course_id, X,course_mapper,course_inv_mapper, k, metric='cosine', show_distance=False):

        neighbour_ids = []

        course_ind = course_mapper[course_id]
        course_vec = X[course_ind]
        k += 1
        kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
        kNN.fit(X)
        course_vec = course_vec.reshape(1, -1)
        neighbour = kNN.kneighbors(course_vec, return_distance=show_distance)
        for i in range(0, k):
            n = neighbour.item(i)
            neighbour_ids.append(course_inv_mapper[n])
        neighbour_ids.pop(0)
        return neighbour_ids

recommend_course("HTML & CSS","6263e194ccf66436915510a7")
