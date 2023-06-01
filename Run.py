import imaplib
import email
import os
import re
import uuid
import time

def process_inbox(imap_server, output_dir):
    # Select the INBOX
    imap_server.select("INBOX")

    # Search for all messages in the INBOX
    _, message_ids = imap_server.search(None, 'ALL')

    # Loop through the message IDs and fetch each message
    for message_id in message_ids[0].split():
        _, message_data = imap_server.fetch(message_id, '(RFC822)')

        # Convert the message to a Message object
        message = email.message_from_bytes(message_data[0][1])

        # Get the message subject and body
        subject = message['Subject']
        body = message.get_payload()

        # Extract phone numbers from "To" field in email header
        phone_numbers = []
        for match in re.finditer(r'(\d{10,})@', message['To']):
            phone_numbers.append(match.group(1))

        if not phone_numbers:
            raise ValueError('Invalid phone number format')

        # Convert the message body to plain text
        if message.is_multipart():
            for part in message.get_payload():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True)
        else:
            body = message.get_payload(decode=True)

        # Make the filename unique and write to separate files
        for i, phone_number in enumerate(phone_numbers):
            unique_id = str(uuid.uuid1())
            timestamp = str(int(time.time()))
            filename = os.path.join(output_dir, f'{unique_id}-{timestamp}.txt')
            with open(filename, 'w') as f:
                f.write(f'To: {phone_number}\n\n{body.decode()}')

        # Archive the message
        imap_server.store(message_id, '+X-GM-LABELS', '\\Trash')

    # Permanently delete the messages marked as deleted
    imap_server.expunge()

# Connect to the Gmail IMAP server using SSL
imap_server = imaplib.IMAP4_SSL('imap.gmail.com')

# Authenticate using email and password
email_address = 'test@test.com'
password =  'password'
imap_server.login(email_address, password)

# Create a directory for the text files
output_dir = '/var/spool/sms/gsm1'
os.makedirs(output_dir, exist_ok=True)

# Process the INBOX
process_inbox(imap_server, output_dir)

# Close the connection to the server
imap_server.close()
imap_server.logout()
