#!/usr/bin/env python3
"""
Quick Weaviate Setup with Sample Data
=====================================
A complete starter script that connects to Weaviate, creates a collection,
and adds sample data. Perfect for demos and getting started quickly.
"""

import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure, Property, DataType
import os

def main():
    # Connect to Weaviate (modify connection as needed)
    client = weaviate.connect_to_local(
        headers={
            "X-OpenAI-Api-Key": os.environ.get("OPENAI_API_KEY", "your-key-here")
        }
    )

    try:
        # Create a simple Article collection
        collection_name = "Article"

        # Delete if exists (for clean demos)
        if client.collections.exists(collection_name):
            client.collections.delete(collection_name)

        # Create collection with vectorizer
        client.collections.create(
            collection_name,
            vector_config=Configure.Vectors.text2vec_openai(),
            properties=[
                Property(name="title", data_type=DataType.TEXT),
                Property(name="body", data_type=DataType.TEXT),
                Property(name="category", data_type=DataType.TEXT),
                Property(name="author", data_type=DataType.TEXT),
                Property(name="publication_date", data_type=DataType.DATE),
                Property(name="word_count", data_type=DataType.INT),
                Property(name="is_published", data_type=DataType.BOOL),
            ]
        )

        collection = client.collections.use(collection_name)

        # Sample articles for demonstration
        sample_articles = [
            {
                "title": "Introduction to Artificial Intelligence",
                "body": "Artificial Intelligence (AI) is revolutionizing how we approach complex problems. From machine learning to neural networks, AI technologies are transforming industries worldwide.",
                "category": "Technology",
                "author": "Dr. Sarah Johnson",
                "publication_date": "2024-01-15T00:00:00Z",
                "word_count": 1500,
                "is_published": True
            },
            {
                "title": "The Future of Renewable Energy",
                "body": "Solar and wind energy are becoming increasingly cost-effective. This article explores the latest developments in renewable energy technology and their impact on global sustainability.",
                "category": "Environment",
                "author": "Michael Chen",
                "publication_date": "2024-02-20T00:00:00Z",
                "word_count": 2200,
                "is_published": True
            },
            {
                "title": "Modern Web Development Practices",
                "body": "From React to TypeScript, modern web development has evolved significantly. Learn about the latest frameworks and best practices for building scalable web applications.",
                "category": "Technology",
                "author": "Emma Rodriguez",
                "publication_date": "2024-03-10T00:00:00Z",
                "word_count": 1800,
                "is_published": True
            },
            {
                "title": "Climate Change and Ocean Ecosystems",
                "body": "Rising ocean temperatures are affecting marine biodiversity. This research examines the correlation between climate change and oceanic ecosystem health.",
                "category": "Science",
                "author": "Dr. James Wilson",
                "publication_date": "2024-01-30T00:00:00Z",
                "word_count": 2500,
                "is_published": False
            },
            {
                "title": "Machine Learning in Healthcare",
                "body": "AI-powered diagnostic tools are improving patient outcomes. Explore how machine learning algorithms are being used to detect diseases earlier and more accurately.",
                "category": "Healthcare",
                "author": "Dr. Lisa Park",
                "publication_date": "2024-03-25T00:00:00Z",
                "word_count": 1900,
                "is_published": True
            }
        ]

        # Insert sample data using batch
        with collection.batch.fixed_size(batch_size=10) as batch:
            for article in sample_articles:
                batch.add_object(properties=article)

        print(f"✅ Successfully created '{collection_name}' collection with {len(sample_articles)} sample articles")
        print("🔍 Ready for search demonstrations!")

        # Quick test search
        response = collection.query.near_text(
            query="artificial intelligence",
            limit=2,
            return_properties=["title", "author"]
        )

        print("\n📝 Sample search results for 'artificial intelligence':")
        for obj in response.objects:
            print(f"  - {obj.properties['title']} by {obj.properties['author']}")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        client.close()

if __name__ == "__main__":
    main()
