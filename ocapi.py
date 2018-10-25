# @Upulag - 20/11/2017

import requests

#Insert cid here
cid = ""
pid = "BB6166_650"
firstname = ""
lastname = ""
email = ""
phonenum = ""
address1 = ""
address2 = ""
postcode = ""
city = ""
region = "GB"
cardnum = ""
expirymonth = 02
expiryyear = 2018
cvv = ""


def updateheaders(s,request,headers):
    etag = request.headers['ETag']
    headers['If-Match'] = etag
    message = ""
    for cookie in s.cookies:
        message = message + "%s=%s; " % (cookie.name, cookie.value)
    cookieheader = message[:-2]
    headers['Cookie'] = cookieheader
    return headers


s = requests.Session()

headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en-US,en;q=0.9',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}



authjson = { "type" : "guest"}


params =  {'client_id': cid}

auth = s.post("https://www.adidas.co.uk/s/adidas-GB/dw/shop/v18_3/customers/auth", headers=headers, params=params, json=authjson)
authorisation = auth.headers['Authorization']
headers['Authorization'] = authorisation


basket = s.post("https://www.adidas.co.uk/s/adidas-GB/dw/shop/v18_3/baskets", headers=headers)
headers = updateheaders(s,basket,headers)
basket_id = basket.json()['basket_id']


cart = s.post("https://www.adidas.co.uk/s/adidas-GB/dw/shop/v16_1/baskets/%s/items"%basket_id, headers=headers, json={ "product_id" : pid, "quantity":1 })
headers = updateheaders(s,cart,headers)
shipment_id = cart.json()['_flash'][4]['details']['shipmentId']


#getshipping_method = s.get("https://www.adidas.co.uk/s/adidas-GB/dw/shop/v18_3/baskets/%s/shipments/%s/shipping_methods"%(basket_id,shipment_id), headers=headers)


shipping_method = s.put("https://www.adidas.co.uk/s/adidas-GB/dw/shop/v18_3/baskets/%s/shipments/%s/shipping_method"%(basket_id,shipment_id), headers=headers, json={ "id" : "Standard-Parcelforce" })
headers = updateheaders(s,shipping_method,headers)


add_shipping = s.put("https://www.adidas.co.uk/s/adidas-GB/dw/shop/v18_3/baskets/%s/shipments/%s/shipping_address"%(basket_id,shipment_id), headers=headers, json={ "first_name" : firstname, "last_name" : lastname, "city" : city, "address1" : address1, "address2" : address2, "postal_code" : postcode, "phone" : phonenum, "country_code" : region })
headers = updateheaders(s,add_shipping,headers)


add_billing = s.put("https://www.adidas.co.uk/s/adidas-GB/dw/shop/v18_3/baskets/%s/billing_address"%basket_id, headers=headers, json={ "first_name" : firstname, "last_name" : lastname, "city" : city, "address1" : address1, "address2" : address2, "postal_code" : postcode, "phone" : phonenum, "country_code" : region })
headers = updateheaders(s,add_billing,headers)


add_info = s.put("https://www.adidas.co.uk/s/adidas-GB/dw/shop/v18_3/baskets/%s/customer"%basket_id, headers=headers, json={ "email" : email })
headers = updateheaders(s,add_info,headers)
price = add_info.json()["order_total"]


getpayment_method = s.get("https://www.adidas.co.uk/s/adidas-GB/dw/shop/v18_3/baskets/%s/payment_methods"%basket_id, headers=headers)


add_payment = s.post("https://www.adidas.co.uk/s/adidas-GB/dw/shop/v18_3/baskets/%s/payment_instruments"%basket_id, headers=headers, json={
  "amount" : price,
  "payment_card" : {
                     "number":cardnum,
                     "security_code":cvv,
                     "holder":"%s %s"%(firstname,lastname),
                     "card_type":"VISA",
                     "expiration_month":expirymonth,
                     "expiration_year":expiryyear
                    },
  "payment_method_id" : "CREDIT_CARD"
})
headers = updateheaders(s,add_payment,headers)
basket = add_payment.json()


create = s.post("https://www.adidas.co.uk/s/adidas-GB/dw/shop/v18_3/orders", headers=headers,json=basket)
headers = updateheaders(s,create,headers)
ordernumber = create.json()['order_no']
paymentinstrumentid = create.json()['payment_instruments'][0]['payment_instrument_id']
order = create.json()
print("Order No: %s, Payment Instrument ID: %s"%(ordernumber,paymentinstrumentid))

patch = s.patch("https://www.adidas.co.uk/s/adidas-GB/dw/shop/v18_3/orders/%s"%ordernumber, headers=headers, json =order)
headers = updateheaders(s,patch,headers)


payment_auth = s.patch("https://www.adidas.co.uk/s/adidas-GB/dw/shop/v18_3/orders/%s/payment_instruments/%s"%(ordernumber,paymentinstrumentid), headers=headers, json={
    "amount": price,
  "payment_card": {
                   "number": cardnum,
                   "security_code": cvv,
                   "holder": "%s %s"%(firstname,lastname),
                   "card_type": "VISA",
                   "expiration_month": expirymonth,
                   "expiration_year": expiryyear
    },
    "payment_method_id": "CREDIT_CARD",


})
