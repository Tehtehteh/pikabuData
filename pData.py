import requests
from bs4 import BeautifulSoup
from IPython.display import SVG
import pygal


users = []


def fetch_users():
	url = 'http://pikabu.ru/banned_users.php'
	soup = BeautifulSoup(requests.get(url=url).content, 'html.parser')
	table = soup.find('table', attrs={'class':'banned_users'}).find_all('tr')
	for row in table[1:]:
		cells = row.find_all('td')
		users.append({
					'username': cells[0].find('a')['name'],
					'type'	: cells[1].text,
					'reason': cells[3].text
		})


def fetch_results():
	reasons = dict()
	for case in users:
		reasons[case['reason']] = reasons.get(case['reason'], 0) + 1
	return reasons


def main(reasons):
	chart = pygal.HorizontalBar()
	chart.title = 'Pikabu banned users statistics'
	for case in reasons:
		chart.add(case, reasons[case])
	chart.render_to_file('data.svg')
	SVG(filename='data.svg')


if __name__ == '__main__':
	fetch_users()
	reasons = fetch_results()
	main(reasons)