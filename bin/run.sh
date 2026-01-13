docker run --env-file ./.env.secrets --mount type=bind,source="$(pwd)/output_docker",target=/src/output craftsmanadam/ai-news-feed:latest
