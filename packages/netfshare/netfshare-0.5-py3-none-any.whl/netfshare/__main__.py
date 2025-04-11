import os

from .netfshare import app, netfshare

# Register netfshare views blueprint
app.register_blueprint(netfshare)
port = int(app.config.get("PORT", 5000))
app.run(port=port, host='0.0.0.0')

print()
