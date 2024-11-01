import email
import imaplib

from Common.BaseClass import BaseClass


def get_last_email(email_address, password, from_email, browser):
    server = imaplib.IMAP4_SSL('smtp.gmail.com')
    server.login(email_address, password)
    server.select('[Gmail]/Spam')
    email_ids = server.search(None, 'FROM', from_email)
    email_id_list = email_ids[1][0].decode('utf-8').split()
    list_len = len(email_id_list)
    latest_email_ids = ""
    for i in range(4):
        latest_email_ids = latest_email_ids + "," + str(email_id_list[list_len - (i + 1)])
    latest_email_ids = latest_email_ids.strip(",").split(",")

    email_dict = {}
    for latest_email_id in latest_email_ids:
        email_dict = {}
        email_data = server.fetch(str(latest_email_id), "(RFC822)")
        message_content = email_data[1][0]
        if message_content is not None:
            if isinstance(message_content, tuple) and len(message_content) == 2:
                email_headers_bytes = message_content[1]
                if isinstance(email_headers_bytes, bytes):
                    message = email.message_from_bytes(email_headers_bytes)
                    email_dict["From"] = message.get('From')
                    email_dict["To"] = message.get('To')
                    email_dict["Date"] = message.get('Date')
                    email_dict["Subject"] = message.get('Subject')
                    for part in message.walk():
                        if part.get_content_type() == "text/plain" and not part.get("Content-Disposition"):
                            email_dict["Content"] = part.get_payload(decode=True).decode(
                                part.get_content_charset() or 'utf-8')
                    if f"{browser}_" in email_dict["Content"]:
                        break
                else:
                    print("The second element of message_content is not bytes.")
            else:
                print("message_content is not a tuple of length 2.")
        else:
            print("message_content is None")
    server.logout()
    return email_dict


def get_latest_email_subject(browser):
    email_body = get_last_email(BaseClass.email, BaseClass.email_password, 'ci@hedgehoglab.com', browser)
    if email_body is not None:
        email_subject = email_body["Subject"]
        return email_subject
    else:
        print("Email body is None")


def get_latest_email_content(browser):
    email_body = get_last_email(BaseClass.email, BaseClass.email_password, 'ci@hedgehoglab.com', browser)
    if email_body is not None:
        email_content = email_body["Content"]
        return email_content
    else:
        print("Email body is None")
