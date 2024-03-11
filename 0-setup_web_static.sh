#!/usr/bin/env bash
# A Bash script that sets up web servers for the deployment of web_static. It must:

#   - Install Nginx if it not already installed
if ! [ -x "$(command -v nginx)" ]; then
    sudo apt-get update
    sudo apt-get -y install nginx
    sudo service nginx start
fi

sudo service nginx start

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

#   - Create a fake HTML file /data/web_static/releases/test/index.html (with simple content, to test your Nginx configuration)
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

#   - Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder. If the symbolic link already exists, it should be deleted and recreated every time the script is ran.
sudo ln -sf /data/web_static/releases/test /data/web_static/current

#   - Give ownership of the /data/ folder to the ubuntu user AND group (you can assume this user and group exist). This should be recursive; everything inside should be created/owned by this user/group.
sudo chown -R ubuntu:ubuntu /data/

#   - Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static (ex: https://mydomainname.tech/hbnb_static). 
config_block="
    location /hbnb_static/ {
        alias /data/web_static/current/;
    }
"
sudo sed -i "/server_name _;/a $config_block" /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart

exit 0



# location=$(grep -Fn location $default_sites | head -1 | cut -d":" -f1)
# hbnb_static="\\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n"

# sudo mkdir -p "/data/web_static/releases/test/" "/data/web_static/shared/"
# echo "<h1>Hello World!</h1>" | sudo tee "/data/web_static/releases/test/index.html"
# sudo ln -sf "/data/web_static/releases/test/" "/data/web_static/current"
# sudo chown -hR ubuntu:ubuntu "/data/"

# sudo sed -i "${location}i ${hbnb_static}" "${default_sites}"
# sudo service nginx restart