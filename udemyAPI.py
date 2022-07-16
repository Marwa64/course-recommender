from bson import ObjectId
from udemy import *
import json

from database_connection import get_database

skills = ["HTML & CSS","Javascript","Hacking","networks"]
Client = PyUdemy(clientID = 'fXD21XVH7riyVu0jI3e9mXOvJgdS4uuxweSF9kFX',
                 clientSecret = 'FKxepGFQz0tynFnh8xbqK2kWiUhXr2DXvfaI86HXIF808BYHbPu3YxsmQ2z8C4jsBBZigD0hJegFKw9hiVLzypNkf0FblcnXBWDBLPs0LHagXRKOtuMdVx9noDndBVOU')

dbname = get_database()

courses = dbname["courses"]

for skill in skills:
    courses_list = Client.get_courseslist(page_size=10, search=skill)
    courses = json.loads(courses_list)
    for result in courses['results']:
        course_detail = Client.get_coursesreviewlist(courseID = result['id'])
        course = json.loads(course_detail)
        name = result['title']
        url = "https://www.udemy.com"+result['url']
        o = ObjectId()

        course = {
        "_id" : o,
        "course_id" : str(o),
        "course_name" : name,
        "skill" : skill,
        "course_url" : url
        }
        courses.insert_one(course)