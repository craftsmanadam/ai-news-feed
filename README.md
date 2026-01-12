# AI-NEWS-FEED

This project is a "playground" for me to play with pydantic ai.  The goal is simple ... grab the latest AI news from good feeds and make decisions on what is the most important and relative to what I like.  It'll have to collect, dedupe, rank and then summarize.

I'm using docker and make as the main logical unit.

# Development

## Requirements

* dotenv
* direnv (command: direnv allow)
* Make sure you have .env.secrets file with GEMINI_API_KEY defined
