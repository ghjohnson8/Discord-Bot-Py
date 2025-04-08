from typing import Final

import discord
import choice_buttons

import yt_dlp
import os
import random

# This program runs the blackjack functionality
# Initial command triggers this script

async def main(message):
    await message.channel.send('🎲 We love blackjack! 🃏');
    await message.channel.send('Location: ' + str(message.channel) + '\nPlayer: ' + str(message.author));
    
    result = await start_choice(message);
    print(result);

    while True:
        if result == "start":
            await print_message(message.channel, "♠️ Starting game...");
            await blackjack_game(message);

        elif result == "exit":
            await print_message(message.channel, "🚪 Exitting...");
            return;
    
        again_result = await play_again(message);
        if again_result == "exit":
            return;
        elif again_result == "start":
            pass;

# Button functions - Reference choice_buttons.py
# Prompt Start Game - Used by main()
async def start_choice(message):
    view = choice_buttons.Start_Buttons();
    prompt_message = await message.channel.send("Start game?", view=view);
    await view.wait();  # Wait for user interaction

    await prompt_message.edit(content=f"You chose: {view.result.upper()}", view=None);  # Update message
    return view.result;  # Return the choice

# Prompt Hit Choice - Used by blackjack_game()
async def get_player_choice(message):
    view = choice_buttons.Hit_Buttons();
    prompt_message = await message.channel.send("Choose an action:", view=view);
    await view.wait();  # Wait for user interaction

    await prompt_message.edit(content=f"You chose: {view.result.upper()}", view=None);  # Update message
    return view.result;  # Return the choice

# Prompt Play Again Choice - Used by play_again()
async def get_play_again_choice(message):
    view = choice_buttons.Play_Again_Buttons();
    prompt_message = await message.channel.send("Choose an action:", view=view);
    await view.wait();  # Wait for user interaction

    await prompt_message.edit(content=f"You chose: {view.result.upper()}", view=None);  # Update message
    return view.result;  # Return the choice


# Basic print messsage function
async def print_message(location, String):
    await location.send(String);

# Blackjack game functions
# blackjack integrated with discord - 1 deck, 4 suits
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*4;

# Dealing deck function
def deal(deck):
    hand = [];
    for i in range(2):
        random.shuffle(deck);
        card = deck.pop();
        if card == 11:
            card = "J";
        elif card == 12:
            card = "Q";
        elif card == 13:
            card = "K";
        elif card == 14:
            card = "A";
        hand.append(card);
    return hand;

async def play_again(message):
    # Prompt if want to play again
    print_message(message.channel, "Do you want to play again? 🎲");

    # Call button function
    choice = await get_play_again_choice(message);
    
    return choice;

# Count hand total
def total(hand):
    total = 0;
    # Sum up non aces to find total
    for card in hand:
        if card == "J" or card == "Q" or card == "K":
            total+= 10;
        elif card == "A":
                total+= 0;
        else:
            total += card;
    
    # Add the aces last to make sure not over stacking
    for card in hand:
        if card == "A":
            if total >= 11:
                total+= 1;
            else: 
                total+= 11;      

    # Return total   
    return total;

# Hit function
def hit(hand):
	card = deck.pop();
	if(card == 11):
		card = "J";
	if(card == 12):
		card = "Q";
	if(card == 13):
		card = "K";
	if(card == 14):
		card = "A";
	hand.append(card);
	return hand;

# Print results - Full hands
async def print_results(message, dealer_hand, player_hand):
    await print_message(message.channel, "The dealer has a " + str(dealer_hand) + " for a total of " + str(total(dealer_hand)));
    await print_message(message.channel, "You have a " + str(player_hand) + " for a total of " + str(total(player_hand)));

# Print hands for decision - return choice of hit, stand, or quit
async def decision_prompt(message, dealer_hand, player_hand):
    await print_message(message.channel, "The dealer is showing " + str(dealer_hand[0]));
    await print_message(message.channel, "You have a " + str(player_hand) + " for a total of " + str(total(player_hand))); 
    
    choice = await get_player_choice(message);
    
    return choice;

# Check for natural blackjacks
async def blackjack(message, dealer_hand, player_hand):
    if total(player_hand) == 21 and total(dealer_hand) != 21:
        await print_message(message.channel, "Congratulations! You got a Blackjack! 🏆");
        return 1;
    if total(player_hand) == 21 and total(dealer_hand) == 21:
        await print_message(message.channel, "Dealer and player blackjack! Tie! 👌");
        return 2;
    if total(player_hand) != 21 and total(dealer_hand) == 21:
        await print_message(message.channel, "Dealer blackjack! Player loses. 😞");
        return 3;
    return 0;

async def score(message, dealer_hand, player_hand):
    # Scoring function
    await print_results(message, dealer_hand, player_hand);

    # Non bust conditions:
    if total(player_hand) <= 21:
        if total(player_hand) == total(dealer_hand):
            # Player, dealer tie
            await print_message(message.channel, "Tie! 👌");
        
        elif total(player_hand) >= total(dealer_hand):	
            # Player beat dealer, win
            await print_message(message.channel, "You win! 💰");
        
        elif total(player_hand) <= total(dealer_hand) and total(dealer_hand) <= 21:			   
            # Dealer beats player, loss    
            await print_message(message.channel, "Dealer wins! 😞");
    
        elif total(dealer_hand) > 21:
            # Dealer busts, player >= 21
            await print_message(message.channel, "Player wins, dealer busts! 🃏");
         
    if total(player_hand) > 21:
        # Player busted
        await print_message(message.channel, "Bust, you lose! 😞");


# blackjack game main function
async def blackjack_game(message):
    await print_message(message.channel, "🎰 WELCOME TO BLACKJACK! 🎲");
    dealer_hand = deal(deck);
    player_hand = deal(deck);

    # Check if either has blackjack
    result = await blackjack(message, dealer_hand, player_hand);
    if result != 0:
        await score(message, dealer_hand, player_hand);
        return;
    
    choice = "";

    # While not choose to quit
    while choice != "quit":
        # prompt
        if total(player_hand) != 21:
            choice = await decision_prompt(message, dealer_hand, player_hand);
        else:
            # See if dealer gets 21
            choice = "stand";
        if choice == "hit":
            hit(player_hand);
        elif choice == "stand":
            # While dealer under 17 must hit
            while total(dealer_hand) < 17:
                hit(dealer_hand);
            await score(message, dealer_hand, player_hand);
            break;
        elif choice == "quit":
            await print_message(message.channel, "Bye!");
            return;
        # Player Busts
        if total(player_hand) > 21:
            await score(message, dealer_hand, player_hand);
            break;