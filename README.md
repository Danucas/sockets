Sockets messaging
-----------------
Flask server to route sockets connections
and Simple client sockets for messaging services

Requirements
------------

- Flask
- pyaudio
- requests

Screenshots
-----------

![](/screenshots/1.png)

Run Flask server
----------------
```
$ ./app.py
```

Client install
--------------

```
$ ./install
```

cd to [client](client) and type

```
./chat.py
```

```
User not found
Please type a new Username: Danucas
Welcome!!  Danucas
To quit type '-logout'
---------------------
Select any option
---------------------
	0-Create a chatroom
	1-Join an existing chatroom
	2-Delete user
(default 0): 0
	Chat room created
	(Id): rbT38UdjCo2kzH0n
	Share this id with yours peers
connected to rbT38UdjCo2kzH0n
________________________________
Danucas > 
```


share the room Id: rbT38UdjCo2kzH0n
and start talking via socket connection


Contribute
----------

To add new features just fork this repo and ask for a PR, also please send me an email 
commenting about your experience with socket communication, we can build a community and bring great solutions for this.

Authors
-------

* Daniel Rodriguez 
	- Gmail [dnart.tech@gmail.com](dnart.tech@gmail.com)
	- Twitter [@Danucas1](https://twitter.com/Danucas1)
	- Linkedin [daniel-rodriguez-castillo](https://www.linkedin.com/in/daniel-rodriguez-castillo/)

	Software engineer from Holberton School interested in visual programming, signal processing, data analisys,
	graphics, sound and a lot of other fields.

Portfolio Project
-----------------
[Data in motion](https://github.com/alejolo311/DataInMotion)