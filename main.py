import json , sys , hashlib , os , time , marshal
from dependency import API_KEY, API_SECRET
from sys import argv


if sys.platform in ["linux","linux2"]:
	W = "\033[0m"
	G = '\033[32;1m'
	R = '\033[31;1m'
else:
	W = ''
	G = ''
	R = ''
try:
	import requests
except ImportError:
    print("Error Import requests")

jml = []
jmlgetdata = []
n = []

def dump(one_id):
	one_id = one_id
	print('[*] load access token')
	try:
		token = open('cookie/token.log','r').read()
		print('[*] Success load access token')
	except IOError:
		print('[!] failed load access token')
		print("[*] type 'token' to generate access token")
	print("[*] fetching all phone numbers")
	print('[*] start')
	try:
		if one_id == "all" or one_id == "All":
			x = requests.get('https://graph.facebook.com/me/friends?access_token=' + token)
			z = json.loads(x.text)
			for i in z['data']:
				x = requests.get("https://graph.facebook.com/" + i['id'] + "?access_token=" + token)
				z = json.loads(x.text)
				try:
					name = z['name']
				except KeyError:
					name = "Null"
				try:
					mobile_phone = z['mobile_phone']
				except KeyError:
					mobile_phone = "Null"
				try:
					email = z['email']
				except KeyError:
					email = "Null"
				print(W + '[' + G + name + W + ']' + R + ' >> phone: ' + W + mobile_phone + ', ' + R + 'email: ' + W + email)
		else:
			x = requests.get("https://graph.facebook.com/"+one_id+"?access_token="+token)
			z = json.loads(x.text)
			try:
				name = z['name']
			except KeyError:
				name = "Null"
			try:
				mobile_phone = z['mobile_phone']
			except KeyError:
				mobile_phone = "Null"
			try:
				email = z['email']
			except KeyError:
				email = "Null"
			print(W + '[' + G + name + W + ']' + R + ' >> phone: ' + W + mobile_phone + ', ' + R + 'email: ' + W + email)
		print('[*] done')
	except KeyboardInterrupt:
		print('\r[!] Stopped')
	except KeyError:
		print("[!] failed to fetch all phone numbers")
	except (requests.exceptions.ConnectionError , requests.exceptions.ChunkedEncodingError):
		print('[!] Connection Error')
		print('[!] Stopped')

def baliho():
    try:
        token = open('cookie/token.log', 'r').read()
        r = requests.get('https://graph.facebook.com/me?access_token=' + token)
        a = json.loads(r.text)
        name = a['name']
        n.append(a['name'])
        print('[*] ' + name + ' [*]')
    except (KeyError, IOError):
        print("Eror authorization")

def id():
	print ('[*] login to your facebook account         ')
	id = input('[?] Username : ')
	pwd = input('[?] Password : ')
	data = {"api_key": API_KEY,"credentials_type":"password","email":id,"format":"JSON", "generate_machine_id":"1","generate_session_cookies":"1","locale":"en_US","method":"auth.login","password":pwd,"return_ssl_resources":"0","v":"1.0"};sig = 'api_key=882a8490361da98702bf97a021ddc14dcredentials_type=passwordemail='+id+'format=JSONgenerate_machine_id=1generate_session_cookies=1locale=en_USmethod=auth.loginpassword='+pwd+'return_ssl_resources=0v=1.0'+API_SECRET
	x = hashlib.new('md5')
	x.update(sig.encode('utf-8'))
	data.update({'sig':x.hexdigest()})
	data.update({'sig':x.hexdigest()})
	try:
		os.mkdir('cookie')
	except OSError:
		pass
	b = open('cookie/token.log','w')
	try:
		r = requests.get('https://api.facebook.com/restserver.php',params=data)
		a = json.loads(r.text)
		b.write(a['access_token'])
		b.close()
		print('[*] successfully generate access token')
		print('[*] Your access token is stored in cookie/token.log')
		exit()
	except KeyError:
		print('[!] Failed to generate access token')
		print('[!] Check your connection / email or password')
		os.remove('cookie/token.log')
	except requests.exceptions.ConnectionError:
		print('[!] Failed to generate access token')
		print('[!] Connection error !!!')
		os.remove('cookie/token.log')

if __name__ == '__main__':
	global target_id
	global one_id
	baliho()
	if len(argv) == 2:
		if argv[1] == "New" or argv[1] == "new":
			id()
			x = input("Vvedite ID or All: ")
			dump(x)
		dump(argv[1])
	else:
		x = input("Vvedite ID or All: ")
		if x == "New" or x == "new":
			id()
		dump(x)


