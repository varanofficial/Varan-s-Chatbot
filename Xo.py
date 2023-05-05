import discord
import random

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!xo'):
        board = [':white_large_square:', ':white_large_square:', ':white_large_square:',
                 ':white_large_square:', ':white_large_square:', ':white_large_square:',
                 ':white_large_square:', ':white_large_square:', ':white_large_square:']
        win_combinations = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        turn = random.choice(['X', 'O'])
        game_over = False

        def draw_board():
            row1 = '|'.join(board[0:3])
            row2 = '|'.join(board[3:6])
            row3 = '|'.join(board[6:9])
            return f'{row1}\n{row2}\n{row3}'

        def check_win(player):
            for combo in win_combinations:
                if all(board[i] == player for i in combo):
                    return True
            return False

        async def get_player_move():
            valid = False
            while not valid:
                response = await client.wait_for('message')
                if response.author == message.author and response.content.isdigit():
                    index = int(response.content)
                    if 0 < index <= 9 and board[index - 1] == ':white_large_square:':
                        valid = True
                        board[index - 1] = turn
                        await response.delete()
                        return

        async def game():
            nonlocal turn
            while not game_over:
                if turn == 'X':
                    await message.channel.send(f'It\'s your turn {message.author.mention}. Pick a spot.')
                    await get_player_move()
                    if check_win('X'):
                        await message.channel.send(draw_board())
                        await message.channel.send(f'Congratulations {message.author.mention}! You win!')
                        return
                    turn = 'O'
                else:
                    index = random.randint(0, 8)
                    while board[index] != ':white_large_square:':
                        index = random.randint(0, 8)
                    board[index] = 'O'
                    if check_win('O'):
                        await message.channel.send(draw_board())
                        await message.channel.send('Sorry, you lose.')
                        return
                    turn = 'X'
                if ':white_large_square:' not in board:
                    await message.channel.send(draw_board())
                    await message.channel.send('It\'s a tie!')
                    return
                await message.channel.send(draw_board())

        await message.channel.send('Welcome to X/O!')
        await message.channel.send(draw_board())
        await game()

client.run('your-token-here')
