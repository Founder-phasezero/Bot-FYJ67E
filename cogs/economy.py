import discord
from discord.ext import commands
import json
import os
import random

BALANCE_FILE = "balances.json"

# Ensure balance JSON exists
if not os.path.exists(BALANCE_FILE):
    with open(BALANCE_FILE, "w") as f:
        json.dump({}, f)

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_balances()

    def load_balances(self):
        with open(BALANCE_FILE, "r") as f:
            self.balances = json.load(f)

    def save_balances(self):
        with open(BALANCE_FILE, "w") as f:
            json.dump(self.balances, f, indent=4)

    def get_balance(self, user_id):
        return self.balances.get(str(user_id), 0)

    def update_balance(self, user_id, amount):
        user_id = str(user_id)
        self.balances[user_id] = self.balances.get(user_id, 0) + amount
        self.save_balances()

    def set_balance(self, user_id, amount):
        self.balances[str(user_id)] = amount
        self.save_balances()

    def delete_balance(self, user_id):
        self.balances.pop(str(user_id), None)
        self.save_balances()

    # ---------------- USER COMMANDS ----------------
    @discord.app_commands.command(name="balance", description="Check your balance")
    async def balance(self, interaction: discord.Interaction):
        bal = self.get_balance(interaction.user.id)
        await interaction.response.send_message(f"💰 {interaction.user.mention}, your balance is {bal} coins.")

    @discord.app_commands.command(name="daily", description="Claim your daily coins")
    async def daily(self, interaction: discord.Interaction):
        daily_amount = 100
        self.update_balance(interaction.user.id, daily_amount)
        await interaction.response.send_message(f"🎁 {interaction.user.mention}, you claimed {daily_amount} coins!")

    @discord.app_commands.command(name="pay", description="Pay coins to another user")
    async def pay(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        if amount <= 0:
            await interaction.response.send_message("❌ Amount must be greater than 0.")
            return
        if self.get_balance(interaction.user.id) < amount:
            await interaction.response.send_message("❌ You don't have enough coins.")
            return
        self.update_balance(interaction.user.id, -amount)
        self.update_balance(member.id, amount)
        await interaction.response.send_message(f"💸 {interaction.user.mention} paid {amount} coins to {member.mention}.")

    # ---------------- ADMIN COMMANDS ----------------
    @discord.app_commands.command(name="addmoney", description="Add coins to a user (Admin only)")
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def addmoney(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        self.update_balance(member.id, amount)
        await interaction.response.send_message(f"✅ Added {amount} coins to {member.mention}.")

    @discord.app_commands.command(name="setmoney", description="Set a user's balance (Admin only)")
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def setmoney(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        self.set_balance(member.id, amount)
        await interaction.response.send_message(f"✅ Set {member.mention}'s balance to {amount} coins.")

    @discord.app_commands.command(name="delmoney", description="Delete a user's balance (Admin only)")
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def delmoney(self, interaction: discord.Interaction, member: discord.Member):
        self.delete_balance(member.id)
        await interaction.response.send_message(f"🗑️ Deleted {member.mention}'s balance.")

    # You can keep all your other commands (shop, buy, gamble, rob, etc.) as-is

async def setup(bot):
    await bot.add_cog(Economy(bot))
