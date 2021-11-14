# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import urllib.request
from bs4 import BeautifulSoup


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = "https://pittsburghbaseball.com/"
    text = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(text,'html.parser')

    data = soup.find_all('ul', attrs={'class': 'wplp_listposts defaultflexslide'})
    hrefs = []
    for ul in data:
        links = ul.find_all('a')
        for a in links:
            if a['href'] not in hrefs:
                hrefs.append(a['href'])
    print(hrefs)
    print(len(hrefs))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
