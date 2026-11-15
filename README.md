# Object Detection & Cloud Archiving Pipeline

Hi! I recently graduated with a B.Sc. (Hons) in Computing and Automation Engineering. I built this project to get hands-on experience integrating classical computer vision with a modern cloud backend. 

This application acts like a smart security camera. It processes a video feed to detect motion, tracks the moving objects, and automatically uploads the event footage to AWS S3, logs the data to a PostgreSQL database, and pings my phone with an alert.

## Why I Built It & How It Works

I wanted to build an end-to-end system rather than just a standalone script. Here is how the different parts work together:

*   Computer Vision (OpenCV): Instead of using a heavy machine learning model, I used classical CV (MOG2 background subtraction and contour detection). This keeps the program lightweight so it can run smoothly on standard hardware. I also added polygon masking (`cv.fillPoly`) to only track motion in specific areas (like a fence line) and custom mathematical logic (speed/displacement) to filter out false positives like leaves or bugs.
*   Cloud Storage & Alerts (AWS S3 & Webhooks): When a real threat is detected, the clip is uploaded to an S3 bucket. Knowing that synchronous cloud uploads would block the main thread and freeze the live video feed, I designed the system using Python's threading module to handle I/O tasks in the background. Once uploaded, the background thread automatically fires a Discord webhook, sending a real-time security alert with a secure presigned URL directly to my phone.
*   Database (Neon PostgreSQL & SQLAlchemy): Every time an event happens, the timestamp and the S3 video link are logged into a cloud database. I used SQLAlchemy to cleanly handle the database sessions, specifically utilizing connection pooling (`pool_pre_ping=True`) to ensure the cloud database connection doesn't drop when idle.
*   Environment Variables: All AWS credentials and database URLs are hidden in a `.env` file to keep the repository secure.

## Tech Stack
*   Language: Python 3
*   Libraries: OpenCV, NumPy, SQLAlchemy, Boto3, Requests, python-dotenv
*   Infrastructure: AWS S3, Neon (Serverless PostgreSQL)

## How to Run It Locally

If you want to clone this and try it yourself, here are the steps:

1. Clone the repository and set up a virtual environment:
```bash
git clone [https://github.com/ilise15/objectDetection.git](https://github.com/ilise15/objectDetection.git)
cd objectDetection
python -m venv .venv

# Activate the virtual environment
# On Windows: .venv\Scripts\activate
# On Mac/Linux: source .venv/bin/activate
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your Environment Variables:
Create a `.env` file in the root directory and add your unique credentials:
```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_BUCKET_NAME=your_bucket_name
DATABASE_URL=postgresql://user:password@your-neon-host.com/dbname
DISCORD_WEBHOOK_URL=[https://discord.com/api/webhooks/your_webhook_id](https://discord.com/api/webhooks/your_webhook_id)
```

4. Run the application:
```bash
python main.py
```