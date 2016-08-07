# -*- coding:utf8 -*-
import urllib2

def get_content(text):
    url_get_base = "http://api.ltp-cloud.com/analysis/?"
    api_key = 'f7S3f5f6LjpjUuJeBw9VAzfsIlgCLcCcBrPT4GyF'
    #text1 = '妈妈买了15个苹果,买了6个橘子,问一共买了多少个水果?'
    #text += '草地上有10只羊,跑走了3只白山羊,又来了7只黑山羊,现在共有几只羊?'
    format = 'xml'
    pattern = 'all'
    result = urllib2.urlopen("%sapi_key=%s&text=%s&format=%s&pattern=%s" % (url_get_base,api_key,text,format,pattern))
    content = result.read().strip()
    return content


def read_file(filename, select = 1):
  fp = open(filename, 'r')
  data = []
  for line in fp:
    if select == 0:
      line = line[line.find('.')+1 : line.find('\r')] +'\n'
      if line.find('\t') != -1:
        line = line[:line.find('\t')]
      else:
        line = line[:line.find('\n')]
    else:
      line = line[:line.find('\n')]
    #line = line.decode().encode('utf-8')
    data.append(line)
  return data

def save_xml(filename, xml):
    fp = open(filename, 'w')
    fp.write(xml)
    fp.close()

if __name__ == '__main__':
    wp = read_file('./dev_for_8', 0)    
    for index in range(len(wp)):
        if index >= 153:
            s = './result/question-%d.xml' % (index+1)
            save_xml(s, get_content(wp[index]))
    print ok
