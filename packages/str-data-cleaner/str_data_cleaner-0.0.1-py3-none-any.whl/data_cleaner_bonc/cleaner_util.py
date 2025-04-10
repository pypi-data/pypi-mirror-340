import bs4


def deal_title(title: str) -> str:
    return bs4.BeautifulSoup(title, 'html.parser').text
