dict = {}

dict['hello'] = {'goodbye': 'world'}
dict['balls'] = 'cock'
dict['cum'] = 'sock'

agent_dict = {}

agent_dict['Stats'] = {'hostname': 'arch', 'family': 'linux'}
agent_dict['cock'] = 'balls'
agent_dict['dick'] = 'pud'

print(*[dict['hello'][key] + "," for key in dict['hello']])

args = [agent_dict['Stats'][key] + "," for key in agent_dict['Stats']]
print(args)
