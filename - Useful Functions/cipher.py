def getmac(interface):
  # Return the MAC address of interface
  try:
    str = open('/sys/class/net/%s/address', %interface).readline()
  except:
    str = "00:00:00:00:00:00"
  return str[0:17]

def getTranslatedMessage(mode, message,key):
     if mode == 'd':
         key = -key
     translated = ''

     for symbol in message:
         if symbol.isalpha():
             num = ord(symbol)
             num += key

             if symbol.isupper():
                 if num > ord('Z'):
                     num -= 26
                 elif num < ord('A'):
                     num += 26
             elif symbol.islower():
                 if num > ord('z'):
                     num -= 26
                 elif num < ord('a'):
                     num += 26

             translated += chr(num)
         else:
             translated += symbol
     translated = translated.replace(':','')
#     return translated

	if mode == 'e':
	# ENCRYPTION: reverse and move end two chars to start
		#string = getTranslatedMessage('e',getmac('eth0'),22)[::-1]
		string = translated[::-1]
		firstpart, secondpart = string[:len(string)-2], string[len(string)-2:]
		final = secondpart+firstpart
		return final

	# DECIPHER - move first two chars to end and split
	if mode == 'd':
		#string2 = getTranslatedMessage('d',final,22)
		firstpart2, secondpart2 = translated[:2], translated[2:]
		final2 = secondpart2+firstpart2
		return final2[::-1]