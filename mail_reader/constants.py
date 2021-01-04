import os
PERSONAL_EMAIL = os.getenv('personal_email')
ENCODED_PASSWORD = os.getenv('personal_password')

IGNORE_EMAILS_LIST = ['Quora Digest', 'Ola', 'Quora']
IMPORTANT_EMAILS_LIST = ['HackerRank Team', 'HackerRank', 'udemy']
INVALID_FORMATE = '?utf'
GMAIL_LINK = "https://mail.google.com/mail/u/1/?tab=wm&ogbl#search/"

CGREEN = '\033[32m'  # Green
CYELLOW = '\33[33m'  # Yellow
CRED = '\033[91m'  # Red
END_COLORING = '\033[0m'  # end coloring

IMPORTENT = "important"
IGNORE = "ignore"
NORMAL = "normal"

EMAIL_COLORS = {
    IMPORTENT: CGREEN,
    NORMAL: CYELLOW,
    IGNORE: CRED
}
