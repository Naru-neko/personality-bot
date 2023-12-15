import discord
import os
from dotenv import load_dotenv
from discord.commands import Option

from gen_embed import gen_exp, gen_question, gen_result
from load_yml import exp_size, question_size, load_attr
from get_type import get_type, tyoe_color


# Classes
#============================================================================================

class TestView(discord.ui.View):
    def __init__(self, timeout=180, lang='ja', index=0):
        super().__init__(timeout=timeout)
        self.lang = lang
        self.index = index
        self.result = []
            
    @discord.ui.button(label='Yes', style=discord.ButtonStyle.red)
    async def yes(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.result.append(load_attr(self.lang, self.index)) # add attribute of type to list 
        self.index += 1
        button.disabled = False
        if self.index == question_size(self.lang):
            type = get_type(self.result)
            color = tyoe_color(type)
            file, embed = gen_result(self.lang, type, color)
            await interaction.response.edit_message(file=file ,embed=embed, view=None)
        else:
            await interaction.response.edit_message(embed=gen_question(self.lang, self.index), view=self)
        
    @discord.ui.button(label="No", style=discord.ButtonStyle.primary)
    async def No(self, button: discord.ui.Button, interaction: discord.Interaction):
        # attribute of case :'No'
        if load_attr(self.lang, self.index) == 'N':
            self.result.append('S')
        elif load_attr(self.lang, self.index) == 'T':
            self.result.append('F')
        elif load_attr(self.lang, self.index) == 'J':
            self.result.append('P')
        elif load_attr(self.lang, self.index) == 'E':
            self.result.append('I')
        self.index += 1
        button.disabled = False
        if self.index == question_size(self.lang):
            type = get_type(self.result)
            color = tyoe_color(type)
            file, embed = gen_result(self.lang, type, color)
            await interaction.response.edit_message(file=file ,embed=embed, view=None)
        else:
            await interaction.response.edit_message(embed=gen_question(self.lang, self.index), view=self)
        
        
class ExpView(discord.ui.View):
    def __init__(self, timeout=180, lang='ja', index=0):
        super().__init__(timeout=timeout)
        self.lang = lang
        self.index = index
        self.index_len = exp_size()-1
        ExpView.get_item(self, custom_id='pnum').label =  '1/' + str(self.index_len+1)
        
    @discord.ui.button(label="<<", style=discord.ButtonStyle.green)
    async def go_top(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.index = 0
        ExpView.get_item(self, custom_id='pnum').label = str(self.index+1) + '/' + str(self.index_len+1)
        button.disabled = False
        file, embed = gen_exp(self.lang, self.index)
        await interaction.response.edit_message(file=file, embed=embed, view=self)
            
    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def previous(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.index == 0:
            self.index = self.index_len
        else:
            self.index -= 1
        button.disabled = False
        ExpView.get_item(self, custom_id='pnum').label = str(self.index+1) + '/' + str(self.index_len+1)
        file, embed = gen_exp(self.lang, self.index)
        await interaction.response.edit_message(file=file, embed=embed, view=self)
        
    @discord.ui.button(label=None, style=discord.ButtonStyle.gray, disabled=True, custom_id='pnum')
    async def page_num(self):
        ...
        
    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.index == self.index_len:
            self.index = 0
        else:
            self.index += 1
        ExpView.get_item(self, custom_id='pnum').label = str(self.index+1) + '/' + str(self.index_len+1)
        button.disabled = False
        file, embed = gen_exp(self.lang, self.index)
        await interaction.response.edit_message(file=file, embed=embed, view=self)
        
    @discord.ui.button(label=">>", style=discord.ButtonStyle.green)
    async def go_end(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.index = 15
        ExpView.get_item(self, custom_id='pnum').label = str(self.index+1) + '/' + str(self.index_len+1)
        button.disabled = False
        file, embed = gen_exp(self.lang, self.index)
        await interaction.response.edit_message(file=file, embed=embed, view=self)
        
#============================================================================================

load_dotenv()

TOKEN = os.environ.get('DISCORD_PERSONALITY_BOT_TOKEN')

bot = discord.Bot(
        intents=discord.Intents.all(),
        activity=discord.Game("/test [lang]"),
)


@bot.event
async def on_ready():
    print("Bot Booted.")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return


@bot.command(name="test", description="性格タイプ診断テストを開始します")
async def test(ctx: discord.ApplicationContext,
               lang: Option(str, '言語は？ - language?', choices=['ja', 'en'])):
    embed=gen_question(lang, 0)
    view = TestView(timeout=None, lang=lang, index=0)
    await ctx.interaction.response.send_message(embed=embed,
                                                view=view,
                                                ephemeral=True # view only sender
                                                )


@bot.command(name="doc", description="性格タイプ解説を表示します")
async def doc(ctx: discord.ApplicationContext, 
              lang: Option(str, '言語は？ - language?', choices=['ja', 'en'])):
    file, embed = gen_exp(lang, 0)
    view = ExpView(timeout=None, lang=lang, index=0)
    await ctx.interaction.response.send_message(file=file,
                                                embed=embed,
                                                view=view,
                                                ephemeral=True # view only sender
                                                )


''' for debug
@bot.command(name="cmdtest")
async def cmdtest(ctx: discord.Guild):
    ...
'''


# booting bot
bot.run(TOKEN)