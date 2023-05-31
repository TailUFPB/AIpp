FROM postgres

WORKDIR /db

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r app/requirements.txt

COPY . .

CMD ["python", "../api/main.py"]