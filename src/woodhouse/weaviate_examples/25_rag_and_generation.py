#!/usr/bin/env python3
"""
Weaviate RAG and Generation Examples
===================================
Demonstrates Retrieval-Augmented Generation (RAG) capabilities using
Weaviate's integrated generative features. Perfect for showing AI-powered
content generation based on retrieved context.
"""

import weaviate
from weaviate.classes.generate import GenerativeConfig
from weaviate.classes.config import Configure
import os

def demonstrate_rag():
    # Connect to Weaviate
    client = weaviate.connect_to_local(
        headers={
            "X-OpenAI-Api-Key": os.environ.get("OPENAI_API_KEY", "your-key-here")
        }
    )

    try:
        collection = client.collections.use("Article")

        print("🤖 WEAVIATE RAG DEMONSTRATIONS")
        print("=" * 50)

        # 1. SINGLE PROMPT GENERATION
        print("\n1️⃣ SINGLE PROMPT GENERATION")
        print("Generate a response for each retrieved object")
        print("-" * 40)

        response = collection.generate.near_text(
            query="artificial intelligence in healthcare",
            single_prompt="Summarize this article in one sentence and explain why it's relevant to modern healthcare: {title} - {body}",
            limit=2
        )

        for obj in response.objects:
            print(f"📄 Original: {obj.properties['title']}")
            print(f"🤖 Generated: {obj.generative.text}")
            print()

        # 2. GROUPED GENERATION
        print("\n2️⃣ GROUPED GENERATION")
        print("Generate a single response based on multiple objects")
        print("-" * 40)

        response = collection.generate.near_text(
            query="technology trends",
            grouped_task="Based on these articles, write a brief report on current technology trends and their potential impact on society. Include key themes and future predictions.",
            limit=3
        )

        print("🤖 TECHNOLOGY TRENDS REPORT:")
        print(response.generative.text)
        print()

        # 3. CUSTOM GENERATION WITH SPECIFIC MODEL
        print("\n3️⃣ CUSTOM GENERATION WITH SPECIFIC MODEL")
        print("-" * 40)

        response = collection.generate.near_text(
            query="climate change research",
            single_prompt="Create a compelling headline and brief summary for this research: {title} - {body}",
            generative_provider=GenerativeConfig.openai(
                model="gpt-4",
                temperature=0.7
            ),
            limit=2
        )

        for obj in response.objects:
            print(f"📄 Original: {obj.properties['title']}")
            print(f"✨ Generated Content:")
            print(obj.generative.text)
            print()

        # 4. STRUCTURED GENERATION
        print("\n4️⃣ STRUCTURED GENERATION")
        print("Generate structured content with specific formatting")
        print("-" * 40)

        structured_prompt = """
        Based on this article, create a structured analysis:

        TITLE: {title}
        AUTHOR: {author}
        CATEGORY: {category}

        ANALYSIS:
        - Main Topic: [extract the primary subject]
        - Key Insights: [list 2-3 main points]
        - Target Audience: [who would benefit from this]
        - Relevance Score (1-10): [rate current relevance]

        Content: {body}
        """

        response = collection.generate.near_text(
            query="scientific research",
            single_prompt=structured_prompt,
            limit=1
        )

        for obj in response.objects:
            print("📋 STRUCTURED ANALYSIS:")
            print(obj.generative.text)
            print()

        # 5. COMPARATIVE ANALYSIS
        print("\n5️⃣ COMPARATIVE ANALYSIS")
        print("Compare and contrast multiple articles")
        print("-" * 40)

        response = collection.generate.near_text(
            query="innovation technology",
            grouped_task="""
            Analyze these articles and provide:
            1. Common themes across all articles
            2. Unique perspectives each article brings
            3. Potential contradictions or debates
            4. Overall conclusion about the state of innovation

            Format your response with clear sections and bullet points.
            """,
            limit=4
        )

        print("📊 COMPARATIVE ANALYSIS:")
        print(response.generative.text)
        print()

        # 6. QUESTION ANSWERING
        print("\n6️⃣ QUESTION ANSWERING")
        print("Answer specific questions based on retrieved content")
        print("-" * 40)

        questions = [
            "What are the main benefits of AI in healthcare?",
            "How is renewable energy technology evolving?",
            "What challenges does climate change present?"
        ]

        for question in questions:
            response = collection.generate.near_text(
                query=question,
                single_prompt=f"Answer this question based on the article content: '{question}'. Use information from: {{title}} - {{body}}",
                limit=1
            )

            print(f"❓ Q: {question}")
            if response.objects:
                print(f"🤖 A: {response.objects[0].generative.text}")
                print(f"📄 Source: {response.objects[0].properties['title']}")
            else:
                print("🤖 A: No relevant articles found.")
            print()

        # 7. CREATIVE GENERATION
        print("\n7️⃣ CREATIVE GENERATION")
        print("Create engaging content based on technical articles")
        print("-" * 40)

        response = collection.generate.near_text(
            query="artificial intelligence machine learning",
            single_prompt="""
            Transform this technical article into an engaging social media post:
            - Create a catchy hook
            - Highlight the most interesting aspect
            - Add relevant hashtags
            - Keep it under 200 characters

            Article: {title} by {author}
            Content: {body}
            """,
            limit=1
        )

        for obj in response.objects:
            print(f"📄 Source: {obj.properties['title']}")
            print("📱 Social Media Post:")
            print(obj.generative.text)
            print()

    except Exception as e:
        print(f"❌ Error during RAG demonstration: {e}")

    finally:
        client.close()

if __name__ == "__main__":
    demonstrate_rag()
