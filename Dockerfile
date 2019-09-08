FROM instapy/instapy:latest
WORKDIR /code
COPY *.py  /code/

CMD ["python", "bot.py"]
