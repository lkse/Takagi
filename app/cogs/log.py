import discord
from discord.ext import commands
from ..config import database, config
from ..logger import log
from typing import Optional, List, Union
from datetime import datetime

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_guild(self, guild: discord.Guild):
        query = "SELECT * FROM GUILDS WHERE GID = ?"
        resp = await database.fetch_one(query, guild.id)
        if not resp:
            async with database.transaction() as transaction:
                query = "INSERT INTO GUILDS (GID) VALUES (?)"
                try:
                    await database.execute(query, guild.id)
                except Exception as e:
                    await transaction.rollback()
                    log.error(f"Guild Creation Error: {e} GID: {guild.id}")
                else:
                    await transaction.commit()
                    log.debug(f"Guild Inserted: {guild.id}")
        if resp['Blacklisted']:
            return 0
        elif resp['LogChannel']:
                channel = guild.get_channel(resp['LogChannel'])
                if not channel:
                    async with database.transaction() as transaction:
                        query = "UPDATE GUILDS SET LogChannel = NULL WHERE GID = ?"
                        try:
                            await database.execute(query, guild.id)
                        except Exception as e:
                            await transaction.rollback()
                            log.error(f"Channel Unlink Error: {e} GID: {guild.id}")
                        else:
                            await transaction.commit()
                            log.debug(f"Channel Unlinked: {guild.id}")
                            return None
                else:
                    return channel
    
    @commands.Cog.listener()
    async def on_automod_rule_create(self, rule: discord.AutoModRule): # https://discordpy.readthedocs.io/en/stable/api.html?highlight=event#discord.on_automod_rule_create
        logchannel = await self.check_guild(rule.guild.id)
        if logchannel:
            enabled = "Enabled" if rule.enabled else "Disabled"
            action = "automod_rule_create"
            message = f"@silent <@{rule.creator_id}> created the automod rule {rule.name}. I'ts Triggered by {rule.trigger} and the action is {rule.action}. the rule is currently {enabled}"
            embed = discord.Embed(title=f"{action}",
                      description=f"Actions: {rule.actions}\nCreator: {rule.creator}\nCreator ID: {rule.creator_id}\nStatus: {enabled}\nEvent Type: {rule.event_type}\nExempt Channel IDs: {rule.exempt_channel_ids}\nExempt Channels: {rule.exempt_channels}\nExempt Role IDs: {rule.exempt_role_ids}\nExempt Roles: {rule.exempt_roles}\nID: {rule.id}\nName: {rule.name}\nTrigger: {rule.trigger}",
                      colour=0x000000,
                      timestamp=datetime.now())

            embed.set_author(name="Logs")

            embed.set_thumbnail(url=f"{rule.creator.avatar.url}")

            embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")
            await logchannel.send(content=message, embed=embed)

    @commands.Cog.listener()
    async def on_automod_rule_update(self, rule: discord.AutoModRule): # https://discordpy.readthedocs.io/en/stable/api.html?highlight=event#discord.on_automod_rule_update
        logchannel = await self.check_guild(rule.guild.id)
        if logchannel:
            enabled = "Enabled" if rule.enabled else "Disabled"
            action = "automod_rule_update"
            message = f"@silent <@{rule.creator_id}> updated the automod rule {rule.name}. I'ts Triggered by {rule.trigger} and the action is {rule.action}. the rule is currently {enabled}"
            embed = discord.Embed(title=f"{action}",
                      description=f"Actions: {rule.actions}\nCreator: {rule.creator}\nCreator ID: {rule.creator_id}\nStatus: {enabled}\nEvent Type: {rule.event_type}\nExempt Channel IDs: {rule.exempt_channel_ids}\nExempt Channels: {rule.exempt_channels}\nExempt Role IDs: {rule.exempt_role_ids}\nExempt Roles: {rule.exempt_roles}\nID: {rule.id}\nName: {rule.name}\nTrigger: {rule.trigger}",
                      colour=0x000000,
                      timestamp=datetime.now())

            embed.set_author(name="Logs")

            embed.set_thumbnail(url=f"{rule.creator.avatar.url}")

            embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")
            await logchannel.send(content=message, embed=embed)

    @commands.Cog.listener()
    async def on_automod_rule_delete(self, rule: discord.AutoModRule): # https://discordpy.readthedocs.io/en/stable/api.html?highlight=event#discord.on_automod_rule_delete
        logchannel = await self.check_guild(rule.guild.id)
        if logchannel:
            enabled = "Enabled" if rule.enabled else "Disabled"
            action = "automod_rule_delete"
            message = f"@silent <@{rule.creator_id}> deleted the automod rule {rule.name}. I'ts Triggered by {rule.trigger} and the action is {rule.action}. the rule is currently {enabled}"
            embed = discord.Embed(title=f"{action}",
                      description=f"Actions: {rule.actions}\nCreator: {rule.creator}\nCreator ID: {rule.creator_id}\nStatus: {enabled}\nEvent Type: {rule.event_type}\nExempt Channel IDs: {rule.exempt_channel_ids}\nExempt Channels: {rule.exempt_channels}\nExempt Role IDs: {rule.exempt_role_ids}\nExempt Roles: {rule.exempt_roles}\nID: {rule.id}\nName: {rule.name}\nTrigger: {rule.trigger}",
                      colour=0x000000,
                      timestamp=datetime.now())

            embed.set_author(name="Logs")

            embed.set_thumbnail(url=f"{rule.creator.avatar.url}")

            embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")
            await logchannel.send(content=message, embed=embed)
    
    @commands.Cog.listener()
    async def on_automod_action(self, execution: discord.AutoModAction): # https://discordpy.readthedocs.io/en/stable/api.html?highlight=event#discord.on_automod_action
        logchannel = await self.check_guild(execution.guild.id)
        if logchannel:
            action_type = "automod_action"
            message = f"@silent AutoMod action taken against <@{execution.user_id}> due to triggered rule ID {execution.rule_id} in <#{execution.channel_id}>.\nTriggered by keyword: {execution.matched_keyword or 'N/A'}, Content: {execution.matched_content or 'N/A'}"

            embed = discord.Embed(
                title=f"{action_type}",
                description=f"Action: {execution.action}\nGuild: {execution.guild}\nGuild ID: {execution.guild_id}\nChannel: {execution.channel}\nChannel ID: {execution.channel_id}\nUser ID: {execution.user_id}\nMember: {execution.member}\nRule ID: {execution.rule_id}\nRule Trigger Type: {execution.rule_trigger_type}\nMessage ID: {execution.message_id or 'N/A'}\nAlert System Message ID: {execution.alert_system_message_id or 'N/A'}\nContent: {execution.content or 'N/A'}\nMatched Keyword: {execution.matched_keyword or 'N/A'}\nMatched Content: {execution.matched_content or 'N/A'}",
                colour=0x000000,
                timestamp=datetime.now()
            )

            embed.set_author(name="Logs")
            embed.set_thumbnail(url=f"{execution.member.avatar.url if execution.member else ''}")
            embed.set_footer(text="Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")

            await logchannel.send(content=message, embed=embed)


    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel): # https://discordpy.readthedocs.io/en/stable/api.html?highlight=event#discord.on_guild_channel_create
        logchannel = await self.check_guild(channel.guild.id)
        if logchannel:
            action_type = "guild_channel_create"
            message = f"@silent New channel created: {channel.mention} (Name: {channel.name}) in guild: {channel.guild}.\nPosition: {channel.position}, Category: {channel.category or 'None'}\nJump URL: {channel.jump_url}"

            embed = discord.Embed(
                title=f"{action_type}",
                description=f"Name: {channel.name}\nGuild: {channel.guild}\nPosition: {channel.position}\nCategory: {channel.category or 'None'}\nMention: {channel.mention}\nJump URL: {channel.jump_url}\nCreated At: {channel.created_at}\nPermissions Synced: {channel.permissions_synced}\nChanged Roles: {channel.changed_roles}\nOverwrites: {channel.overwrites}",
                colour=0x000000,
                timestamp=datetime.now()
            )

            embed.set_author(name="Logs")
            embed.set_footer(text="Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")

            await logchannel.send(content=message, embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel): # https://discordpy.readthedocs.io/en/stable/api.html?highlight=event#discord.on_guild_channel_delete
        logchannel = await self.check_guild(channel.guild.id)
        if logchannel:
            action_type = "guild_channel_delete"
            message = f"@silent Channel Deleted: (Name: {channel.name}) in guild: {channel.guild}.\nPosition: {channel.position}, Category: {channel.category or 'None'}\nJump URL: {channel.jump_url}"
        
            embed = discord.Embed(
                title=f"{action_type}",
                description=f"Name: {channel.name}\nGuild: {channel.guild}\nPosition: {channel.position}\nCategory: {channel.category or 'None'}\nMention: {channel.mention}\nJump URL: {channel.jump_url}\nCreated At: {channel.created_at}\nPermissions Synced: {channel.permissions_synced}\nChanged Roles: {channel.changed_roles}\nOverwrites: {channel.overwrites}",
                colour=0x000000,
                timestamp=datetime.now()
            )
        
            embed.set_author(name="Logs")
            embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")
        
            await logchannel.send(content=message, embed=embed)


    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel): # https://discordpy.readthedocs.io/en/stable/api.html?highlight=event#discord.on_guild_channel_update
        before_dict = before.__dict__
        after_dict = after.__dict__

        differences = {key: (before_dict[key], after_dict[key]) for key in before_dict if key in after_dict and before_dict[key] != after_dict[key]}
        # {key: (before, after)}

        logchannel = await self.check_guild(after.guild.id)
        if logchannel:
            action_type = "guild_channel_update"
            message = "@silent Channel updated: {after.mention} (ID: {after.id})\nChanges:\n" + "\n".join([f"{key.capitalize()}: {before} ➔ {after}" for key, (before, after) in differences.items()])

            embed = discord.Embed(
                title=f"{action_type}",
                description=f"Channel updated in guild: {after.guild}\nChanges:\n" + "\n".join([f"{key.capitalize()}: {before} ➔ {after}" for key, (before, after) in differences.items()]),
                colour=0x000000,
                timestamp=datetime.now()
            )

            embed.set_author(name="Logs")
            embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")

            await logchannel.send(content=message, embed=embed)


    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        before_dict = before.__dict__
        after_dict = after.__dict__

        differences = {key: (before_dict[key], after_dict[key]) for key in before_dict if key in after_dict and before_dict[key] != after_dict[key]}
        # {key: (before, after)}
        logchannel = await self.check_guild(after.guild.id)
        if logchannel:
            action_type = "guild_update"
            message = f"@silent Guild updated: {after.name} (ID: {after.id})\nChanges:\n" + "\n".join([f"{key.capitalize()}: {before} ➔ {after}" for key, (before, after) in differences.items()])

            embed = discord.Embed(
                title=f"{action_type}",
                description=f"Guild updated: {after.name}\nID: {after.id}\nChanges:\n" + "\n".join([f"{key.capitalize()}: {before} ➔ {after}" for key, (before, after) in differences.items()]),
                colour=0x000000,
                timestamp=datetime.now()
            )

            embed.set_author(name="Logs")
            embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")

            await logchannel.send(content=message, embed=embed)


    @commands.Cog.listener()
    async def on_invite_create(self, invite: discord.Invite): # https://discordpy.readthedocs.io/en/stable/api.html?highlight=event#discord.on_invite_create
        logchannel = await self.check_guild(invite.guild.id)
        if logchannel:
            action_type = "invite_create"
            message = f"@silent <@{invite.inviter.id}> created an invite for {invite.guild.name} ({invite.code}).\nChannel: {invite.channel.mention}\nExpires At: {invite.expires_at or 'Never'}\nTemporary: {'Yes' if invite.temporary else 'No'}\nMax Uses: {invite.max_uses or 'Unlimited'}"

            embed = discord.Embed(
                title=f"{action_type}",
                description=f"Code: {invite.code}\nGuild: {invite.guild.name}\nChannel: {invite.channel.mention}\nCreated At: {invite.created_at}\nExpires At: {invite.expires_at or 'Never'}\nInviter: {invite.inviter}\nMax Age: {invite.max_age or 'Unlimited'}\nMax Uses: {invite.max_uses or 'Unlimited'}\nTemporary: {'Yes' if invite.temporary else 'No'}\nTarget User: {invite.target_user or 'N/A'}\nTarget Application: {invite.target_application or 'N/A'}\nURL: {invite.url}\nScheduled Event: {invite.scheduled_event or 'N/A'}",
                colour=0x000000,
                timestamp=datetime.now()
            )

            embed.set_author(name="Logs")
            embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")

            await logchannel.send(content=message, embed=embed)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite: discord.Invite): # https://discordpy.readthedocs.io/en/stable/api.html?highlight=event#discord.on_invite_delete
        logchannel = await self.check_guild(invite.guild.id)
        if logchannel:
            action_type = "invite_delete"
            message = f"@silent The invite with code {invite.code} for {invite.guild.name} was deleted.\nChannel: {invite.channel.mention}"

            embed = discord.Embed(
                title=f"{action_type}",
                description=f"Code: {invite.code}\nGuild: {invite.guild.name}\nChannel: {invite.channel.mention}\nCreated At: {invite.created_at}\nExpires At: {invite.expires_at or 'Never'}\nInviter: {invite.inviter}\nMax Age: {invite.max_age or 'Unlimited'}\nMax Uses: {invite.max_uses or 'Unlimited'}\nTemporary: {'Yes' if invite.temporary else 'No'}\nTarget User: {invite.target_user or 'N/A'}\nTarget Application: {invite.target_application or 'N/A'}\nScheduled Event: {invite.scheduled_event or 'N/A'}",
                colour=0x000000,
                timestamp=datetime.now()
            )

            embed.set_author(name="Logs")
            embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")

            await logchannel.send(content=message, embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        logchannel = await self.check_guild(member.guild.id)
        if logchannel:
            action_type = "member_join"
            message = f"@silent {member.mention} has joined the server."

            embed = discord.Embed(
                title=f"{action_type}",
                description=f"Member: {member.mention}\nName: {member.name}\nID: {member.id}\nJoined At: {member.joined_at}\nGuild: {member.guild.name}\nAccount Created At: {member.created_at}",
                colour=0x000000,
                timestamp=datetime.now()
            )

            embed.set_author(name="Logs")
            embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")

            await logchannel.send(content=message, embed=embed)

        
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member): # https://discordpy.readthedocs.io/en/stable/api.html?highlight=event#discord.on_member_remove
        logchannel = await self.check_guild(member.guild.id)
        if logchannel:
            action_type = "member_remove"
            message = f"@silent {member.mention} has left the server."

            embed = discord.Embed(
                title=f"{action_type}",
                description=f"Member: {member.mention}\nName: {member.name}\nID: {member.id}\nGuild: {member.guild.name}\nJoined At: {member.joined_at}\nAccount Created At: {member.created_at}",
                colour=0x000000,
                timestamp=datetime.now()
            )

            embed.set_author(name="Logs")
            embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")

            await logchannel.send(content=message, embed=embed)


    @commands.Cog.listener()
    async def on_member_update(self, before:discord.Member, after:discord.Member): # https://discordpy.readthedocs.io/en/stable/api.html?highlight=event#discord.on_member_update
        before_dict = before.__dict__
        after_dict = after.__dict__

        differences = {key: (before_dict[key], after_dict[key]) for key in before_dict if key in after_dict and before_dict[key] != after_dict[key]}
        # {key: (before, after)}
        logchannel = await self.check_guild(after.guild.id)
        if logchannel:
            action_type = "member_update"
            message = f"@silent {after.mention}'s profile has been updated.\nChanges:\n" + "\n".join([f"{key.capitalize()}: {before} ➔ {after}" for key, (before, after) in differences.items()])

            embed = discord.Embed(
                title=f"{action_type}",
                description=f"Member: {after.mention}\nName: {after.name}\nID: {after.id}\nGuild: {after.guild.name}\nChanges:\n" + "\n".join([f"{key.capitalize()}: {before} ➔ {after}" for key, (before, after) in differences.items()]),
                colour=0x000000,
                timestamp=datetime.now()
            )

            embed.set_author(name="Logs")
            embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")

            await logchannel.send(content=message, embed=embed)

        
    @commands.Cog.listener()
    async def on_user_update(self, before: discord.Member, after: discord.Member): # https://discordpy.readthedocs.io/en/stable/api.html?highlight=event#discord.on_user_update
        before_dict = before.__dict__
        after_dict = after.__dict__

        differences = {key: (before_dict[key], after_dict[key]) for key in before_dict if key in after_dict and before_dict[key] != after_dict[key]}
        # {key: (before, after)}
        logchannel = await self.check_guild(after.guild.id)
        if logchannel:
            action_type = "user_update"
            message = f"@silent {after.mention}'s profile has been updated.\nChanges:\n" + "\n".join([f"{key.capitalize()}: {before} ➔ {after}" for key, (before, after) in differences.items()])

            embed = discord.Embed(
                title=f"{action_type}",
                description=f"User: {after.mention}\nName: {after.name}\nID: {after.id}\nGuild: {after.guild.name}\nChanges:\n" + "\n".join([f"{key.capitalize()}: {before} ➔ {after}" for key, (before, after) in differences.items()]),
                colour=0x000000,
                timestamp=datetime.now()
            )

            embed.set_author(name="Logs")
            embed.set_footer(text="Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")

            await logchannel.send(content=message, embed=embed)
    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: Union[discord.User | discord.Member]): # https://discordpy.readthedocs.io/en/stable/api.html?highlight=event#discord.on_member_ban
        logchannel = await self.check_guild(guild.id)
        if logchannel:
            action_type = "member_ban"
            message = f"@silent {user.mention} has been banned from {guild.name}."
        
            embed = discord.Embed(
                title=f"{action_type}",
                description=f"User: {user.mention}\nName: {user.name}\nID: {user.id}\nGuild: {guild.name}\nBanned At: {datetime.now()}",
                colour=0x000000,
                timestamp=datetime.now()
            )
        
            embed.set_author(name="Logs")
            embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")
        
            await logchannel.send(content=message, embed=embed)


    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user:discord.User): # https://discordpy.readthedocs.io/en/stable/api.html?highlight=event#discord.on_member_unban
        logchannel = await self.check_guild(guild.id)
        if logchannel:
            action_type = "member_unban"
            message = f"@silent {user.mention} has been unbanned from {guild.name}."

            embed = discord.Embed(
                title=f"{action_type}",
                description=f"User: {user.mention}\nName: {user.name}\nID: {user.id}\nGuild: {guild.name}\nUnbanned At: {datetime.now()}",
                colour=0x000000,
                timestamp=datetime.now()
            )

            embed.set_author(name="Logs")
            embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")

            await logchannel.send(content=message, embed=embed)


    #@commands.Cog.listener()
    #async def on_presence_update(self, before: discord.Member, after: discord.Member):
    #    before_dict = before.__dict__
    #    after_dict = after.__dict__
