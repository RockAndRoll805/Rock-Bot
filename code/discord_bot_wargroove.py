import discord
from discord.ext import commands

class Wargroove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        global attacker_arr, unit_names, terrain_names, co_damage_list, crit_multiplier, terrain_defense, co_hp, co_terrain, message_out, message_embed
        attacker_arr = []
        unit_names = ['soldier', 'dog', 'spearman', 'archer', 'mage', 'cavalry', 'ballista', 'trebuchet', 'giant', 'aeronaut', 'hex', 'dragon', 'warship', 'amphibian', 'rifleman', 'commander']
        terrain_names = ['road', 'bridge', 'plains', 'forest', 'mountain', 'beach', 'river', 'flagstone', 'carpet']
        co_damage_list = [15, 20, 20, 10, 25, 30, 15, 30, 40, 20, 10, 40, 30, 15, 10]
        crit_multiplier = [1.5, 1.5, 1.5, 1.35, 1.5, 1.5, 1.5, 1.5, 2.5, 1.25, 1, 2, 1.5, 2, 1.5]
        terrain_defense = [0, 0, 10, 30, 40, -1, -2, 2, 2]
        co_hp = 100
        co_terrain = 'plains'

        message_out = discord.Message
        message_embed = discord.Embed

    # using listener instead of command because making a command called "range" overloads python range
    @commands.Cog.listener()
    async def on_message(self, msg):
        msg_content = msg.content
        if msg_content.lower().startswith('!range'):
            num = int(msg_content.split(' ')[1])
            if num > 7:
                return
            output = ''
            for i in range(num+1):
                if i == num:
                    output += "▧"*(i) + "☒" + "▧"*(i) + '\n'
                else:
                    output += "☐"*(num-i) + "▧"*(i*2+1) + "☐"*(num-i) + '\n'
            for i in range(num-1, -1, -1):
                output += "☐"*(num-i) + "▧"*(i*2+1) + "☐"*(num-i) + '\n'
            await msg.channel.send('```\n' + output + '```')

    @commands.command()
    async def lethal(self, ctx, *, info):
        '''To use the lethal calculator, follow the format" `!lethal [HP] [terrain]`'''

        global message_out, message_embed, terrain_names, co_hp, co_terrain, attacker_arr
        attacker_arr = []

        # error checking
        info_split = info.split(' ')
        if len(info_split) != 2:
            await ctx.send('To use the lethal calculator, follow the format" `!lethal [HP] [terrain]`')
            return
        if (info_split[0].isdigit() == False) or int(info_split[0]) > 100 or int(info_split[0]) < 0:
            await ctx.send('Please enter a valid HP')
            return
        if info_split[1] not in terrain_names:
            await ctx.send('Please enter a valid terrain')
            return
        
        co_hp = int(info_split[0])
        co_terrain = info_split[1]

        message_embed = discord.Embed(title = info_split[0] + '% HP commander on ' + info_split[1].capitalize())
        message_out = await ctx.send(embed=message_embed)
    
    @commands.command(pass_context=True)
    async def add_attacker(self, ctx, *, info):
        '''Use the format: "!add_attacker [unit] [HP] [direction] [crit]"
            For direction specify all directions you can attack from: (N)orth (E)ast (S)outh (W)est or if it is a (R)anged attack
            For crit you can write "crit" or "true" if the unit is able to crit. If it can\'t then leave it blank or write "false".
            An example of a valid input would be ""!add_attacker cavalry 83 SW crit"'''

        global message_out, message_embed, unit_names, attacker_arr, co_damage_list, crit_multiplier

        # error checking
        info_split = info.lower().split(' ')
        if len(info_split) != 3 and len(info_split) != 4:
            await ctx.send('To add an attacker, follow the format" `!add_attacker [unit] [HP] [direction] [crit]`. For more info use `!help add_attacker`.')
        elif info_split[0] not in unit_names:
            unit_names_str = ''
            for name in unit_names:
                unit_names_str += name + ', '
            await ctx.send('Please enter a valid attacker: `' + unit_names_str[:-2] + '`')
            return
        elif (info_split[1].isdigit() == False) or int(info_split[1]) > 100 or int(info_split[1]) < 0:
            await ctx.send('Please enter a valid HP')
            return
        elif ('n' not in info_split[2]
        and 'e' not in info_split[2]
        and 's' not in info_split[2]
        and 'w' not in info_split[2]
        and 'r' not in info_split[2]):
            await ctx.send('Please enter valid cardinal directions or ranged')
            return

        await ctx.message.delete()

        if 'r' in info_split[2]:
            info_split[2] = 'r'

        damage = (int(info_split[1]) * .01) * co_damage_list[unit_names.index(info_split[0])]
        if len(info_split) == 4 and (info_split[3] == 'crit' or info_split[3] == 'true'):
            damage *= crit_multiplier[unit_names.index(info_split[0])]

        message_embed.add_field(
            name = info_split[1] + '% HP ' + info_split[0].capitalize() + ' attacking from ' + info_split[2].upper(),
            value = 'Capable of dealing ' + str(round(damage, 2)) + '% (not including terrain)',
            inline = False
        )
        attacker = [info_split[0], info_split[1], info_split[2], damage]
        attacker_arr.append(attacker)

        await message_out.edit(embed=message_embed)

    @commands.command(pass_context=True)
    async def remove_attacker(self, ctx, *, index):
        global message_out, message_embed, attacker_arr

        # error checking
        if int(index) > len(attacker_arr) or int(index) < 1:
            await ctx.send('Invalid index')
            return

        await ctx.message.delete()

        message_embed.remove_field(int(index) - 1)
        await message_out.edit(embed = message_embed)
        attacker_arr.pop(int(index) - 1)

    @commands.command()
    async def print_attackers(self, ctx):
        global attacker_arr
        await ctx.send(attacker_arr)

    @commands.command()
    async def calculate_lethal(self, ctx):
        # function will need to work like this:
        #   √ sort attackers by damage
        #   use least occurrent cardinal direction
        #       if there is a tie for least occurrence then find which of the tie is less damage
        #   attack from that direction, remove it option
        #   continue until entire array is parsed

        global attacker_arr, co_hp, co_terrain

        sorted_arr = attacker_arr
        sorted_arr = sorted(sorted_arr, key=lambda attacker: attacker[3], reverse=True)

        # count the cardinal directions
        n_count, e_count, s_count, w_count = 0, 0, 0, 0
        for attacker in sorted_arr:
            if 'n' in attacker[2]:
                n_count += 1
            if 'e' in attacker[2]:
                e_count += 1
            if 's' in attacker[2]:
                s_count += 1
            if 'w' in attacker[2]:
                w_count += 1

        def get_count(char):
            if char == 'n':
                return n_count
            if char == 'e':
                return e_count
            if char == 's':
                return s_count
            if char == 'w':
                return w_count
            if char == 'r':
                return 0

        print('n_count: ' + str(n_count))
        print('e_count: ' + str(e_count))
        print('s_count: ' + str(s_count))
        print('w_count: ' + str(w_count))

        final_hp_lucky = co_hp
        final_hp_unlucky = co_hp
        story = ''
        # find least occurrence and perform attack
        for attacker in sorted_arr:
            least_direction = attacker[2][:1]
            # gets the least occurring cardinal direction
            for char in attacker[2][1:]:
                if get_count(char) < get_count(least_direction) and get_count(least_direction) > 0:
                    least_direction = char
                elif get_count(char) == get_count(least_direction):
                    # TO-DO check which occurrence is further for char and least_direction
                    ctx.send('You found the edge case I need to fix')
            # attack from that side
            if get_count(least_direction) > 0 or least_direction == 'r':
                story += attacker[1] + '% HP ' + attacker[0] + ' attack from ' + least_direction.upper() + '\n'
                terrain = terrain_defense[terrain_names.index(co_terrain)]
                final_hp_lucky -= (attacker[3] *  (1 - ((terrain * 0.1) * (final_hp_lucky * 0.01)))) + (5 * int(attacker[1]) * 0.01)
                final_hp_unlucky -= (attacker[3] *  (1 - ((terrain * 0.1) * (final_hp_unlucky * 0.01)))) - (5 * int(attacker[1]) * 0.01)

        print(final_hp_lucky)
        print(final_hp_unlucky)

        if final_hp_lucky <= 0 and final_hp_unlucky <= 0:
            await ctx.send('It is impossible to not have lethal if you:\n' + story)
        elif final_hp_lucky <= 0 and final_hp_unlucky > 0:
            hp_range = abs(final_hp_unlucky - final_hp_lucky)
            await ctx.send('You have a ' + str(round(abs(final_hp_lucky / hp_range) * 100, 2)) + '% chance of lethal if you:\n' + story)
        else:
            await ctx.send('Even with good RNG you do not have lethal')