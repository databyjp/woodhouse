#!/usr/bin/env python3
"""
Weaviate Search Methods Demonstration
====================================
Comprehensive examples of different search types: semantic, keyword, hybrid,
and filtered searches. Perfect for demonstrating search capabilities.
"""

import weaviate
from weaviate.classes.query import Filter, MetadataQuery, HybridFusion
import os

def demonstrate_searches():
    # Connect to Weaviate
    client = weaviate.connect_to_local(
        headers={
            "X-OpenAI-Api-Key": os.environ.get("OPENAI_API_KEY", "your-key-here")
        }
    )

    try:
        collection = client.collections.use("Article")

        print("🔍 WEAVIATE SEARCH DEMONSTRATIONS")
        print("=" * 50)

        # 1. SEMANTIC SEARCH (Vector-based)
        print("\n1️⃣ SEMANTIC SEARCH with near_text")
        print("-" * 40)

        response = collection.query.near_text(
            query="machine learning and artificial intelligence",
            limit=3,
            return_metadata=MetadataQuery(distance=True),
            return_properties=["title", "category", "author"]
        )

        for obj in response.objects:
            print(f"📄 {obj.properties['title']}")
            print(f"   Category: {obj.properties['category']} | Author: {obj.properties['author']}")
            print(f"   Distance: {obj.metadata.distance:.4f}")
            print()

        # 2. KEYWORD SEARCH (BM25)
        print("\n2️⃣ KEYWORD SEARCH with BM25")
        print("-" * 40)

        response = collection.query.bm25(
            query="renewable energy solar wind",
            query_properties=["title", "body"],
            limit=3,
            return_metadata=MetadataQuery(score=True),
            return_properties=["title", "category", "word_count"]
        )

        for obj in response.objects:
            print(f"📄 {obj.properties['title']}")
            print(f"   Category: {obj.properties['category']} | Words: {obj.properties['word_count']}")
            print(f"   BM25 Score: {obj.metadata.score:.4f}")
            print()

        # 3. HYBRID SEARCH (Combines semantic + keyword)
        print("\n3️⃣ HYBRID SEARCH (Semantic + Keyword)")
        print("-" * 40)

        response = collection.query.hybrid(
            query="healthcare AI technology",
            alpha=0.5,  # 50/50 balance between semantic and keyword
            fusion_type=HybridFusion.RELATIVE_SCORE,
            limit=3,
            return_metadata=MetadataQuery(score=True, explain_score=True),
            return_properties=["title", "category", "author"]
        )

        for obj in response.objects:
            print(f"📄 {obj.properties['title']}")
            print(f"   Category: {obj.properties['category']} | Author: {obj.properties['author']}")
            print(f"   Hybrid Score: {obj.metadata.score:.4f}")
            print(f"   Score Explanation: {obj.metadata.explain_score}")
            print()

        # 4. FILTERED SEARCH
        print("\n4️⃣ FILTERED SEARCH with Conditions")
        print("-" * 40)

        response = collection.query.near_text(
            query="technology innovation",
            filters=(
                Filter.by_property("category").equal("Technology") &
                Filter.by_property("word_count").greater_than(1000) &
                Filter.by_property("is_published").equal(True)
            ),
            limit=5,
            return_properties=["title", "author", "word_count", "publication_date"]
        )

        print("🎯 Technology articles > 1000 words, published:")
        for obj in response.objects:
            print(f"📄 {obj.properties['title']}")
            print(f"   Author: {obj.properties['author']} | Words: {obj.properties['word_count']}")
            print(f"   Published: {obj.properties['publication_date']}")
            print()

        # 5. COMPLEX FILTERING
        print("\n5️⃣ COMPLEX FILTERING (Multiple Conditions)")
        print("-" * 40)

        response = collection.query.fetch_objects(
            filters=(
                Filter.by_property("category").contains_any(["Technology", "Science"]) |
                (Filter.by_property("word_count").greater_than(2000) &
                 Filter.by_property("author").like("Dr.*"))
            ),
            limit=10,
            return_properties=["title", "category", "author", "word_count"]
        )

        print("🔍 Tech/Science articles OR (>2000 words + Doctor authors):")
        for obj in response.objects:
            print(f"📄 {obj.properties['title']}")
            print(f"   {obj.properties['category']} | {obj.properties['author']} | {obj.properties['word_count']} words")
            print()

        # 6. SEARCH WITH METADATA
        print("\n6️⃣ SEARCH WITH DETAILED METADATA")
        print("-" * 40)

        response = collection.query.near_text(
            query="research development",
            limit=2,
            return_metadata=MetadataQuery(
                distance=True,
                score=True,
                creation_time=True
            ),
            return_properties=["title", "author"]
        )

        for obj in response.objects:
            print(f"📄 {obj.properties['title']}")
            print(f"   Author: {obj.properties['author']}")
            print(f"   Distance: {obj.metadata.distance:.4f}")
            print(f"   Created: {obj.metadata.creation_time}")
            print()

    except Exception as e:
        print(f"❌ Error during search demonstration: {e}")

    finally:
        client.close()

if __name__ == "__main__":
    demonstrate_searches()