#
    #    differences = {key: (before_dict[key], after_dict[key]) for key in before_dict if key in after_dict and before_dict[key] != after_dict[key]}
    #    # {key: (before, after)}
    #    logchannel = await self.check_guild(after.guild.id)
    #    if logchannel:
    #        action_type = "presence_update"
    #        message = f"@silent {after.mention}'s presence has been updated.\nChanges:\n" + "\n".join([f"{key.capitalize()}: {before} ➔ {after}" for key, (before, after) in differences.items()])
#
    #        embed = discord.Embed(
    #            title=f"{action_type}",
    #            description=f"Member: {after.mention}\nName: {after.name}\nID: {after.id}\nGuild: {after.guild.name}\nChanges:\n" + "\n".join([f"{key.capitalize()}: {before} ➔ {after}" for key, (before, after) in differences.items()]),
    #            colour=0x000000,
    #            timestamp=datetime.now()
    #        )
#
    #        embed.set_author(name="Logs")
    #        embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")
#
    #        await logchannel.send(content=message, embed=embed)

    @commands.Cog.listener()
    async def on_messsage_edit(self, before: discord.Message, after:discord.Message): # https://discordpy.readthedocs.io/en/stable/api.html?highlight=event#discord.on_message_edit
        before_dict = before.__dict__
        after_dict = after.__dict__

        differences = {key: (before_dict[key], after_dict[key]) for key in before_dict if key in after_dict and before_dict[key] != after_dict[key]}
        # {key: (before, after)}
        logchannel = await self.check_guild(after.guild.id)
        if logchannel:
            action_type = "message_edit"
            message = f"@silent A message was edited in {after.guild.name}.\nChanges:\n" + "\n".join([f"{key.capitalize()}: {before} ➔ {after}" for key, (before, after) in differences.items()])

            embed = discord.Embed(
                title=f"{action_type}",
                description=f"Message by: {after.author.mention}\nChannel: {after.channel.name}\nID: {after.id}\nGuild: {after.guild.name}\nEdited At: {datetime.now()}\nChanges:\n" + "\n".join([f"{key.capitalize()}: {before} ➔ {after}" for key, (before, after) in differences.items()]),
                colour=0x000000,
                timestamp=datetime.now()
            )

            embed.set_author(name="Logs")
            embed.set_footer(text="Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")

            await logchannel.send(content=message, embed=embed)


    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message): # https://discordpy.readthedocs.io/en/stable/api.html?highlight=event#discord.on_message_delete
        logchannel = await self.check_guild(message.guild.id)
        if logchannel:
            action_type = "message_delete"
            message_content = message.clean_content if message.clean_content else "No content"

            embed = discord.Embed(
                title=f"{action_type}",
                description=f"Message by: {message.author.mention}\nChannel: {message.channel.name}\nContent: {message_content}\nID: {message.id}\nGuild: {message.guild.name}\nDeleted At: {datetime.now()}",
                colour=0x000000,
                timestamp=datetime.now()
            )

            embed.set_author(name="Logs")
            embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")

            await logchannel.send(content=f"@silent A message was deleted in {message.guild.name}.", embed=embed)


    @commands.Cog.listener()
    async def on_poll_add(self, user: Union[discord.User, discord.Member], answer: discord.PollAnswer):
        logchannel = await self.check_guild(answer.guild.id)
        if logchannel:
            action = "poll_add"
            message = f"@silent <@{user.id}> added an answer to the poll {answer.poll.id}. The answer text is '{answer.text}' and it has {answer.vote_count} votes."
            embed = discord.Embed(title=f"{action}",
                                  description=f"Answer ID: {answer.id}\nText: {answer.text}\nEmoji: {answer.emoji}\nVote Count: {answer.vote_count}\nSelf Voted: {answer.self_voted}\nMedia: {answer.media}\nPoll ID: {answer.poll.id}",
                                  colour=0x000000,
                                  timestamp=datetime.now())
    
            embed.set_author(name="Logs")
    
            embed.set_thumbnail(url=f"{user.avatar.url}")
    
            embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")
    
            await logchannel.send(content=message, embed=embed)
    @commands.Cog.listener()
    async def on_poll_remove(self, user: Union[discord.User, discord.Member], answer: discord.PollAnswer):
        logchannel = await self.check_guild(answer.guild.id)
        if logchannel:
            action = "poll_remove"
            message = f"@silent <@{user.id}> removed an answer from the poll {answer.poll.id}. The answer text was '{answer.text}' and it had {answer.vote_count} votes."
            embed = discord.Embed(title=f"{action}",
                                  description=f"Answer ID: {answer.id}\nText: {answer.text}\nEmoji: {answer.emoji}\nVote Count: {answer.vote_count}\nSelf Voted: {answer.self_voted}\nMedia: {answer.media}\nPoll ID: {answer.poll.id}",
                                  colour=0x000000,
                                  timestamp=datetime.now())
    
            embed.set_author(name="Logs")
    
            embed.set_thumbnail(url=f"{user.avatar.url}")
    
            embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")
    
            await logchannel.send(content=message, embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        logchannel = await self.check_guild(role.guild.id)
        if logchannel:
            action = "guild_role_create"
            message = f"@silent A new role '{role.name}' was created in the guild."
            embed = discord.Embed(title=f"{action}",
                                  description=f"Role ID: {role.id}\nName: {role.name}\nGuild: {role.guild}\nHoist: {role.hoist}\nPosition: {role.position}\nUnicode Emoji: {role.unicode_emoji}\nManaged: {role.managed}\nMentionable: {role.mentionable}\nTags: {role.tags}\nPermissions: {role.permissions}\nColour: {role.colour}\nIcon: {role.icon}\nDisplay Icon: {role.display_icon}\nCreated At: {role.created_at}\nMention: {role.mention}\nMembers: {len(role.members)}\nFlags: {role.flags}",
                                  colour=0x000000,
                                  timestamp=datetime.now())
    
            embed.set_author(name="Logs")
    
            embed.set_thumbnail(url=f"{role.icon.url if role.icon else ''}")
    
            embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")
    
            await logchannel.send(content=message, embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        logchannel = await self.check_guild(role.guild.id)
        if logchannel:
            action = "guild_role_delete"
            message = f"@silent The role '{role.name}' was deleted from the guild."
            embed = discord.Embed(title=f"{action}",
                                  description=f"Role ID: {role.id}\nName: {role.name}\nGuild: {role.guild}\nHoist: {role.hoist}\nPosition: {role.position}\nUnicode Emoji: {role.unicode_emoji}\nManaged: {role.managed}\nMentionable: {role.mentionable}\nTags: {role.tags}\nPermissions: {role.permissions}\nColour: {role.colour}\nIcon: {role.icon}\nDisplay Icon: {role.display_icon}\nCreated At: {role.created_at}\nMention: {role.mention}\nMembers: {len(role.members)}\nFlags: {role.flags}",
                                  colour=0x000000,
                                  timestamp=datetime.now())
    
            embed.set_author(name="Logs")
    
            embed.set_thumbnail(url=f"{role.icon.url if role.icon else ''}")
    
            embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")
    
            await logchannel.send(content=message, embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        before_dict = before.__dict__
        after_dict = after.__dict__
    
        differences = {key: (before_dict[key], after_dict[key]) for key in before_dict if key in after_dict and before_dict[key] != after_dict[key]}
        # {key: (before, after)}
        logchannel = await self.check_guild(after.guild.id)
        if logchannel:
            action_type = "guild_role_update"
            message = f"@silent The role '{after.name}' was updated in {after.guild.name}.\nChanges:\n" + "\n".join([f"{key.capitalize()}: {before} ➔ {after}" for key, (before, after) in differences.items()])
    
            embed = discord.Embed(
                title=f"{action_type}",
                description=f"Role: {after.name}\nID: {after.id}\nGuild: {after.guild.name}\nUpdated At: {datetime.now()}\nChanges:\n" + "\n".join([f"{key.capitalize()}: {before} ➔ {after}" for key, (before, after) in differences.items()]),
                colour=0x000000,
                timestamp=datetime.now()
            )
    
            embed.set_author(name="Logs")
            embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")
    
            await logchannel.send(content=message, embed=embed)
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        before_dict = before.__dict__
        after_dict = after.__dict__
    
        differences = {key: (before_dict[key], after_dict[key]) for key in before_dict if key in after_dict and before_dict[key] != after_dict[key]}
        # {key: (before, after)}
        logchannel = await self.check_guild(after.guild.id)
    
        if logchannel:
            action_type = "voice_state_update"
            message = f"@silent {member.mention}'s voice state was updated in {after.guild.name}.\nChanges:\n" + "\n".join([f"{key.capitalize()}: {before} ➔ {after}" for key, (before, after) in differences.items()])
    
            embed = discord.Embed(
                title=f"{action_type}",
                description=f"Member: {member.mention}\nID: {member.id}\nGuild: {after.guild.name}\nUpdated At: {datetime.now()}\nChanges:\n" + "\n".join([f"{key.capitalize()}: {before} ➔ {after}" for key, (before, after) in differences.items()]),
                colour=0x000000,
                timestamp=datetime.now()
            )
    
            embed.set_author(name="Logs")
            embed.set_footer(text=f"Takagi v{config.VERSION} | by lkse", icon_url="https://lkse.pw/images/takagi.gif")
    
            await logchannel.send(content=message, embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        await database.connect()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith(config.DISCORD_PREFIX):
            command_body = message.content[len(config.DISCORD_PREFIX):].strip()
            command, *args = command_body.split()
            if command == 'setlogchannel':
                async with message.channel.typing():
                    if message.channel_mentions:
                        log_channel = message.channel_mentions[0]
                        guild_id = message.guild.id
                        # Check if guild exists in the database
                        query = "SELECT * FROM servers WHERE guild_id = :guild_id"
                        values = {"guild_id": guild_id}
                        guild = await database.fetch_one(query, values)
                        if guild is None:
                            # Insert new guild into the database
                            query = "INSERT INTO servers (guild_id, log_channel_id) VALUES (:guild_id, :log_channel_id)"
                            values = {"guild_id": guild_id, "log_channel_id": log_channel.id}
                            await database.execute(query, values)
                        else:
                            # Update existing guild's log channel
                            query = "UPDATE servers SET log_channel_id = :log_channel_id WHERE guild_id = :guild_id"
                            values = {"log_channel_id": log_channel.id, "guild_id": guild_id}
                            await database.execute(query, values)
                        await message.channel.send(f"Log channel set to {log_channel.mention}")
                    else:
                        await message.channel.send("Please mention a channel to set as the log channel.")
        


async def setup(bot):
    await bot.add_cog(Logging(bot))