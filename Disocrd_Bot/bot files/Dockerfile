FROM python:3

WORKDIR /usr/src/app

RUN python3 -m pip install pyyaml
RUN python3 -m pip install discord
RUN python3 -m pip install fuzzywuzzy
RUN python3 -m pip install python-levenshtein

COPY . .

CMD [ "python", "./bot.py" ]