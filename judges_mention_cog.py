import json
import datetime
import logging

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
user_id_for_send_logs = int(cfg["user_id_for_send_logs"])

async def send_logs(time: str, thread_url: str, judges_mention: list):
    judges_mention_names = ""

    for member in judges_mention:
        judges_mention_names += f"{member.name} : {member.id}\n"

    logging.info(f"Создание нового обжалования")
    logging.info(f"время: {time}, ссылка на публикацию: {thread_url}")
    logging.info(f"было упомянуто: {len(judges_mention)} судей")
    logging.info(f"список упомянутых судей:\n{judges_mention_names}")

async def get_nicknames_without_vacation(members_with_judge: list, vacation_role_id: int) -> list:
    """ 
        Returns nicknames list without vacation
    """
    nicknames_without_vacation = []

    if not members_with_judge:
        return nicknames_without_vacation

    for member in members_with_judge:
        role_ids = {role.id for role in member.roles}
        if vacation_role_id not in role_ids:
            nicknames_without_vacation.append(member.id)

    return nicknames_without_vacation

async def get_members_without_vacation(members_with_judge: list, vacation_role_id: int) -> list:
    """ 
        Returns members list without vacation
    """
    members_without_vacation = []

    if not members_with_judge:
        return members_without_vacation

    for member in members_with_judge:
        role_ids = {role.id for role in member.roles}
        if vacation_role_id not in role_ids:
            members_without_vacation.append(member)

    return members_without_vacation

logging.basicConfig(level=logging.INFO)

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

        if (not members_with_judge): 
            logging.warning("Пользователей с ролью судья не обнаружено")
            return

        mentions = "Пинг судей: "
        members_list = []

        if (mention_on_vacation):
            for member in members_with_judge:
                mentions += f"<@{member.id}> "
                members_list.append(member)
        else:
            without_vacation = await get_nicknames_without_vacation(members_with_judge, vacation_role_id)
            members_list = await get_members_without_vacation(members_with_judge, vacation_role_id)

            if (not without_vacation): return
            for id in without_vacation:
                mentions += f"<@{id}> "
        
        await thread.send(mentions)

        thread_url = thread.jump_url
        await send_logs(datetime.datetime.now(), thread_url, members_list)