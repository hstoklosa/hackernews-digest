#!/usr/bin/env python3

import os
import requests
import time
from typing import List, Dict, Any
from datetime import datetime

from podcastfy.client import generate_podcast


def get_top_stories(limit: int = 30) -> List[int]:
    """Fetch the IDs of the top stories from HackerNews."""
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()[:limit]
    return []


def get_item(item_id: int) -> Dict[str, Any]:
    """Fetch a Hacker News item by its ID."""
    url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}


def get_top_comments(story_id: int, limit: int = 5) -> List[Dict[str, Any]]:
    """Fetch top comments for a story."""
    story = get_item(story_id)
    comments = []
    
    if 'kids' in story and story['kids']:
        comment_ids = story['kids'][:limit]
        for comment_id in comment_ids:
            comment = get_item(comment_id)
            if comment and not comment.get('deleted') and not comment.get('dead'):
                comments.append(comment)
            time.sleep(0.1)  # Be nice to the API
    
    return comments


def prepare_podcast_content() -> str:
    """Prepare content for the podcast by fetching and organizing HackerNews data."""
    print("Fetching top stories from HackerNews...")
    top_story_ids = get_top_stories(30)
    
    content = "# HackerNews Daily Digest\n\n"
    content += f"Top discussions on HackerNews for {datetime.now().strftime('%Y-%m-%d')}\n\n"
    
    for i, story_id in enumerate(top_story_ids, 1):
        print(f"Processing story {i}/{len(top_story_ids)}: {story_id}")
        story = get_item(story_id)
        
        if not story:
            continue
            
        # Add story details
        title = story.get('title', 'Untitled')
        url = story.get('url', '')
        author = story.get('by', 'Unknown')
        score = story.get('score', 0)
        
        content += f"## {i}. {title}\n"
        content += f"Score: {score} | By: {author}\n"
        if url:
            content += f"URL: {url}\n"
        
        # Add story text if available
        if 'text' in story and story['text']:
            content += f"\nSummary: {story['text'][:300]}...\n"
        
        # Add top comments
        comments = get_top_comments(story_id)
        if comments:
            content += "\nTop comments:\n"
            for j, comment in enumerate(comments, 1):
                text = comment.get('text', '')
                if text:
                    # Basic HTML tag removal
                    text = text.replace('<p>', ' ').replace('</p>', ' ')
                    for tag in ['<i>', '</i>', '<b>', '</b>', '<code>', '</code>']:
                        text = text.replace(tag, '')
                    text = text.replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&')
                    
                    # Truncate long comments
                    if len(text) > 200:
                        text = text[:200] + "..."
                        
                    content += f"- @{comment.get('by', 'anonymous')}: {text}\n"
        
        content += "\n---\n\n"
        time.sleep(0.2)  # Be nice to the API
    
    return content


def main():
    # Create directories if they don't exist
    os.makedirs("./data/raw", exist_ok=True)
    os.makedirs("./data/audio", exist_ok=True)
    os.makedirs("./data/transcripts", exist_ok=True)
    
    # Generate date-based filenames
    today = datetime.now().strftime("%Y-%m-%d")
    raw_file = f"./data/raw/hn_digest_{today}.txt"
    
    # Prepare content
    print("Preparing podcast content...")
    content = prepare_podcast_content()
    
    # Save raw content
    with open(raw_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Raw content saved to {raw_file}")
    
    # Configure podcast conversation
    conversation_config = {
        "word_count": 4000,  # ~30 minutes of audio
        "conversation_style": ["informative", "conversational"],
        "roles_person1": "Tech Analyst",
        "roles_person2": "Industry Expert",
        "dialogue_structure": [
            "Introduction",
            "Top Stories Overview",
            "Deep Dive: Tech Developments",
            "Deep Dive: Industry News",
            "Community Insights",
            "Emerging Trends",
            "Conclusion"
        ],
        "podcast_name": "HackerNews Daily Digest",
        "podcast_tagline": "Your daily dose of tech conversations",
        "output_language": "English",
        "engagement_techniques": ["debate", "examples", "questions", "analogies"],
        "creativity": 0.4  # Balanced between factual and engaging
    }

    # Generate podcast from the content
    print("Generating podcast...")
    podcast_result = generate_podcast(
        text=content,
        conversation_config=conversation_config,
        llm_model_name="openrouter/openai/gpt-4o-mini",
        api_key_label="OPENROUTER_API_KEY",
        tts_model="edge",  # Using Microsoft Edge TTS for good quality and free usage
    )
    
    print(f"Podcast generated successfully!")
    print(f"Transcript: {podcast_result[0]}")
    print(f"Audio file: {podcast_result[1]}")


if __name__ == "__main__":
    main()
