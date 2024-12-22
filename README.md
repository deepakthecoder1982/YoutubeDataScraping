# YouTube Data Scraper

This repository contains a Python-based application designed to scrape data from YouTube videos, including captions. The script dynamically fetches the top 500 videos for any specified genre using the YouTube API, extracting metadata and saving it into a CSV file.

## Features

- **Dynamic Genre Input**: Accepts any genre or search term dynamically at runtime, ensuring flexibility during evaluation.
- **Video Metadata Extraction**: Gathers the following details for each video:
  - Video URL
  - Title
  - Description
  - Channel Title
  - Keyword Tags
  - YouTube Video Category
  - Topic Details
  - Video Published At
  - Video Duration
  - View Count
  - Comment Count
  - Captions Available (true/false)
  - Caption Text
  - Location of Recording
- **Captions Handling**: If captions are available, they are fetched and included in the CSV file.

## Assignment Requirements Addressed

1. **Dynamic Genre Support**: 
   - The script prompts the user for a genre or search term at runtime, ensuring no manual intervention is needed to change the input.
2. **Top 500 Videos**:
   - Fetches up to 500 videos for the specified genre or search term.
   - Uses pagination to ensure comprehensive data collection.
3. **CSV Export**:
   - All collected data points are saved into a CSV file for easy review and submission.

## Dependencies

The script uses the following libraries:
- `googleapiclient`: To interact with the YouTube Data API.
- `youtube_transcript_api`: To fetch captions for videos.
- `csv`: To save the extracted data in CSV format.
- `os`: For file handling.
- `requests`: For making API requests.

Install the dependencies using:
```bash
pip install -r requirements.txt
```

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/youtube-data-scraper.git
   cd youtube-data-scraper
   ```
2. Replace the placeholder in the script with your YouTube Data API Key:
   ```python
   API_KEY = "YOUR_API_KEY"
   ```
3. Run the script:
   ```bash
   python main.py
   ```
4. Enter the genre or search term when prompted:
   ```text
   Enter a genre or search term: music
   ```
5. The script will fetch the data and save it in a CSV file named `youtube_videos.csv`.

## Output

The script generates a `youtube_videos.csv` file with the following columns:
- Video URL
- Title
- Description
- Channel Title
- Keyword Tags
- YouTube Video Category
- Topic Details
- Video Published At
- Video Duration
- View Count
- Comment Count
- Captions Available
- Caption Text
- Location of Recording

## Limitations

- **YouTube API Quotas**: The script depends on the YouTube API and is subject to daily quota limits.
- **Runtime**: Fetching 500 videos can take several minutes depending on API response times and network connectivity.
- **Captions Availability**: Not all videos have captions, and in some cases, captions might not be available in English.

## Submission Guidelines

To submit the assignment:
1. Run the script for the specified genre.
2. Submit the generated `youtube_videos.csv` file with all the required data points.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Thanks to YouTube for providing API access.
- Inspired by the requirements of the Data Scraping Internship assignment.
