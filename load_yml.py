import yaml
import csv


def load_question(lang, index):
    with open('data/questions.yml', 'r', encoding='utf-8') as yml:
        questions = yaml.safe_load(yml)        
        return questions[lang][index]['question']
    
    
def load_attr(lang, index):
    with open('data/questions.yml', 'r', encoding='utf-8') as yml:
        questions = yaml.safe_load(yml)
        return questions[lang][index]['attr']
    
    
def question_size(lang='ja'):
    with open('data/questions.yml', 'r', encoding='utf-8') as yml:
        questions = yaml.safe_load(yml)
        return len(questions[lang])
    
    
def load_exp(lang):
    with open('data/explanations.yml', 'r', encoding='utf-8') as yml:
        exps = yaml.safe_load(yml)
        return exps[lang]


def exp_size(lang='ja'):
    with open('data/explanations.yml', 'r', encoding='utf-8') as yml:
        exps = yaml.safe_load(yml) 
        return len(exps[lang])


def load_type(lang, type):
    with open('data/types.yml', 'r', encoding='utf-8') as yml:
        types = yaml.safe_load(yml) 
        return types[lang][type]
    
    
def convert_qcsv(file):
    qlist = []
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            qlist.append({'question': row[0], 'attr': row[1]})
    content = {'ja': qlist}
    with open('data/questions.yaml','w', encoding='utf-8') as f:
        yaml.dump(content, f, default_flow_style=False, allow_unicode=True)
        
        
        
if __name__ == '__main__':
    convert_qcsv('data/questions.csv')