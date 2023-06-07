import os
import imaplib

# Gmail account credentials
username = "email@test.com"
password = "EMAIL PASSWORD"

# Connect to Gmail's IMAP server
imap_server = "imap.gmail.com"
imap_port = 993
mail = imaplib.IMAP4_SSL(imap_server, imap_port)
mail.login(username, password)

# Select the INBOX
mail.select("INBOX")

# Check if there are any emails in the Inbox
status, count = mail.search(None, "ALL")
num_emails = len(count[0].split())

if num_emails > 0:
    # Create error.txt file in /var/prtg/scripts/Gmail_Check and /var/prtg/scripts/Gmail_Check/Archive
    error_msg = "There are %d emails in the Inbox" % num_emails
    error_path = "/var/prtg/scripts/Gmail_Check/Errors.txt"
    archive_path = "/var/prtg/scripts/Gmail_Check/Archive/Errors.txt"
    
    if os.path.exists(error_path):
        pass # do nothing if error file already exists
    else:
        with open(error_path, "w+") as f:
            f.write(error_msg)
    
    with open(archive_path, "a") as f:
        f.write("\n" + error_msg)
    
    # Make both error.txt files overwritable
    os.chmod(error_path, 0o777)
    os.chmod(archive_path, 0o777)
else:
    # Delete /var/prtg/scripts/Gmail_Check/Errors.txt if it exists
    error_path = "/var/prtg/scripts/Gmail_Check/Errors.txt"
    
    if os.path.exists(error_path):
        os.remove(error_path)

# Close the mailbox and logout
mail.close()
mail.logout()
