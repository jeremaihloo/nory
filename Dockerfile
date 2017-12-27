FROM python:3.6
LABEL Description="ncms project" Version="0.1"

WORKDIR /workspace

ENV TZ 'Asia/Shanghai'
    RUN echo $TZ > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata

COPY ./requirements.txt /workspace/

RUN pip install -r requirements.txt

EXPOSE 9000

COPY ./www /workspace/
ENV PYTHONPATH=/workspace/
CMD ["python", "ncms.py"]

