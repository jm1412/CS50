I wrote a detailed summary of how I approached the problem, but after an hour of playing with tensorflow and reading documentation and posts from people regarding best practices, I have come to 2 new learnings.

Good data, one that is understandable by the machine, is very important since it’s your starting point; this is why rescaling improved my accuracy dramatically.

There’s a delicate balance between wide and deep neural networks, and it’s a very interesting topic for me to learn especially since i stumbled upon it on my own after wondering how adding more layers vs adding more units will affect my machine.

Basically, for my case where the images don’t have a lot of variation (traffic signs), a wider network works better since I need my network to memorize, not generalize. For human faces, maybe, I’ll need a deeper network more than wide since I’d need my machine to generalize more than memorize.

Here’s the post in question: https://stats.stackexchange.com/questions/222883/why-are-neural-networks-becoming-deeper-but-not-wider/223637#223637