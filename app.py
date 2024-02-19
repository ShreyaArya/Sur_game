from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
import random
import os
import numpy as np
from flask_session import Session


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Define a list of sound files (without the file extension)
sound_files = ["C4", "D4", "E4", "F4", "G4", "A4", "B4","Ab4","Bb4","Db4","Eb4","Gb4"]
#note_dict={0:"C4", 1: "D4", 2: "E4",3:}
note_dict={
    'C4': 0,
    'Db4': 1,
    'D4': 2,
    'Eb4': 3,
    'E4': 4,
    'F4': 5,
    'Gb4': 6,
    'G4': 7,
    'Ab4': 8,
    'A4': 9,
    'Bb4': 10,
    'B4': 11
}
surs=['sa',"kre",'re',"kga",'ga','ma',"tma",'pa',"kdha",'dha',"kni",'ni']
sur_dict = {
    0: 'sa',
    1: 'kre',
    2: 're',
    3: 'kga',
    4: 'ga',
    5: 'ma',
    6: 'tma',
    7: 'pa',
    8: 'kdha',
    9: 'dha',
    10: 'kni',
    11: 'ni'
}

def difference(note, scale):
    corresponding_number1= note_dict.get(note)
    corresponding_number2= note_dict.get(scale)
    #print(corresponding_number1,corresponding_number2)
    return np.remainder(corresponding_number1-corresponding_number2,12)

def sur_in_scale(note, scale):
    return sur_dict.get(difference(note,scale))


@app.route('/')
def start_game():
    return render_template('start.html')

@app.route('/start_game', methods=['POST'])
def initialize_game():
    scale = request.form.get('scale')
    session['scale'] = scale.upper() + "4"  # Store the scale in the session

    return redirect(url_for('play_game', scale=scale))

@app.route('/play_game', methods=['GET', 'POST'])
def play_game():
    feedback = ''  # Initialize feedback variable
    scale = session.get('scale', 'default_scale')  # Get the scale parameter from the URL
    #scale=scale.upper()+"4"
    #print(scale)
    random_sound = request.form.get('random_sound', random.choice(sound_files))
    if not random_sound:  # If random_sound is not provided, generate a new one
        random_sound = random.choice(sound_files)
    
    if request.method == 'POST':
        user_input = request.form.get('user_input', '').upper()
        correct_guesses = int(request.form.get('correct_guesses', 0))
        total_guesses = int(request.form.get('total_guesses', 0)) + 1

        answer_in_sur=sur_in_scale(random_sound,scale)
        #print("answer is", answer_in_sur)
        #print(user_input)
        # Compare only the first character of user_input and random_sound
        if user_input.upper() == answer_in_sur.upper():
            correct_guesses += 1
            feedback = 'correct'
            random_sound = random.choice(sound_files)
        else:
            feedback = 'incorrect'

        #if total_guesses == 10:  # You can adjust the total number of guesses
        #    return redirect(url_for('end_game', correct_guesses=correct_guesses, total_guesses=total_guesses))

        return render_template('game.html', random_sound=random_sound, correct_guesses=correct_guesses, total_guesses=total_guesses, feedback=feedback,surs=surs)

    return render_template('game.html', random_sound=random_sound, correct_guesses=0, total_guesses=0, feedback=feedback, surs=surs)

@app.route('/end_game')
def end_game():
    correct_guesses = request.args.get('correct_guesses', 0)
    total_guesses = request.args.get('total_guesses', 0)
    return render_template('end_game.html', correct_guesses=correct_guesses, total_guesses=total_guesses)

def serve_sound(filename):
    full_path = os.path.join(app.root_path, 'static', 'sounds', filename)
    
    # Check if the file exists
    if os.path.exists(full_path):
        # Send the file with proper MIME type
        response = send_from_directory(os.path.join(app.root_path, 'static', 'sounds'), filename, mimetype='audio/mpeg')
        # Enable support for range requests
        response.headers.add('Accept-Ranges', 'bytes')
        return response

    return 'File not found', 404

if __name__ == '__main__':
    app.run(debug=True)