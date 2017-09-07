#activate_this = '/home/ubuntu/catalogapp/catalogappenv/bin/activate_this.py)
#execfile(activate_this, dict(__file__=activate_this))

from project import app
import sys
sys.path.insert(0, '/home/ubuntu/catalogapp')

# this is just if you run it using python wsgi:app ...
app.secret_key = 'TVLb2,zX,V#geo6j^dD%uzEgtsjaBoG8*AEKvMeeWR2{3;YNQ2{>3CgLrE4k2Lb3'

if __name__ == "__main__":
    app.secret_key = 'TVLb2,zX,V#geo6j^dD%uzEgtsjaBoG8*AEKvMeeWR2{3;YNQ2{>3CgLrE4k2Lb3'
    app.run(host='0.0.0.0', port=80)
