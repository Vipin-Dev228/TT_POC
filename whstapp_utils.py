import requests

ACCESS_TOKEN_1 = "EAATR1HS3QPUBPACI6aC87FkQOImKzlXvNMYJ2Is9FqdCWzd9CuZBbf1urEXBZAgZCUdOqrWq7WUS7ZBP1EaFilksFYGTwPQiNVswXXcOlLoqsYZBIqI96K6IvqUkAllVGvN6SI9CZA758LVJRJnJX8aKNLPa7xnc1kRbqgNcoJCe6fQUdXY1VHLzpkPf3FH9UNdAZDZD"

PHONE_NUMBER_ID_1 = "683037344885466"



# Send Text Message
def send_text_message(to, message):
    url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID_1}/messages"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN_1}"
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to.replace("+", ""),  # remove +
        "type": "text",
        "text": {
            "body": message
        }
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        print("Text Sent:", res.status_code, res.text)
    except Exception as e:
        print("Error:", str(e))


# Send Document
def send_document(to, file_url, filename="file.pdf", caption=""):
    url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID_1}/messages"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN_1}"
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to.replace("+", ""),  # remove +
        "type": "document",
        "document": {
            "link": file_url,
            "caption": caption,
            "filename": filename
        }
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        print("Document Sent:", res.status_code, res.text)
    except Exception as e:
        print("Error:", str(e))


# TEST
if __name__ == "__main__":
    # Text
    send_text_message("+919667335707", "Hello")

    # # Document
    # send_document(
    #     "+919667335707",
    #     "https://pdfobject.com/pdf/sample.pdf",
    #     "https://pdfobject.com/pdf/sample.pdf",
    #     "https://pdfobject.com/pdf/sample.pdf"
    # )

    resume_links = [
    "https://pdfobject.com/pdf/sample.pdf",
    "https://pdfobject.com/pdf/sample.pdf"
]

for link in resume_links:
    send_document("+919667335707", link, "resume.pdf", "Candidate Resume")