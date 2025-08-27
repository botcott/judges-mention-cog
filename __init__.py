from .judges_mention_cog import JudgesMentionCog

def setup(bot):
    bot.add_cog(JudgesMentionCog(bot))