#!/usr/bin/env python3

import os
from podcastfy.client import generate_podcast

def main():
    input_file = "./data/raw/hn_44044043.txt"
    
    # Check if the file exists
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found!")
        return
    
    print(f"Generating podcast from {input_file}...")
    
    # Read the file content if it's a .txt file
    file_content = None
    if input_file.lower().endswith('.txt'):
        print("Reading text file content...")
        with open(input_file, 'r', encoding='utf-8') as file:
            file_content = file.read()
        print(f"Read {len(file_content)} characters from the file.")
    
    conversation_config = {
        "word_count": 3000,  # Moderate length for discussion
        "conversation_style": ["analytical", "conversational"],
        "roles_person1": "tech enthusiast",
        "roles_person2": "AI researcher",
        "dialogue_structure": ["Topic Introduction", "Key Points", "Analysis", "Implications", "Conclusion"],
        "podcast_name": "HackerNews Insights",
        "podcast_tagline": "Diving Deep into Tech Discussions",
        "output_language": "English",
        "engagement_techniques": ["debate", "examples", "questions"],
        "creativity": 0.4  # Balanced creativity
    }

    # Generate podcast from the local file or its content
    if file_content:
        # Use the file content as a string instead of the file path
        print("Using file content directly...")
        podcast_result = generate_podcast(
            text=file_content,  # Pass content directly as text parameter
            conversation_config=conversation_config,
            llm_model_name="openrouter/openai/gpt-4o-mini",
            api_key_label="OPENROUTER_API_KEY",
            tts_model="edge",
        )
    else:
        # For PDF files, continue using the file path
        podcast_result = generate_podcast(
            urls=[input_file],
            conversation_config=conversation_config,
            llm_model_name="openrouter/openai/gpt-4o-mini",
            api_key_label="OPENROUTER_API_KEY",
            tts_model="edge",
        )
    
    print(f"Podcast generated successfully!")
    print(f"Transcript: {podcast_result[0]}")
    print(f"Audio file: {podcast_result[1]}")

if __name__ == "__main__":
    main()
