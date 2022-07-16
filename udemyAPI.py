from bson import ObjectId
from udemy import *
import json
from database_connection import get_database

dbname = get_database()

skillsdb = dbname["skills"]
coursesdb = dbname["courses"]
s = skillsdb.find()
skills = []
for item in s:
    skills.append(item["name"])

print(skills)
Client = PyUdemy(clientID = 'fXD21XVH7riyVu0jI3e9mXOvJgdS4uuxweSF9kFX',
                 clientSecret = 'FKxepGFQz0tynFnh8xbqK2kWiUhXr2DXvfaI86HXIF808BYHbPu3YxsmQ2z8C4jsBBZigD0hJegFKw9hiVLzypNkf0FblcnXBWDBLPs0LHagXRKOtuMdVx9noDndBVOU')



for skill in skills:
    courses_list = Client.get_courseslist(page_size=50, search=skill)
    courses = json.loads(courses_list)
    for result in courses['results']:
        course_detail = Client.get_coursesreviewlist(courseID = result['id'])
        course = json.loads(course_detail)
        name = result['title']
        url = "https://www.udemy.com"+result['url']
        o = ObjectId()
        sk = []
        sk.append(skill)

        course = {
        "_id" : o,
        "course_id" : str(o),
        "course_name" : name,
        "skills" : sk,
        "course_url" : url
        }

        count = coursesdb.count_documents({"course_url":url})



        if(count>0):
            c = coursesdb.find_one({"course_url": url})
            c["skills"].append(skill)
            print(c)
            coursesdb.update_one({"course_url": url},{"$set": c })
            continue

        else:
            print(url)
            coursesdb.insert_one(course)
