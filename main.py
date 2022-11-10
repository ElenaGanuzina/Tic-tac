from token1 import TOKEN
from telegram import ReplyKeyboardRemove
from telegram.ext import (
    CommandHandler, 
    ConversationHandler, 
    Filters,
    MessageHandler, 
    Updater)

maps = list(range(1,10))

victories = [[0,1,2],
             [3,4,5],
             [6,7,8],
             [0,3,6],
             [1,4,7],
             [2,5,8],
             [0,4,8],
             [2,4,6]]
step = ""
win  = ""
symbol = ""
player = "X"
CHOICE = 0

# Вывод карты
def print_maps(maps, update, _): 
    for i in range(3):
        update.message.reply_text(f"| {maps[0 + i * 3]} | {maps[1 + i * 3]} | {maps[2 + i * 3]} |")



def check_line(sum_O,sum_X):
    step = ""
    for line in victories:
        o = 0
        x = 0

        for j in range(0,3):
            if maps[line[j]] == "O":
                o = o + 1
            if maps[line[j]] == "X":
                x = x + 1
 
        if o == sum_O and x == sum_X:
            for j in range(0,3):
                if maps[line[j]] != "O" and maps[line[j]] != "X":
                    step = maps[line[j]]           
    return step


def start(update, _):
    global maps, player, step
    player = "X"
    update.message.reply_text("Привет! Сыграем в крестики-нолики?" )
    update.message.reply_text(' 1 - да,\n 2 - нет\n')
    return CHOICE

def choice(update, _):
    global player, maps, victories, step, symbol, win
    user = update.message.from_user
    user_choice = update.message.text
    if user_choice == 1:
        game_over = False
        player = True
        while game_over == False:
            update.message.reply_text(print_maps(maps))
            if player == True:
                symbol = "X"
                step = update.message.reply_text("Твой ход: ")
                
            else:
                update.message.reply_text("Мой ход: ")
                symbol = "O"
                player_bot()

            if step != "":
                ind = maps.index(step)
                maps[ind] = symbol
                win = get_result() 
                if win != "":
                    game_over = True
                else:
                    game_over = False
            else:
                update.message.reply_text("Ничья!")
                game_over = True
                win = "победила дружба!"
        
            player = not(player)        
            
        update.message.reply_text(print_maps(maps))
        update.message.reply_text("Поздравляю,", win)
    
    elif user_choice == "2":
        update.message.reply_text('Тогда до скорого! :)')
        return ConversationHandler.END
    else:
        update.message.reply_text("Попробуй снова:\n 1 - да,\n 2 - нет\n")
    


def get_result():
    win = ''
    for i in victories:
        if maps[i[0]] == "X" and maps[i[1]] == "X" and maps[i[2]] == "X":
            win = "X"
        if maps[i[0]] == "O" and maps[i[1]] == "O" and maps[i[2]] == "O":
            win = "O"          
    return win
 
def player_bot():        
    step = ""
    step = check_line(2,0)
    if step == "":
        step = check_line(0,2)        
    if step == "":
        step = check_line(1,0)           
    if step == "":
        if maps[4] != "X" and maps[4] != "O":
            step = 5           
    if step == "":
        if maps[0] != "X" and maps[0] != "O":
            step = 1           
    return step
 

def cancel(update, _):
    update.message.reply_text("Пока!")
    return ConversationHandler.END


if __name__ == '__main__':
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOICE: [MessageHandler(Filters.text, choice)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)

    print('server start')

    updater.start_polling()
    updater.idle()