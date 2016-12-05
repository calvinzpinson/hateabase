from sys import argv, exit as die
import pip

try:
    from mysql.connector import connect
    from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
except:
    try:
        pip.main(['install','-r','requirements.pip'])
        from mysql.connector import connect
        from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
    except:
        die(-1)

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def main():
    port_num = 5000
    if len(argv) == 2:
        port_num = int(argv[1])
    app.run(port=port_num)

if __name__ == '__main__':
    main()