# slide_extractor
A python script to extract slides from a presentation video. This script was originally written to extract slides from the videos of a course, whose instructor refused to share the slides and had very long videos, which I was so lazy to watch. Notes were allowed in exams. So, had to come up with this script to make a pdf of the slides from the video. It's best used with a video scraping script.

## Usage
Install Requirements
`pip3 install -r requirements.txt`
Run script for a video file
`python3 main.py video.mp4`

## Implementation details
This script uses OpenCV to parse videos. Each frame is compared with the previous frame using a simmilarity score (from sklearn). If the two consecutive frames are similar, skip this frame, otherwise save the frame as an image. Next compare each saved frame with every other frame and remove furthur duplicates. Finally from the ramaining frames, make a pdf and remove the jpg files.
