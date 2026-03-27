import re

ALLOWED_SENDERS = [
    "creator-spotlight@mail.beehiiv.com",
    "dan@highperformancefounder.com",
    "newsletter@economictimesnews.com",
    "evolvingai@mail.beehiiv.com",
    "jason@quantscience.io",
    "hi@news.jayshetty.me",
    "o@ollyrichards.co",
    "dailybite@mail.beehiiv.com",
    "stayingahead@mail.beehiiv.com",
    "thecore@mail.beehiiv.com",
    "drjustinsung@icanstudy.com",
    "jason@pyquantnews.com",
    "pyquantnews@substack.com",
    "hello@justinwelsh.me",
    "mitchell@baldridgecpa.com",
    "nick@sweatystartup.com",
    "no-reply@teamsidebar.com",
    "sieva@sievakozinsky.com",
    "simonsquibb@simonsquibb.com",
    "support@vinhgiang.com",
    "jason@asmartbear.com",
    "kasey@teamsidebar.com",
    "mosh@codewithmosh.com",
    "newsletter@codewithmosh.com",
]

def is_allowed_sender(sender):
    if not sender:
        return False

    match = re.search(r'[\w\.-]+@[\w\.-]+', sender)

    if not match:
        return False

    email_addr = match.group(0).lower()

    return email_addr in ALLOWED_SENDERS