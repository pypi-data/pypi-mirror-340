Installation
************

Pour installer **phystool** dans un environnement virtuel, il suffit de passer
par `pip`:

    pip install phystool


Le fichier de configuration LaTeX `texmf.cnf` doit contenir la ligne suivant:

    max_print_line=1000

Cela permet au compilateur LaTeX d'afficher des lignes plus longues et donc
permet un meilleur parsing des logs.


Requirements
============

+ Python 3.12
+ `ripgrep <https://github.com/BurntSushi/ripgrep>`_
+ `bat <https://github.com/sharkdp/bat>`_
+ `delta <https://github.com/dandavison/delta>`_
