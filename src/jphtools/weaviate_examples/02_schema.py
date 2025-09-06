import weaviate
import os

client = weaviate.Client(
    os.environ["WEAVIATE_URL"],
    auth_client_secret=weaviate.AuthApiKey(os.environ["WEAVIATE_API_KEY"]),
)

schema = {
    "classes": [
        {
            "class": "Question",
            "description": "A question from a user",
            "properties": [
                {
                    "name": "question",
                    "dataType": ["text"],
                    "description": "The question itself",
                },
                {
                    "name": "answer",
                    "dataType": ["text"],
                    "description": "The answer to the question",
                },
            ],
        }
    ]
}

client.schema.create(schema)

print("Schema created!")
