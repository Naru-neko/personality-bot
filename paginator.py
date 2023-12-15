import discord

class PageView(discord.ui.View):
    def __init__(self, timeout=180, embeds:list=[]):
        super().__init__(timeout=timeout)
        self.embeds = embeds # [{'embed': discord.Embed, 'file': discord.File}, ... ]
        self.index = 0
        self.index_len = len(embeds)-1
        PageView.get_item(self, custom_id='pnum').label =  '1/' + str(self.index_len+1)
        
    @discord.ui.button(label="<<", style=discord.ButtonStyle.green)
    async def go_top(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.index = 0
        PageView.get_item(self, custom_id='pnum').label = str(self.index+1) + '/' + str(self.index_len+1)
        button.disabled = False
        file, embed = self.embeds[self.index]['file'], self.embeds[self.index]['embed']
        await interaction.response.edit_message(file=file, embed=embed, view=self)
            
    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def previous(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.index == 0:
            self.index = self.index_len
        else:
            self.index -= 1
        button.disabled = False
        PageView.get_item(self, custom_id='pnum').label = str(self.index+1) + '/' + str(self.index_len+1)
        file, embed = self.embeds[self.index]['file'], self.embeds[self.index]['embed']
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
        PageView.get_item(self, custom_id='pnum').label = str(self.index+1) + '/' + str(self.index_len+1)
        button.disabled = False
        file, embed = self.embeds[self.index]['file'], self.embeds[self.index]['embed']
        await interaction.response.edit_message(file=file, embed=embed, view=self)
        
    @discord.ui.button(label=">>", style=discord.ButtonStyle.green)
    async def go_end(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.index = 15
        PageView.get_item(self, custom_id='pnum').label = str(self.index+1) + '/' + str(self.index_len+1)
        button.disabled = False
        file, embed = self.embeds[self.index]['file'], self.embeds[self.index]['embed']
        await interaction.response.edit_message(file=file, embed=embed, view=self)
        
