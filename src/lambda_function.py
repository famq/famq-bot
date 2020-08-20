import sys
import json
import urllib.parse

from plugins import sukkirisu

def lambda_handler(event, context):
  month = int(urllib.parse.parse_qs(event['body'])['text'][0].rstrip())
  target='month'
  result = sukkirisu.sukkirisu(month,target)
  return {
    'isBase64Encoded': False,
    'statusCode': 200,
    'headers': {},
    'body': json.dumps({
        "response_type": "in_channel",
        "text": result
    })
  }

if __name__ == '__main__':
  if len(sys.argv) != 2:
    sys.stderr.write("argument error: {} <month in int>\n".format(sys.argv[0]))
    sys.exit(1)
  target='month'
  result = sukkirisu.sukkirisu(int(sys.argv[1]),target)
  print(result)