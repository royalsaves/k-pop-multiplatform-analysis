# K-Pop Data Analysis Project

This project is focused on analyzing K-Pop data, specifically related to the group NCT. It includes various data sources and scripts to fetch, analyze, and visualize the data.

## Project Structure

- **data/**: Contains all the data files.
  - **youtube/**: Contains CSV files with YouTube video statistics.
    - `video_counts_by_day.csv`: Daily view counts for YouTube videos.
    - `views_by_day.csv`: Total daily views for YouTube videos.
    - `comment_counts_by_day.csv`: Daily comment counts for YouTube videos.
  - **theqoo/**: Contains filtered data related to NCT.
    - `theqoo_nct_all_filtered.csv`: Filtered data related to NCT.
    - `sentiment_by_day.csv`: Daily sentiment analysis results for NCT-related data.
  - **trends/**: Contains Google Trends data.
    - `google_trends_data.csv`: Google Trends data.

- **scripts/**: Contains Python scripts for data processing and analysis.
  - `collect_youtube_data.py`: Script to collect YouTube data.
  - `collect_theqoo_data.py`: Script to collect Theqoo data.
  - `analyze_sentiment_theqoo.py`: Script to analyze sentiment in Theqoo data.
  - `collect_google_trends.py`: Script to collect Google Trends data.
  - `plot_all_results.py`: Script to visualize all results.

- **result/**: Directory for saving analysis results and graphs.

- **requirements.txt**: Lists the required packages for the project.

## Usage

1. Install the required packages using the command:
   ```
   pip install -r requirements.txt
   ```

2. Run the scripts in the `scripts/` directory to fetch and analyze the data.

3. Check the `result/` directory for saved graphs and analysis results.

## Contributing

Feel free to contribute to this project by adding more data sources, improving the analysis scripts, or enhancing the visualizations.