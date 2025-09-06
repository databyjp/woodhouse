import weaviate
import os

client = weaviate.Client(
    os.environ["WEAVIATE_URL"],
    auth_client_secret=weaviate.AuthApiKey(os.environ["WEAVIATE_API_KEY"]),
)

print("Client created!")
