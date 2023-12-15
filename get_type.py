import random
import re


def random_attr(attr1:str, attr2:str) -> str:
    choice = random.randint(1,2)
    if choice == 1:
        return attr1
    else:
        return attr2


def attr_comparer(attr1:str, attr2:str, attrs:dict):
    if attrs[attr1] == attrs[attr2]:
        attrs[random_attr(attr1, attr2)] += 1
    if attrs[attr1] > attrs[attr2]:
        return attr1
    elif attrs[attr1] < attrs[attr2]:
        return attr2


def simply_personality_analyzer(attrs:dict) -> list: 
    chosen_attrs = []
    
    if attrs['N'] == attrs['S']:
        attrs[random_attr('N', 'S')] += 1
        
    if attrs['N'] > attrs['S']:
        chosen_attrs.append('N')
        chosen_attrs.append(attr_comparer('T', 'F', attrs))
        chosen_attrs.insert(0, attr_comparer('I', 'E', attrs))
        chosen_attrs.append(attr_comparer('J', 'P', attrs))
        
    elif attrs['N'] < attrs['S']:
        chosen_attrs.append('S')
        chosen_attrs.append(attr_comparer('J', 'P', attrs))
        chosen_attrs.insert(0, attr_comparer('I', 'E', attrs))
        chosen_attrs.insert(2, attr_comparer('T', 'F', attrs))
            
    return ''.join(chosen_attrs)
    

def get_type(result:list = []):
    attrs = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
    
    for r in result: # count each num of attr
        for attr in attrs.keys():
            if attr == r:
                attrs[attr] += 1
                
    return simply_personality_analyzer(attrs)


def tyoe_color(type):
    patterns = {'.NT.': 0xff00ff, '.NF.': 0x00ff00, '.S.J': 0x40aaff, '.S.P': 0xffff00}
    for pattern in patterns.keys():
        if re.match(pattern, type):
            return patterns[pattern]
    return 0x6173ff

if __name__ == '__main__':
    print(get_type(['I', 'S', 'T', 'P'])) # for debug