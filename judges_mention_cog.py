import json

import discord
from discord.ext import commands

with open("./config/config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

appeal_channel_id = int(cfg["appeal_channel_id"])
guild_id = int(cfg["guild_id"])

enable_mention = bool(cfg["enable_mention"])
mention_on_vacation = bool(cfg["mention_on_vacation"])

judge_role_id = int(cfg["judge_role_id"])
vacation_role_id = int(cfg["vacation_role_id"])

async def get_without_vacation(members_with_judge: list, vacation_role_id: int):
    nicknames_without_vacation = []

    if not members_with_judge:
        return nicknames_without_vacation

    for member in members_with_judge:
        role_ids = {role.id for role in member.roles}
        if vacation_role_id not in role_ids:
            nicknames_without_vacation.append(member.id)

    return nicknames_without_vacation

class JudgesMentionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        """
            This event is triggered when someone creates a post in the forum.
        """

        if (not enable_mention): return
        if (not isinstance(thread.parent, discord.ForumChannel)): return
        if (thread.parent.id != appeal_channel_id): return

        guild = self.bot.get_guild(guild_id)
        judge_role = guild.get_role(judge_role_id)
        members_with_judge = [member for member in guild.members if judge_role in member.roles]

        if (not members_with_judge): return

        mentions = "Пинг судей: "
        if (mention_on_vacation):
            for member in members_with_judge:
                mentions += f"<@{member.id}> "
        else:
            without_vacation = await get_without_vacation(members_with_judge, vacation_role_id)

            if (not without_vacation): return
            for id in without_vacation:
                mentions += f"<@{id}> "
        
        await thread.send(mentions)