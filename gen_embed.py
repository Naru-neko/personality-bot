import discord
from load_yml import load_question, load_type, load_exp


def gen_question(lang, index):
    title = {'ja':'性格タイプ診断', 'en':'Personality TEST'}
    embed = discord.Embed(title=title[lang],
                          color=0x6173ff
                         )
    embed.add_field(name='Q' + str(index+1) + '. ' + load_question(lang, index),
                    value=''
                    )
    return embed


def gen_result(lang, type, color=0x6173ff):
    title = {'ja':'あなたの性格タイプは...', 'en':'Your Personality is...'}
    embed = discord.Embed(title=title[lang],
                          color=color
                         )
    embed.add_field(name=load_type(lang, type),
                    value=''
                    )
    
    fname= type + ".png" # アップロード時のファイル名, 拡張子付
    file = discord.File(fp="resources/types/" + fname,filename=fname,spoiler=False)
    embed.set_image(url=f"attachment://{fname}")
    return file, embed


def gen_exp(lang, index):
    title = {'ja':'性格タイプ一覧', 'en':'Personal Types'}
    type = list(load_exp(lang).keys())[index]
    embed = discord.Embed(title=title[lang],
                          color=0x6173ff
                         )
    embed.add_field(name = type + ' ' + list(load_exp(lang).values())[index],
                    value=''
                    )
    fname= type + ".png"
    file = discord.File(fp="resources/types/" + fname,filename=fname,spoiler=False)
    embed.set_image(url=f"attachment://{fname}")
    return file, embed