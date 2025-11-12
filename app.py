from config import vuln_app
import os
from flask import Flask

app = Flask(__name__)

'''
 Decide if you want to server a vulnerable version or not!
 DO NOTE: some functionalities will still be vulnerable even if the value is set to 0
          as it is a matter of bad practice. Such an example is the debug endpoint.
'''
vuln = int(os.getenv('vulnerable', 1))
# vuln=1
# token alive for how many seconds?
alive = int(os.getenv('tokentimetolive', 60))


if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
