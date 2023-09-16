FROM python:3.11
LABEL author=LEZGIDJ
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV TOKEN=0
ENV group_id=0
CMD ["python", "main.py"]
