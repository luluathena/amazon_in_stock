# coding=utf-8
from lxml import html
import requests
import itchat
import time

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

# 海外购商品列表，填了price则会在低于这个价格时汇报
PRODUCTS = (
	{ 'asin' : 'B01JRF2M0Y'},
	{ 'asin' : 'B002XC8VXG', 'price' : 100},
)

URL_PREFIX = r'https://www.amazon.cn/gp/product/'

class HtmlConst(object):
	XPATH_NAME = '//span[@id="productTitle"]//text()'
	XPATH_METICS = '//div[@id="cerberus-data-metrics"]'
	XPATH_DELIVERY = '//div[@id="dynamicDeliveryMessage"]'

	ATTRIB_PRICE = 'data-asin-price'
	ATTRIB_ID = 'id'

	VALUE_DELIVERY = 'ddmDeliveryMessage'
	value_shipping = 'ddmShippingMessage'

class Product(object):
	def __init__(self, idx):
		self.index = idx
		asin = PRODUCTS[idx]['asin']
		self.url = URL_PREFIX + asin
		page = requests.get(self.url, headers=headers)
		doc = html.fromstring(page.content)

		# 因为找到了2种判断库存的方式，所以做个试验，对比一下:P
		metics = doc.xpath(HtmlConst.XPATH_METICS)
		price = metics[0].attrib[HtmlConst.ATTRIB_PRICE]
		if price:
			in_stock1 = True
			self.price = float(price)
		else:
			in_stock1 = False
			self.price = 100000

		in_stock2 = False
		delivery = doc.xpath(HtmlConst.XPATH_DELIVERY)
		for div in delivery[0].getchildren():
			if div.attrib.get(HtmlConst.ATTRIB_ID, '') == HtmlConst.VALUE_DELIVERY:
				in_stock2 = True	

		assert in_stock1 == in_stock2
		self.in_stock = in_stock1

		name = doc.xpath(HtmlConst.XPATH_NAME)[0]
		self.name = name.strip(' \t\n\r')

		# 有些含有特殊字符的商品名，命令行输出会出错
		try:
			self.name.encode('gbk')
		except:
			self.name = self.name.encode('gbk', 'replace').decode('gbk')

	def check_status(self, user_name):
		if self.in_stock:
			data = PRODUCTS[self.index]
			if data.has_key('price'):
				# 符合条件则发送微信
				if self.price <= data['price']:
					itchat.send(self.name + u'price {0}. {1}'.format(self.price, self.url), toUserName=user_name)
				else:
					print self.name, 'current price {0}'.format(self.price)
			else:
				itchat.send(self.name + u' in stock, price {0}. {1}'.format(self.price, self.url), toUserName=user_name)
		else:
			print self.name, 'out of stock'

if __name__ == '__main__':
	# 自动登录，命令行显示二维码
	itchat.auto_login(hotReload=True, enableCmdQR=True)
	# 搜索好友，用来发消息
	user_name = itchat.search_friends(name='lulu')[0]['UserName']
	while True:
		for idx in xrange(len(PRODUCTS)):
			try:
				product = Product(idx)
			except:
				import traceback
  				traceback.print_exc()
  				continue

			product.check_status(user_name)

		print 'Finish check %s...' % time.strftime('%H:%M:%S',time.localtime(time.time()))
		time.sleep(600)