# NOW
# TODO Add login system and page
# DONE Add SQL Alchemy Database
# TODO Add cart
#
# AFTER MEETING WITH ELIJAH
# TODO Add products
# TODO Format HTML pages
#
# END
# TODO Add email sending
# TODO Figure out security
# TODO Figure out purchase verification
# TODO Add to server
from RugWebsite import app, ph
from RugWebsite.database import Users, dropAll, createAll
from RugWebsite.__init__ import session

session.close()
dropAll()
createAll()

admin = Users(username="admin", password=ph.hash("adminpass"))
session.add(admin)
session.commit()

if __name__ == "__main__":
    app.run(debug=True)
