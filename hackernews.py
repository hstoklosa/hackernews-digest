#!/usr/bin/env python3

import requests
import json
import time
import sys
import os
from typing import Dict, List, Any, Optional

def get_item(item_id: int) -> Optional[Dict[str, Any]]:
    """Fetch a Hacker News item by its ID."""
    url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_comments(comment_ids: List[int], indent: int = 0) -> List[Dict[str, Any]]:
    """Recursively fetch all comments for a given list of comment IDs."""
    comments = []
    for comment_id in comment_ids:
        comment = get_item(comment_id)
        if comment is None:
            continue
        
        # Skip deleted or dead comments
        if comment.get('deleted') or comment.get('dead'):
            continue
            
        comment['indent'] = indent
        comments.append(comment)
        
        # Recursively get replies if they exist
        if 'kids' in comment:
            replies = get_comments(comment['kids'], indent + 1)
            comments.extend(replies)
        
        # Be nice to the API
        time.sleep(0.1)
    
    return comments

def format_comment(comment: Dict[str, Any]) -> str:
    """Format a comment for text output."""
    indent = "  " * comment['indent']
    author = comment.get('by', '[deleted]')
    text = comment.get('text', '')
    if text:
        # Remove HTML tags (very basic implementation)
        text = text.replace('<p>', '\n\n').replace('</p>', '')
        for tag in ['<i>', '</i>', '<b>', '</b>', '<code>', '</code>']:
            text = text.replace(tag, '')
        text = text.replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&')
    
    return f"{indent}@{author}:\n{indent}{text}\n"

def save_discussion(story_id: int, output_file: str) -> None:
    """Fetch a Hacker News discussion and save it to a text file."""
    print(f"Fetching story {story_id}...")
    story = get_item(story_id)
    
    if not story:
        print(f"Error: Could not fetch story {story_id}")
        return
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write story details
        title = story.get('title', 'Untitled')
        url = story.get('url', '')
        author = story.get('by', 'Unknown')
        score = story.get('score', 0)
        time_posted = time.ctime(story.get('time', 0))
        
        f.write(f"Title: {title}\n")
        if url:
            f.write(f"URL: {url}\n")
        f.write(f"By: {author}\n")
        f.write(f"Score: {score}\n")
        f.write(f"Posted: {time_posted}\n")
        
        if 'text' in story:
            f.write(f"\n{story['text']}\n")
        
        f.write("\n" + "-" * 80 + "\n\n")
        
        # Write comments
        if 'kids' in story:
            print(f"Fetching {len(story['kids'])} top-level comments and their replies...")
            comments = get_comments(story['kids'])
            print(f"Total comments fetched: {len(comments)}")
            
            for comment in comments:
                f.write(format_comment(comment))
        
    print(f"Discussion saved to {output_file}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <story_id> [output_file]")
        print("Example: python main.py 34404741 discussion.txt")
        return
    
    story_id = int(sys.argv[1])
    output_file = sys.argv[2] if len(sys.argv) > 2 else f"hn_{story_id}.txt"
    
    save_discussion(story_id, output_file)

if __name__ == "__main__":
    main()
