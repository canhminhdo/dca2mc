FROM ubuntu:24.04.1

RUN apt-get update && apt-get install -y \
    vim \
    wget \
    git \
    curl \
    zip \
    unzip \
    g++ \
    net-tools

RUN wget https://github.com/maude-lang/Maude/releases/download/Maude3.2/Maude-3.2-linux.zip \
    && unzip Maude-3.2-linux.zip && mv Linux64 Maude && mv Maude/maude.linux64 Maude/maude \
    && rm Maude-3.2-linux.zip

RUN wget http://maude.cs.illinois.edu/w/images/0/0a/Full-Maude-3.1.zip \
    && unzip Full-Maude-3.1.zip && mv full-maude31.maude Maude/full-maude.maude

ENV PATH=/Maude:$PATH

