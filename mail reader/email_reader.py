import imaplib
import email
import pyttsx3
import base64
import pdb
import constants

class EmailReader:
  def __init__(self):
    email, password = self.__get_credentials()
    self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
    self.mail.login(email, password)
    self.mail.select('inbox')
    self.speaker = pyttsx3.init()

  def get_all_unread_email(self):
    new_emails_data = []
    result, data = self.mail.search(None, 'UNSEEN')
    new_email_id_list = data[0].split()
    for email_id in new_email_id_list:
      result, mail_data = self.mail.fetch(str(int(email_id)), '(RFC822)')
      new_emails_data.append(mail_data[0])

    return new_emails_data

  def is_any_new_emails(self, new_emails_list):
    if not new_emails_list:
        self.speaker.say("No new email")
        self.speaker.runAndWait()
        return False
    else:
        self.speaker.say("We have "+str(len(new_emails_list)) + "new email")
        self.speaker.runAndWait()
        return True

  def read_new_mails(self, new_emails_list):
    ignored_emails = []

    mails_categories = self.__categories_new_email(new_emails_list)

    self.__read_and_print_email(mails_categories[constants.IMPORTENT], constants.IMPORTENT)
    self.__read_and_print_email(mails_categories[constants.NORMAL], constants.NORMAL)

    for ignored_email in mails_categories[constants.IGNORE]:
      ignored_emails.append(ignored_email['from'])
      self.__print_email_content("From: " + ignored_email['from'],
                                "Subject: " + ignored_email['subject'],
                                constants.EMAIL_COLORS[constants.IGNORE])

    self.__ignored_emails_data(ignored_emails)

  #Private methods
  def __print_email_content(self, from_email, subject, mail_color, link=""):
    print(mail_color)
    print(from_email + '\n')
    print(subject + '\n')
    if(link):
      print(link + '\n\n')
    print(constants.END_COLORING)

  def __validate_email_content(self, from_email, subject):
    from_email_and_name = from_email.split('<')
    from_email = from_email_and_name[0]
    email_subject = subject
    if constants.INVALID_FORMATE in from_email.strip().lower():
      from_email = from_email_and_name[1].split('@')[0]

    if constants.INVALID_FORMATE in email_subject.strip().lower():
        email_subject = "contains invalid text formate"

    return from_email.strip(), email_subject.strip()

  def __ignored_emails_data(self, ignored_emails):
    ignore_email_counts = dict()
    for from_email in ignored_emails:
      ignore_email_counts[from_email] = ignore_email_counts.get(from_email, 0) + 1
    
    for from_email, email_count in ignore_email_counts.items():
      self.__text_to_voice( 
          ["Ignored email list",
            "We Ignored " + str(email_count) + "emails from" + from_email
          ]
        )

  def __read_and_print_email(self,email_list, type):
    for p_email in email_list:
      self.__text_to_voice(
          [
            type + " email",
            "From " + p_email['from'],
            "Subject " + p_email['subject']
          ]
      )
      email_link = constants.GMAIL_LINK+'+'.join(p_email['subject'].split(' '))
      self.__print_email_content("From: " + p_email['from'],
                                "Subject: " + p_email['subject'],
                                constants.EMAIL_COLORS[type],
                                email_link)
  
  def __get_credentials(self):
    return constants.PERSONAL_EMAIL, base64.b64decode(constants.ENCODED_PASSWORD).decode()

  def __text_to_voice(self,datas=[]):
    for data in datas:
      self.speaker.say(data)
    self.speaker.runAndWait()

  def __categories_new_email(self, new_emails_list):
    emails_by_category = {
        constants.IMPORTENT: [],
        constants.IGNORE: [],
        constants.NORMAL: []
    }
    for email_data in new_emails_list:
      msg = email.message_from_bytes(email_data[1])
      from_email, subject = self.__validate_email_content(msg['from'], msg['subject'])

      email_category = constants.NORMAL

      if from_email in constants.IGNORE_EMAILS_LIST:
        email_category = constants.IGNORE
      elif from_email in constants.IMPORTANT_EMAILS_LIST:
        email_category = constants.IMPORTENT

      emails_by_category[email_category].append(
          {"from": from_email, "subject": subject})

    return emails_by_category



email_reader = EmailReader()
new_emails_list = email_reader.get_all_unread_email()

if email_reader.is_any_new_emails(new_emails_list):
  email_reader.read_new_mails(new_emails_list)
