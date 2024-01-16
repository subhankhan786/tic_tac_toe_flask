from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)

board = [["", "", ""], ["", "", ""], ["", "", ""]]
current_player = 1

def check_win():
    global board
    # Check rows, columns, and diagonals for wins
    for i in range(3):
        if (board[i][0] == board[i][1] == board[i][2] != ""):
            return "win"  # Check rows
        if (board[0][i] == board[1][i] == board[2][i] != ""):
            return "win"  # Check columns
    if (board[0][0] == board[1][1] == board[2][2] != "" or
        board[0][2] == board[1][1] == board[2][0] != ""):
        return "win"  # Check diagonals

    # Check for tie
    if not any("" in row for row in board):
        return "tie"

    return False  # No win or tie yet

def button_color():
    if current_player == 1:
        return '#09C372'
    else:
        return '#498AFB'

@app.route('/')
def home():
    button_color_value = button_color()
    return render_template('home.html', board=board, current_player=current_player, button_color=button_color_value)

@app.route('/make_move', methods=['POST'])
def make_move():
    global current_player
    # Getting position
    if request.method == 'POST':
        position = request.form.get('position')
        row, col = map(int, position.split('-'))
        print(row, col)
        # Check if the cell is empty
        if not board[row][col] == "":
            return
        board[row][col] = "X" if current_player == 1 else "O"
        print([x for x in board])
        if check_win() == 'win':
            print(check_win())
            return render_template('game_over.html', status='win', player=current_player)
        if check_win() == 'tie':
            return render_template('game_over.html', status='tie')
        current_player = 3 - current_player
        print("Current player: ",current_player)
        return redirect('/')

@app.route('/reset', methods=['POST'])
def reset():
    global board, current_player
    board = [["", "", ""], ["", "", ""], ["", "", ""]]
    current_player = 1
    return redirect('/')

@app.route('/over')
def over():
    return render_template('game_over.html')

if __name__ == '__main__':
    app.run(debug=True)