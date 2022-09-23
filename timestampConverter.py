'''
logファイルに含まれるUNIX時間を変換する

Usage: timestampConverter [-o FILE] [INPUT]

Options:
    -h, --help          ヘルプを表示します
    -o, --output FILE   出力先ファイルを指定します
'''
import os
import re
import sys
import datetime
from docopt import docopt


def checkArgs(args):
    if args['INPUT'] is None:
        print('logファイルを指定してください')
        sys.exit()
    if not os.path.isfile(args['INPUT']):
        print('logファイルが見つかりませんでした')
        sys.exit()
    if os.path.isfile(args['--output']):
        print(args['--output']+'は既に存在します')
        print('上書きしますか(y/N)')
        if input() != 'y':
            sys.exit()


def getConvertedTexts(input):
    with open(input) as f:
        def fromtimestamp(matchoj):
            return '[' + str(datetime.datetime.fromtimestamp(int(matchoj.group(1)), datetime.timezone(datetime.timedelta(hours=9)))) + ']'
        return [re.sub('\[([0-9]+)\]', fromtimestamp, s) for s in f.readlines()]


def putTexts(dir, texts):
    with open(dir, mode='w') as f:
        f.writelines(texts)


def main():
    try:
        args = docopt(__doc__)
        output = args['INPUT'] if args['--output'] is None else args['--output']
        putTexts(output, getConvertedTexts(args['INPUT']))
    except Exception as e:
        print('予期せぬエラーが発生しました')
        print(e)


if __name__ == '__main__':
    main()
