import telebot

size = 3
board = []
player = 'X'
step_count = 0

API_TOKEN = 'your token'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Предлагаю поиграть в крестики-нолики\nПравила ходов - /help.')
    bot.send_message(message.chat.id, 'Играем?\n"да" / "нет"')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Что бы сделать ход введите координаты точки через пробел и нажмиете Enter')


@bot.message_handler(content_types=['text'])
def game(message):
    global board
    global player
    global step_count
    if 'да' in message.text:
        board = [["-" for j in range(size)] for i in range(size)]
        bot.send_message(message.chat.id,'Поле:')
        get_board(message)
        bot.send_message(message.chat.id,'Ходит крестик, выберите клетку')
    elif 'нет' in message.text:
        bot.send_message(message.chat.id,'Надеюсь сыграем позже')
        exit()
    else:
        if player == 'X':
            hod = message.text.split()
            try:
                if board[int(hod[0])-1][int(hod[1])-1] != '-':
                    bot.send_message(message.chat.id, 'Эта клеточка занята')
                else:
                    step_x(hod)
                    player = '0'
                    get_board(message)
                    step_count += 1
                    if result() == True:
                        bot.send_message(message.chat.id,'Поздравляем! Крестики выиграли\nСыграем еще? "да" / "нет"')
                    elif step_count == size*size:
                        bot.send_message(message.chat.id, 'Победила дружба!\nСыграем еще? "да" / "нет"')
                    else:
                        bot.send_message(message.chat.id,'Ходит нолик, выберите клетку')
            except:
                bot.send_message(message.chat.id, 'Неправильный ввод')
        else:
            hod = message.text.split()
            try:
                if board[int(hod[0])-1][int(hod[1])-1] != '-':
                    bot.send_message(message.chat.id, 'Эта клеточка занята')
                else:
                    step_0(hod)
                    player = 'X'
                    get_board(message)
                    step_count += 1
                    if result() == True:
                        bot.send_message(message.chat.id,'Поздравляем! Нолики выиграли\nСыграем еще? "да" / "нет"')
                    elif step_count == size*size:
                        bot.send_message(message.chat.id, 'Победила дружба!\nСыграем еще? "да" / "нет"')
                    else:
                        bot.send_message(message.chat.id,'Ходит крестик, выберите клетку')
            except:
                bot.send_message(message.chat.id, 'Неправильный ввод')

def step_x(list):
    global board
    board[int(list[0])-1][int(list[1])-1] = 'X'
def step_0(list):
    global board
    board[int(list[0])-1][int(list[1])-1] = '0'
def get_board(text):
    bot.send_message(text.chat.id, f"{'   '.join(board[0])}\n{'   '.join(board[1])}\n{'   '.join(board[2])}")
def result():
    count = 0
    global board
    for j in range(size):
        count = 0
        for i in range(size-1):
            if board[i][j] == board[i+1][j] and board[i][j] != '-':
                count += 1
        if count == 2:
            return True
    for i in range(size):
        if board[i].count(board[i][j]) == len(board[i]) and board[i][j] != '-':
            return True
    count = 0
    for i in range(size-1):
        if board[i][i] == board[i+1][i+1] and board[i][i] != '-':
            count += 1
    if count == 2:
        return True
    count = 0
    for i in range(size-1):
        if board[i][-1-i] == board[i+1][-2-i] and board[i][-1-i] != '-':
            count += 1
    if count == 2:
        return True

bot.polling()