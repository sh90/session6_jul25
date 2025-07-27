# pip install newspaper3k lxml_html_clean
"""
An RSS feed (Really Simple Syndication) is a type of web feed that allows users and applications to receive updates
to websites in a standardized, computer-readable format.

Here’s a breakdown of how it works:

Publishers (like blogs, news sites, or podcasts) create an RSS feed — an XML file containing summaries or full content of their latest updates.

Users subscribe to that feed using an RSS reader (such as Feedly, Inoreader, or an email client).

The reader periodically checks the feed and shows new content, so users can stay updated without visiting each site individually.

Example Use Case:
You follow 10 blogs. Instead of visiting each site daily, you subscribe to their RSS feeds in one app. That app aggregates all new posts in one place.

Would you like to see an example of what an RSS feed file looks like?

"""
import json

import newspaper
import feedparser
import openai
from openai import OpenAI

import data_info
import certifi
import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

os.environ['SSL_CERT_FILE'] = certifi.where()
openai.api_key = data_info.open_ai_key

# Email credentials
sender_email = "shikhatyagi1990@gmail.com"
receiver_email = "shikhatyagi1990@gmail.com"  # Can be any email address
password = data_info.app_password  # Use an app password, NOT your Gmail password


def scrape_news_from_feed(feed_url):
    articles = []
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        # create a newspaper article object
        article = newspaper.Article(entry.link)
        # download and parse the article
        article.download()
        article.parse()
        # extract relevant information
        articles.append({
            'title': article.title,
            'author': article.authors,
            'publish_date': article.publish_date,
            'content': article.text
        })
    return articles


feed_url = 'http://feeds.bbci.co.uk/news/rss.xml'
articles = scrape_news_from_feed(feed_url)
print(articles)
# print the extracted articles
for article in articles[0:1]:
    print('Title:', article['title'])
    print('Author:', article['author'])
    print('Publish Date:', article['publish_date'])
    print('Content:', article['content'])

    # Analyze sentiment
    analyze_sentiment_prompt = f"""

    You are an expert news analyst and your task is to identify company names and do sentiment analysis.
    Analyze the news article given below. 

     News Article: {article['content']}

     Format the response in a friendly format which can be sent via email.

    Output Format: 
    Generate a plain json object with two keys "subject" and "body" subject will contain the subject of the email message and "body" body will contain the body of the email message.
    In the body, keep Sender name as Shikha Tyagi,

    """
    client = OpenAI(api_key=data_info.open_ai_key)
    response = client.responses.create(
        model="gpt-4o-mini",
        input=analyze_sentiment_prompt,
        temperature=0,
    )

    print(response.output_text)
    final_response = response.output_text.split("{")[1].split("}")[0]
    final_response = json.loads("{" + final_response + "}")
    # Email content
    print(final_response)
    subject = final_response["subject"]
    body = final_response["body"]

    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    # Send the email via Gmail's SMTP server
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)
