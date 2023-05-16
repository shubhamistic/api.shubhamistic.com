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


## Production Commands (Ubuntu)

- SSH into your vpc using security key:
  ```bash
  $ ssh -i path-to-your-pem-file.pem ubuntu@ip
  ```
  
- Install gunicorn & gevent-websocket in global environment
  ```bash
  $ pip install gunicorn gevent-websocket
  ```
  
- Activate virtualenv and install the modules:
  ```bash
  $ virualenv project-directory
  $ cd project-directory
  $ source bin/activate
  $ pip install -r requirements.txt
  ```

- Run the server using:
  ```bash
  $ gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 -b 127.0.0.1:5000 app:app
  ```


## License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.


## About the Author
This repository is maintained by [shubhamistic](https://github.com/shubhamistic), a passionate programmer and web developer. Explore my projects and join me on my journey to create innovative solutions and push the boundaries of what's possible.


<p align="right">(<a href="#readme-top">back to top</a>)</p>
