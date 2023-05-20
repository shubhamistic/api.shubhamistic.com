<a name="readme-top"></a>

<div align="center">
  <h3 align="center">api.shubhamistic.com</h3>
  APIs designed specifically for shubhamistic.github.io webpages
  <p align="center">
    <a href="https://github.com/shubhamistic/api.shubhamistic.com"><strong>Explore the docs »</strong></a>
    <br />
    ·
    <a href="https://github.com/shubhamistic/api.shubhamistic.com/issues">Report Bug</a>
    ·
    <a href="https://github.com/shubhamistic/api.shubhamistic.com/issues">Request Feature</a>
    ·
  </p>
</div>


## SETUP (Ubuntu)

- SSH into your vpc using security key:
  ```bash
  ssh -i path-to-your-pem-file.pem ubuntu@ip
  ```

- Install NGINX:
  ```bash
  sudo apt update
  
  sudo apt install nginx
  ```

- Open nginx configuration file:
  ```bash
  sudo nano /etc/nginx/sites-available/default
  ```

- Clear the contents of the file and add the following lines (SAVE & EXIT):
  ```
  $ server {
    server_name <your-domain.com> <your-vpc-ip-address>;
    location / {
        include proxy_params;
        proxy_pass http://localhost:5000;
    }

    location /socket.io {
        include proxy_params;
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_pass http://localhost:5000/socket.io;
    }
  }
  ```

- Open bash profile:
  ```bash
  sudo nano ~/.bash_profile
  ```

- Append these lines inside bash profile (SAVE & EXIT):
  ```
  export DB_USER="<your-db-username>"
  export DB_PASS="<your-db-password>"
  export SECRET_KEY="<your-secret-key(any random string)>"
  ```
  
- Execute commands from a bash_profile in current shell environment:
  ```bash
  source ~/.bash_profile
  ```

- Install gunicorn & gevent-websocket in global environment:
  ```bash
  pip install gunicorn gevent-websocket
  ```
  
- Activate virtualenv and install the modules:
  ```bash
  virtualenv project-directory
  
  cd project-directory
  
  source bin/activate
  
  pip install -r requirements.txt
  ```

- Run the server using:
  ```bash
  gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 -b 127.0.0.1:5000 app:app
  ```

- **DATABASE CONFIGURATION**
  - Run the following commands in your mysql command line:
    - SQL commands for */tictactoe* route:
    ```bash
    CREATE DATABASE tictactoe;
    
    USE tictactoe;
    
    CREATE TABLE rooms ( 
        room_code INT PRIMARY KEY, 
        start_time DATETIME,
        end_time DATETIME,
        occupied BOOLEAN DEFAULT FALSE,
        token CHAR(20)
    );
    
    INSERT IGNORE INTO
    rooms (room_code, start_time, end_time)
    VALUES (1000, NOW(), NOW());
    
    COMMIT;
    ```
    

## License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.


## About the Author
This repository is maintained by [shubhamistic](https://github.com/shubhamistic), a passionate programmer and web developer. Explore my projects and join me on my journey to create innovative solutions and push the boundaries of what's possible.


<p align="right">(<a href="#readme-top">back to top</a>)</p>
