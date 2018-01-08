FROM node:latest as admin-builder
WORKDIR /workspace
COPY www/apps/admin/adminify/package.json /workspace/package.json
RUN npm install --registry https://registry.npm.taobao.org
COPY www/apps/admin/adminify /workspace/
RUN npm run build 

FROM node:latest as article-builder
WORKDIR /workspace
COPY www/apps/article/front-admin/package.json /workspace/package.json
RUN npm install --registry https://registry.npm.taobao.org
COPY www/apps/article/front-admin /workspace
RUN npm run build


FROM python:3.6
LABEL Description="ncms project" Version="0.1"

WORKDIR /workspace

ENV TZ 'Asia/Shanghai'
    RUN echo $TZ > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata

COPY ./requirements.txt /workspace/

RUN pip install -r requirements.txt -i https://pypi.douban.com/simple && \
    rm -rf /root/.cache

EXPOSE 9000

COPY ./www /workspace/

COPY --from=admin-builder /workspace/dist /workspace/apps/admin/adminify/dist/
COPY --from=article-builder /workspace/dist /workspace/apps/article/front-admin/dist/

ENV PYTHONPATH=/workspace/
ENTRYPOINT [ "python", "ncms.py" ]
