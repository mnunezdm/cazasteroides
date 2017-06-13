import requests
from flask import jsonify

result = []
for x in range(0, 100):
    dictionary = {
        "user_info": {
            "_id": x+6101
        },
        "vote_info": {
            "karma_level": 5,
            "vote_type": True
        },
        "observation_info": {
            "_id": str(x+231129),
            "image_id": str(x+3124113),
            "votes": {
                "upvotes":0,
                "downvotes":0
            },
            "position": {
                "x": 12,
                "y": 15
            }
        }
    }

    response = requests.post("http://localhost:5000/v1/validate", json=dictionary)

    jsoned = response.json()
    result.append(jsoned['time'])

    print('Observation {} time {} ns'.format(x, jsoned['time']))

print(sum(result)/len(result))
