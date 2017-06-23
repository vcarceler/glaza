import json

        
txt = '''192.168.17.187 | SUCCESS => {
    "name": "name1" 
}
192.168.17.147 | SUCCESS => {
    "name": "name2"
}
192.168.17.106 | UNREACHABLE! => {
    "changed": false, 
    "msg": "ERROR! SSH encountered an unknown error during the connection. We recommend you re-run the command using -vvvv, which will enable SSH debugging output to help diagnose the issue", 
    "unreachable": true
}
192.168.17.136 | UNREACHABLE! => {
    "changed": false, 
    "msg": "ERROR! SSH encountered an unknown error during the connection. We recommend you re-run the command using -vvvv, which will enable SSH debugging output to help diagnose the issue", 
    "unreachable": true
}'''

print(txt)

try:
    while 1:
        first_key = txt.index('SUCCESS =>')
        #print('Primera llave: {}'.format(first_key))

        substring = txt[first_key+10:]
        #print('Subcadena: {}'.format(substring))

        last_key = substring.find('}\n')

        json_string = substring[:last_key+1]
        print('Json: {}'.format(json_string))

        txt = substring[last_key:]
except:
    print('No hay más datos')
    