import sys
import requests
from .botmessage import botreply
from bs4 import BeautifulSoup
from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re

def sukkirisu(month_or_rank=1, target_type='month'):
  url = 'https://www.ntv.co.jp/sukkiri/sukkirisu/'
  html = requests.get(url)
  soup = BeautifulSoup(html.content, "html.parser")
  
  fortune_telling_date = soup.find('p' ,class_ = 'date').text
  
  results = []
  rank01 = soup.find('h3', class_='rankGroup-1').find_next()
  rank1_row1 = rank01.find('div', class_='row1')
  rank1_row2 = rank01.find('div', class_='row2')
  results.append(FortuneResult(1, int(rank1_row1.p.span.text), rank1_row2.p.text, rank1_row2.div.text))

  rank12 = soup.find('h3', class_='rankGroup-12').find_next()
  rank12_row1 = rank12.find('div', class_='row1')
  rank12_row2 = rank12.find('div', class_='row2')
  results.append(FortuneResult(12, int(rank12_row1.p.span.text), rank12_row2.p.text, rank12_row2.div.text))
  
  rank02_06 = soup.find('h3', class_='rankGroup-2').find_next()
  rank2_row1 = rank02_06.find_all('div', class_='row1')
  rank2_row2 = rank02_06.find_all('div', class_='row2')

  for (row1, row2) in zip(rank2_row1, rank2_row2):
    results.append(FortuneResult(int(row1.div.text.replace('位', '')), int(row1.p.span.text), row2.p.text, row2.div.text))

  rank07_11 = soup.find('h3', class_='rankGroup-7').find_next()
  rank7_row1 = rank07_11.find_all('div', class_='row1')
  rank7_row2 = rank07_11.find_all('div', class_='row2')

  for (row1, row2) in zip(rank7_row1, rank7_row2):
    results.append(FortuneResult(int(row1.div.text.replace('位', '')), int(row1.p.span.text), row2.p.text, row2.div.text))

  ranks = {r.rank:r for r in results}
  monthes = {r.month:r for r in results}

  if target_type == 'rank':
    r = ranks[int(month_or_rank)]
    return f"{fortune_telling_date}\n{r.month}月:{r.eval_fortune()} ラッキーカラー:{r.color}\n{r.comment}"
  elif target_type == 'month':
    r = monthes[int(month_or_rank)]
    return f"{fortune_telling_date}\n{r.eval_fortune()} ラッキーカラー:{r.color}\n{r.comment}"
  else:
    r = monthes[int(month_or_rank)]
    return f"{fortune_telling_date}\n{r.eval_fortune()} ラッキーカラー:{r.color}\n{r.comment}"

class FortuneResult:
  def __init__(self, rank, month, comment, color):
    self.rank = rank
    self.month = month
    self.comment = comment
    self.color = color

  def eval_fortune(self):
    if self.rank == 1:
      return '超スッキりす'
    elif self.rank == 12:
      return 'ガッカりす'
    elif self.rank in [2,3,4,5,6]:
      return f"スッキりす{self.rank}位"
    elif self.rank in [7,8,9,10,11]:
      return f"まあまあスッキりす {self.rank}位"
    else:
      return ''

@respond_to('^sukkirisu\s+([1-9]|1[0-2])(\s+rank)?$')
def sukkiri(message, month, target='month'):
  return botreply(message,sukkirisu(month, target))

