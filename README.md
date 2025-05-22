# HackerNews Digest Podcasts

This script generates an AI-powered podcast that summarizes the top 30 discussions on HackerNews. The podcast features a conversation between two AI voices discussing trending tech topics and community insights.

## Features

- Fetches the top 30 stories from HackerNews API
- Extracts key discussion points from comments
- Generates a conversational podcast transcript
- Converts the transcript to audio using AI voices
- Saves both raw content, transcript, and audio files

## Requirements

- Python 3.8+
- Required Python packages (see `requirements.txt`)
- OpenRouter API key (for LLM access)

## Setup

1. Clone this repository
2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your API keys:

```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## Usage

Run the script to generate a podcast:

```bash
source .venv/bin/activate  # Activate virtual environment
python main.py
```

The script will:

1. Fetch the top 30 stories from HackerNews
2. Process the stories and comments
3. Generate a podcast transcript
4. Convert the transcript to audio
5. Save the output files in the `data` directory

## Output Files

- Raw content: `data/raw/hn_digest_YYYY-MM-DD.txt`
- Transcript: `data/transcripts/transcript_[uuid].txt`
- Audio: `data/audio/podcast_[uuid].mp3`

## Customisation

You can modify the podcast generation parameters in `main.py`:

- `word_count`: Controls the length of the podcast
- `conversation_style`: Adjusts the tone and style
- `roles_person1` and `roles_person2`: Defines the speakers' personas
- `dialogue_structure`: Changes the podcast structure
- `tts_model`: Changes the text-to-speech model

## Credits

- Uses [Podcastfy](https://github.com/souzatharsis/podcastfy) for podcast generation
- Data sourced from [HackerNews API](https://github.com/HackerNews/API)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

